# pclaude

Prompt archive for Claude Code CLI.

## Installation

```bash
pipx install pclaude
```

## Usage

```bash
# Run claude with automatic prompt capture
pclaude "your prompt here"

# List recent prompts
pclaude ls --recent 10

# Search prompts
pclaude search "keyword"

# Show full prompt
pclaude show 123

# Reuse a prompt
pclaude use 123 "additional instructions"
```
