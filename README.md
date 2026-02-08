# pclaude

Prompt archive for Claude Code CLI - Automatically capture, archive, and search your Claude prompts.

## Why pclaude?

Every well-crafted prompt you send to Claude becomes a permanent, searchable asset. Stop losing valuable prompts and start building your "prompt equity."

## Installation

### From Source (Development)

```bash
# Clone and install in editable mode
git clone https://github.com/linsipeng/pclaude.git
cd pclaude
pip install -e .

# Or with pipx
pipx install -e .
```

### From PyPI (Coming Soon)

```bash
pipx install pclaude
```

## Quick Start

### 1. Run claude with automatic capture

```bash
pclaude "Write a Python script to scrape Amazon prices"
```

You'll see:
```
[SAVED] #1 (2026-02-08 15:30)
Use: pclaude show 1    or    pclaude use 1
```

### 2. List your prompts

```bash
# Recent 10 prompts (default)
pclaude ls

# Recent 20 prompts
pclaude ls --recent 20

# All prompts
pclaude ls --all
```

Output:
```
 ID   Time   Prompt
 #3   15:45   Analyze my FBA ad spend last week...
 #2   15:35   Write a Python script to scrape Ama...
 #1   15:30   Write a function to calculate tax...
```

### 3. Search prompts

```bash
pclaude search Amazon
```

Output:
```
Found 1 match(es):

#1  2026-02-08T15:30:00
  Write a Python script to scrape Amazon product prices
```

### 4. Show full prompt

```bash
pclaude show 1
```

Output:
```
#1  2026-02-08T15:30:00

Write a Python script to scrape Amazon product prices and save to CSV
```

### 5. Reuse and modify

```bash
# Reuse as-is
pclaude use 1

# Reuse with modifications
pclaude use 1 "and save to JSON instead"
```

## Command Reference

| Command | Description |
|---------|-------------|
| `pclaude "prompt"` | Run claude with automatic capture |
| `pclaude ls` | List recent prompts |
| `pclaude search <keyword>` | Search prompts |
| `pclaude show <id>` | Show full prompt |
| `pclaude use <id> [append]` | Reuse a prompt |

### Options

#### ls
- `--recent, -n <N>` - Show N recent prompts (default: 10)
- `--all` - Show all prompts

#### search
- `<keyword>` - Search term (required)

#### show
- `<id>` - Prompt ID number (required)

#### use
- `<id>` - Prompt ID number (required)
- `[append]` - Additional instructions (optional)

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PROMPT_ARCHIVE_DIR` | Custom directory for prompts.jsonl | `~/.prompt-archive/` |

Example:
```bash
export PROMPT_ARCHIVE_DIR=/path/to/my/prompts
```

### Storage Location

Prompts are stored in JSONL format at:
- **Default**: `~/.prompt-archive/prompts.jsonl`
- **Custom**: `$PROMPT_ARCHIVE_DIR/prompts.jsonl`

Each line is a JSON record:
```json
{"id": "#123", "timestamp": "2026-02-08T15:30:00+09:00", "prompt": "...", "source": "one-shot", "session_id": null}
```

## Requirements

- Python 3.11+
- Claude Code CLI
- typer >= 0.12
- rich >= 13

## Development

```bash
# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Build package
poetry build
```

## Roadmap

- [ ] v1.0 - MVP (current)
- [ ] v1.1 - Interactive REPL support, quiet mode config
- [ ] v1.2 - Prompt templates, tags, batch export
- [ ] v2.0 - Prompt versioning, edit/fork

## License

MIT
