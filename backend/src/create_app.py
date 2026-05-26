from _thread import lock
import os
import sys
import threading
import time

# Third-party imports
from flask import Flask, Response, jsonify, render_template
from flask_cors import CORS
from src.config import  config as project_config
from src.core.live_data_manager import live_data_manager
from flask import Flask, Response, jsonify, render_template



# 全局日志队列，用于 SSE 推送
class LogQueue:
    """线程安全的内存日志队列。"""

    def __init__(self, maxsize=100):
        self.queue = []
        self.maxsize = maxsize
        self.lock: lock = threading.Lock()

    def put(self, msg):
        """追加一条日志（空白会被过滤）。"""
        with self.lock:
            # 过滤掉一些无意义的换行或空白
            clean_msg = msg.strip()
            if not clean_msg:
                return
            # 不再重复添加时间戳，因为原始日志中通常已经包含了时间
            self.queue.append(clean_msg)
            if len(self.queue) > self.maxsize:
                self.queue.pop(0)

    def get_all(self):
        """取出并清空队列中的全部日志。"""
        with self.lock:
            logs = list(self.queue)
            self.queue.clear()
            return logs
        
global_log_queue = LogQueue()



# 重定向 stdout 以捕获 print 语句
class StdoutRedirector:
    """将写入 sys.stdout 的内容同步写入日志队列。"""

    def __init__(self, original_stdout, log_queue):
        self.original_stdout = original_stdout
        self.log_queue = log_queue

    def write(self, msg):
        """写入 stdout 的同时，把日志推入 SSE 队列。"""
        self.log_queue.put(msg)
        self.original_stdout.write(msg)

    def flush(self):
        """刷新底层 stdout。"""
        self.original_stdout.flush()

if not isinstance(sys.stdout, StdoutRedirector):
    sys.stdout = StdoutRedirector(sys.stdout, global_log_queue)


def create_app() -> Flask:
    app = Flask(import_name=__name__,
                static_folder="../../frontend/static",
                template_folder="../../frontend/templates")
    
    CORS(app, resources={
        r"/*": {"origins": "*"}
    })

    # 加载项目配置（包含 LLM_* 等）
    cfg_name = os.environ.get('FLASK_ENV', 'development')
    cfg_cls = project_config.get(cfg_name) or project_config.get('default')
    app.config.from_object(obj=cfg_cls)
    
    # 启动市场数据服务
    try:
        live_data_manager.start()
    except Exception as e:
        print(f"Error starting LiveDataManager: {e}")

    @app.route('/')
    def index():
        """主页。"""
        return render_template('index.html')

    @app.route('/strategy')
    def strategy():
        """策略回测页。"""
        return render_template('backtest.html')

    @app.route('/trading')
    def trading():
        """手动交易页。"""
        return render_template('trader.html')

    @app.route('/run')
    def run():
        """运行策略页。"""
        return render_template('gostrategy.html')

    # SSE 日志流
    @app.route('/api/logs/stream')
    def stream_logs():
        """日志实时流（SSE）。

        前端通过 EventSource 或 fetch 流式读取该接口，以获得后台日志增量。
        """
        def generate():
            """生成 SSE 数据流。"""
            # 建立连接时先发送一个欢迎消息
            yield "data: [SYSTEM] Log stream connected...\n\n"
            while True:
                logs = global_log_queue.get_all()
                for log in logs:
                    # SSE 格式必须以 data: 开头，并以 \n\n 结束
                    yield f"data: {log}\n\n"
                time.sleep(0.5)
        return Response(generate(), mimetype='text/event-stream')
    
    @app.errorhandler(404)
    def not_found(error):
        """未知路由。"""
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """服务端错误兜底。"""
        return jsonify({'error': 'Internal server error'}), 500
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)