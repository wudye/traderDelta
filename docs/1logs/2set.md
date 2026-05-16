Let me explain how to add a FileHandler to the logger so that logs are also written to a file, not just the terminal (StreamHandler).

The user wants to know how to write logs to a file in addition to or instead of the terminal output.

I should explain:
1. StreamHandler - for console output (current)
2. FileHandler - for file output
3. How to add both
4. Maybe RotatingFileHandler for log rotation

Since I'm in ask mode, I can only provide explanations and code examples, not actually edit files
好问题！当前你的 `Logger` 只配置了 `StreamHandler`（终端输出），需要添加 `FileHandler` 来写入文件。

---

## 两种 Handler 对比

| Handler | 用途 |
|---------|------|
| `StreamHandler(sys.stdout)` | 输出到终端（当前配置） |
| `FileHandler("path/to/log.log")` | 输出到文件 |

---

## 修改方案：同时输出到终端和文件

修改 `libs/quant/src/quant/core/logger.py`：

```python
import logging
import sys
from pathlib import Path


class Logger:

    def __init__(self, name: str = "quant", level: str = "INFO", log_file: str = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        self.logger.propagate = False  # 防止重复日志

        if not self.logger.handlers:
            # 1. 终端输出 Handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_formatter = logging.Formatter(
                '[%(asctime)s] %(levelname)-7s %(name)-20s >>> %(message)s',
                datefmt='%H:%M:%S'
            )
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)

            # 2. 文件输出 Handler（如果指定了 log_file）
            if log_file:
                log_path = Path(log_file)
                log_path.parent.mkdir(parents=True, exist_ok=True)  # 自动创建目录
                
                file_handler = logging.FileHandler(log_file, encoding='utf-8')
                file_formatter = logging.Formatter(
                    '[%(asctime)s] %(levelname)-7s %(name)-20s >>> %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'  # 文件日志建议带日期
                )
                file_handler.setFormatter(file_formatter)
                self.logger.addHandler(file_handler)
```

---

## 使用方法

```python
from quant.core.logger import Logger

# 只输出到终端
logger = Logger()

# 同时输出到终端和文件
logger = Logger(log_file="logs/quant.log")

logger.info("This is a test message")
```

---

## 进阶：按日期自动轮转日志文件

如果你想**每天生成一个新的日志文件**，可以使用 `TimedRotatingFileHandler`：

```python
import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


class Logger:

    def __init__(self, name: str = "quant", level: str = "INFO", log_file: str = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        self.logger.propagate = False

        if not self.logger.handlers:
            # 终端 Handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_formatter = logging.Formatter(
                '[%(asctime)s] %(levelname)-7s %(name)-20s >>> %(message)s',
                datefmt='%H:%M:%S'
            )
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)

            # 文件 Handler（带日期轮转）
            if log_file:
                log_path = Path(log_file)
                log_path.parent.mkdir(parents=True, exist_ok=True)

                # 每天轮转，保留 7 天
                file_handler = TimedRotatingFileHandler(
                    log_file,
                    when='midnight',      # 每天午夜轮转
                    interval=1,           # 间隔 1 天
                    backupCount=7,        # 保留 7 个备份
                    encoding='utf-8'
                )
                file_handler.suffix = '%Y-%m-%d'  # 备份文件后缀
                file_formatter = logging.Formatter(
                    '[%(asctime)s] %(levelname)-7s %(name)-20s >>> %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
                file_handler.setFormatter(file_formatter)
                self.logger.addHandler(file_handler)
```

---

## 日志文件效果

```
logs/
├── quant.log              ← 当前日志
├── quant.log.2026-05-15   ← 昨天的日志
├── quant.log.2026-05-14
└── ...
```

---

你目前处于 **ask 模式**，如果需要我帮你修改 `logger.py` 文件，请切换到 **craft 模式**。