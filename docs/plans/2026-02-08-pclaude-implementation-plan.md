# pclaude 实施计划

**版本**: 1.0
**基于**: PRD-pclaude-v1.md
**创建日期**: 2026-02-08

## 阶段一：项目初始化

### 1.1 创建项目结构

```bash
pclaude/
├── src/
│   └── pclaude/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── capture.py
│       ├── storage.py
│       └── utils.py
├── pyproject.toml
├── README.md
├── .gitignore
└── tests/
    └── test_storage.py
```

### 1.2 配置 pyproject.toml

```toml
[project]
name = "pclaude"
version = "0.1.0"
description = "Prompt archive for Claude Code CLI"
readme = "README.md"
requires-python = ">=3.11"
authors = [{name = "Sam Lam"}]
dependencies = [
    "typer>=0.12",
    "rich>=13",
]

[project.scripts]
pclaude = "pclaude.__main__:main"

[build-system]
requires = ["poetry-core>=1.0"]
build-backend = "poetry.core.masonry.api"
```

## 阶段二：核心模块实现

### 2.1 storage.py - JSONL 存储模块

**职责**: 管理 `~/.prompt-archive/prompts.jsonl` 文件的读写

```python
# storage.py 核心函数

def get_archive_path() -> Path:
    """获取存档文件路径（支持环境变量覆盖）"""
    env_path = os.environ.get("PROMPT_ARCHIVE_DIR")
    if env_path:
        return Path(env_path) / "prompts.jsonl"
    return Path.home() / ".prompt-archive" / "prompts.jsonl"

def get_next_id(path: Path) -> int:
    """读取最后一条记录的 ID，返回下一个 ID"""
    if not path.exists():
        return 1
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    if not lines:
        return 1
    last = json.loads(lines[-1])
    return int(last["id"].lstrip("#")) + 1

def append_prompt(path: Path, record: dict) -> None:
    """追加一条记录到 JSONL 文件"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

def read_all(path: Path) -> list[dict]:
    """读取所有记录（用于 ls/search）"""
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def search_prompts(path: Path, keyword: str) -> list[dict]:
    """模糊搜索 prompt 内容"""
    records = read_all(path)
    keyword_lower = keyword.lower()
    return [r for r in records if keyword_lower in r["prompt"].lower()]
```

### 2.2 utils.py - 辅助函数

**职责**: 颜色输出、时间格式化、prompt 提取

```python
# utils.py

from datetime import datetime
from rich.console import Console
from rich.theme import Theme

console = Console(theme=Theme({"repr.str": "green"}))

def format_timestamp(ts: str) -> str:
    """将 ISO 8601 转换为简洁显示格式"""
    dt = datetime.fromisoformat(ts.replace("+00:00", ""))
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def extract_time_only(ts: str) -> str:
    """提取时间部分（用于 ls 简洁显示）"""
    dt = datetime.fromisoformat(ts.replace("+00:00", ""))
    return dt.strftime("%H:%M")

def get_prompt_text(args: list[str]) -> str:
    """从 sys.argv 提取用户 prompt 文本"""
    # -p "prompt text" 或直接跟随的文本
    # 需要处理引号和多参数情况
    pass  # 详细实现在 capture.py 中处理
```

### 2.3 capture.py - 核心捕获逻辑

**职责**: 参数解析、prompt 捕获、保存、转发

```python
# capture.py

import subprocess
import sys
from pathlib import Path

from storage import (
    get_archive_path,
    get_next_id,
    append_prompt,
)
from utils import format_timestamp, extract_time_only, console

def capture_and_run(args: list[str]) -> None:
    """主流程：捕获 prompt → 保存 → 转发给 claude"""
    archive_path = get_archive_path()

    # 1. 提取 prompt 文本
    prompt_text = extract_prompt_from_args(args)

    # 2. 生成记录
    next_id = get_next_id(archive_path)
    record = {
        "id": f"#{next_id}",
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt_text,
        "source": "one-shot",
        "session_id": None,
    }

    # 3. 保存
    append_prompt(archive_path, record)

    # 4. 反馈（除非 --quiet）
    if "--quiet" not in args:
        show_save_feedback(next_id, record["timestamp"])

    # 5. 转发给 claude
    subprocess.run(
        ["claude"] + args,
        shell=False,  # PRD 确认：安全方案
        check=False,  # 让 claude 自己处理错误
    )

def extract_prompt_from_args(args: list[str]) -> str:
    """从命令行参数中提取原始 prompt 文本"""
    # -p 后的内容或直接跟随的参数
    # 需要正确处理引号
    pass  # 详细实现
```

### 2.4 cli.py - 子命令定义

**职责**: `ls`, `search`, `show`, `use` 子命令

```python
# cli.py

import typer
from typing import Optional
from rich.table import Table
from rich.console import Console

from storage import read_all, search_prompts, get_archive_path, append_prompt
from utils import extract_time_only, console

app = typer.Typer()

@app.command()
def ls(
    recent: int = typer.Option(10, "--recent", "-n"),
    all: bool = typer.Option(False, "--all"),
):
    """显示最近的 prompts"""
    pass

@app.command()
def search(keyword: str):
    """搜索 prompts"""
    pass

@app.command()
def show(id: int):
    """显示完整 prompt"""
    pass

@app.command()
def use(id: int, append: Optional[str] = typer.Argument(None)):
    """复用历史 prompt"""
    pass
```

### 2.5 __main__.py - 入口分发

**职责**: 判断是子命令还是代理模式

```python
# __main__.py

import sys
from cli import app
from capture import capture_and_run

def main():
    if len(sys.argv) < 2:
        app()
        return

    first_arg = sys.argv[1]

    # 子命令列表
    subcommands = ["ls", "list", "search", "show", "use", "--help", "-h"]

    if first_arg in subcommands or first_arg.startswith("-"):
        # 子命令或全局参数
        app()
    else:
        # 代理模式：捕获并转发
        capture_and_run(sys.argv[1:])

if __name__ == "__main__":
    main()
```

## 阶段三：测试验证

### 3.1 单元测试

```python
# tests/test_storage.py

def test_get_next_id_new_file():
    path = Path("/tmp/test_prompts.jsonl")
    assert get_next_id(path) == 1

def test_append_and_read():
    append_prompt(path, {"id": "#1", "prompt": "test"})
    records = read_all(path)
    assert len(records) == 1
```

### 3.2 集成测试

```bash
# 测试流程
$ pip install -e .
$ pclaude ls  # 验证空状态
$ pclaude "test prompt"  # 验证保存
$ pclaude search "test"  # 验证搜索
$ pclaude show 1  # 验证显示
```

## 阶段四：打包发布

```bash
# Poetry 构建
poetry build

# 发布到 PyPI（需要认证）
poetry publish

# 安装验证
pipx install dist/pclaude-*.whl
```

## 风险与注意事项

| 风险 | 缓解措施 |
|------|----------|
| 参数透传不完整 | 全面测试常见组合；使用 `shell=False` |
| 引号处理问题 | 使用 `shlex` 或正确传递 list |
| 文件并发写 | 单用户场景，Python append 原子安全 |

## 依赖安装顺序

```bash
pip install typer rich
# 或
poetry add typer rich
```
