
```python
root_dir = Path(__file__).resolve().parent.parent
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
```


```python
# 使用 pathlib.Path
root_dir = Path(__file__).resolve().parent.parent

# 使用 os.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
```

## 主要区别

### 1. **API 风格**
- **`os.path`**: 函数式/过程式风格，需要嵌套函数调用
- **`pathlib.Path`**: 面向对象风格，更直观和优雅

### 2. **可读性对比**

从你的代码可以看出明显的可读性差异：

```python
# os.path - 嵌套难读
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# pathlib - 链式调用，清晰易懂
root_dir = Path(__file__).resolve().parent.parent
```

### 3. **路径拼接**
```python
# os.path
import os
data_dir = os.path.join(os.path.dirname(__file__), 'data', 'output.csv')

# pathlib - 使用 / 运算符
from pathlib import Path
data_dir = Path(__file__).parent / 'data' / 'output.csv'
```

### 4. **功能完整性**

`pathlib.Path` 不仅处理路径，还集成了文件操作：

```python
from pathlib import Path

p = Path('data/output.csv')

# 路径操作
p.parent          # 父目录
p.name            # 文件名
p.suffix          # 扩展名
p.stem            # 文件名（无扩展名）
p.exists()        # 是否存在
p.is_file()       # 是否是文件
p.is_dir()        # 是否是目录

# 文件操作（无需额外 import）
p.read_text()     # 读取文本
p.write_text('...')  # 写入文本
p.read_bytes()    # 读取二进制
p.mkdir(parents=True)  # 创建目录
```

而 `os.path` 只处理路径，文件操作需要额外的 `open()`、`os.makedirs()` 等。

## 推荐：使用 `pathlib.Path`

**原因：**

1. **Python 官方推荐**：从 Python 3.4+ 引入，是处理路径的现代标准
2. **更简洁可读**：代码更直观，维护更容易
3. **功能更全面**：路径处理 + 文件操作一体化
4. **跨平台更好**：自动处理不同操作系统的路径分隔符
5. **类型提示友好**：IDE 能提供更好的自动补全

