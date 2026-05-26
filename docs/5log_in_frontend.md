用户正在查看 `src/create_app.py` 文件，并且询问 `stream_logs` 的解释。我需要先读取这个文件，看看 `stream_logs` 是什么。从文件名来看，这是 Flask 应用工厂文件，可能包含一个日志流端点。让我先读取文件内容。
现在我看到了 `stream_logs` 函数。这是一个 Flask 路由处理器，用于提供服务器发送事件（Server-Sent Events, SSE）的日志流。让我详细解释一下这个函数。首先，我需要理解整个上下文：有一个 `LogQueue` 类用于存储日志，`StdoutRedirector` 类将标准输出重定向到该队列，`global_log_queue` 是全局实例。`stream_logs` 函数通过 SSE 将队列中的日志推送到客户端。

我需要向用户解释 `stream_logs` 的工作原理、用途以及相关组件。用户可能想了解这个功能是如何工作的，或者为什么需要它。我应该用中文回答，因为之前的对话都是中文。让我组织一下解释。首先，说明这是一个 SSE 端点，用于实时推送日志到前端。然后，解释相关组件：`LogQueue`、`StdoutRedirector`、`global_log_queue`。接着，详细说明 `stream_logs` 函数：它定义了一个生成器 `generate()`，该生成器持续从队列中获取日志并以 SSE 格式发送。最后，总结其用途：用于前端实时显示后端日志，比如策略运行状态、市场数据更新等。

我还应该提到，这个功能对于量化交易系统很有用，因为需要实时监控策略执行和市场数据。另外，注意代码中有一个问题：第1行导入了 `_thread.lock`，但应该是 `threading.Lock`。不过，用户没有问这个，所以我暂时不提。

现在，开始回答。
`stream_logs` 是一个 Flask 路由函数，它实现了 **服务器发送事件（Server-Sent Events, SSE）** 的日志流功能，用于将后端产生的日志实时推送到前端页面。

## 核心机制

### 1. **日志收集系统**
- **`LogQueue` 类**：线程安全的内存日志队列，用于临时存储日志消息（最大容量100条）。
- **`StdoutRedirector` 类**：重定向 `sys.stdout`（标准输出），使得所有 `print()` 语句的输出同时被捕获到日志队列中。
- **`global_log_queue`**：全局单例，整个应用共享的日志队列实例。

### 2. **SSE 端点 `/api/logs/stream`**
```python
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
```

## 工作流程

1. **日志产生**：任何使用 `print()` 的输出（包括 Flask 应用、市场数据网关、策略引擎等）都会被 `StdoutRedirector` 捕获并存入 `global_log_queue`。

2. **前端连接**：前端页面通过 JavaScript 的 `EventSource` API 连接到 `/api/logs/stream` 端点。

3. **实时推送**：
   - 连接建立时，立即发送欢迎消息
   - 每 0.5 秒检查一次日志队列
   - 将队列中的所有日志以 SSE 格式（`data: 日志内容\n\n`）发送给客户端
   - 发送后清空队列，避免重复发送

4. **前端接收**：前端通过 `EventSource` 的 `onmessage` 事件处理函数接收并显示日志。

## 在量化交易系统中的用途

这个功能特别适合需要实时监控的场景：

1. **策略执行跟踪**：实时显示策略开平仓信号、订单执行状态
2. **市场数据监控**：显示数据网关的连接状态、tick 接收情况
3. **系统运行状态**：显示服务启动、停止、错误信息
4. **调试与诊断**：开发时实时查看后端日志，无需查看终端输出

## 技术特点

- **低延迟**：0.5 秒的轮询间隔保证了实时性
- **轻量级**：相比 WebSocket，SSE 更简单，适合单向日志推送
- **自动重连**：SSE 协议支持自动重连机制
- **跨域支持**：通过 Flask-CORS 允许前端跨域访问

## 前端使用示例

```javascript
// 在前端页面中连接日志流
const eventSource = new EventSource('/api/logs/stream');

eventSource.onmessage = function(event) {
    const logElement = document.getElementById('log-container');
    logElement.innerHTML += event.data + '<br>';
    logElement.scrollTop = logElement.scrollHeight; // 自动滚动到底部
};

eventSource.onerror = function() {
    console.error('Log stream connection lost, attempting to reconnect...');
};
```

## 注意事项

1. **连接数限制**：每个浏览器标签页会建立一个持久连接
2. **内存管理**：日志队列有大小限制（100条），避免内存泄漏
3. **性能影响**：大量日志输出时可能影响性能，生产环境建议使用专门的日志系统

这个功能使得前后端分离的架构中，前端能够实时获得后端的运行状态，极大提升了系统的可观测性和用户体验。