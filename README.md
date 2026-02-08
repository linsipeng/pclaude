# pclaude

**Auto-capture your Claude prompts.** Every prompt becomes a permanent, searchable asset.

## Why pclaude?

- **Never lose a good prompt** - Automatically saved
- **Easy to find** - Search and reuse instantly
- **Zero friction** - Works with your existing workflow

## Installation

### Windows

```powershell
# 双击运行 install.bat 或执行：
powershell -ExecutionPolicy Bypass -File install.bat
```

### macOS / Linux

```bash
# 1. 安装 pclaude
pipx install pclaude

# 2. 设置 alias
pclaude install-alias
source ~/.zshrc  # 或 source ~/.bashrc
```

### 从源码安装

```bash
git clone https://github.com/linsipeng/pclaude.git
cd pclaude
pip install -e .
pclaude install-alias
```

## Usage

```bash
# 直接用 claude，prompt 自动保存
claude "Write a Python function to calculate Fibonacci"

# 查看历史
pclaude ls

# 搜索
pclaude search Fibonacci

# 复用
pclaude use 1 "with memoization"
```

## Commands

| Command | Description |
|---------|-------------|
| `claude "prompt"` | Run claude (auto-captures) |
| `pclaude ls` | List prompts |
| `pclaude search <keyword>` | Search prompts |
| `pclaude show <id>` | Show full prompt |
| `pclaude use <id> [text]` | Reuse with optional append |
| `pclaude install-alias` | Install claude alias |

### ls Options

- `--recent, -n <N>` - Show N recent prompts (default: 10)
- `--all` - Show all prompts

## Configuration

### Environment Variables

| Variable | Default |
|----------|---------|
| `PROMPT_ARCHIVE_DIR` | `~/.prompt-archive/` |

### Storage

Prompts stored at: `~/.prompt-archive/prompts.jsonl`

Format:
```json
{"id": "#123", "timestamp": "2026-02-08T15:30:00+09:00", "prompt": "...", "source": "one-shot", "session_id": null}
```

## How It Works

```
claude "prompt" → pclaude captures → saves to JSONL → runs actual claude
```

pclaude wraps the `claude` command to capture your prompts before forwarding them to the real Claude CLI.

## Requirements

- Python 3.11+
- Claude Code CLI

## Roadmap

- [x] v1.0 - MVP (capture, ls, search, show, use)
- [ ] v1.1 - Alias installation, quiet mode
- [ ] v1.2 - Templates, tags, export
- [ ] v2.0 - Versioning, edit/fork

## License

MIT
