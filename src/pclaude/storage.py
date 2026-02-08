"""JSONL storage module for prompt archive."""

import json
import os
from pathlib import Path


def get_archive_path() -> Path:
    """Get archive file path (supports environment variable override)."""
    env_path = os.environ.get("PROMPT_ARCHIVE_DIR")
    if env_path:
        return Path(env_path) / "prompts.jsonl"
    return Path.home() / ".prompt-archive" / "prompts.jsonl"


def get_next_id(path: Path) -> int:
    """Read the last record ID and return the next ID."""
    if not path.exists():
        return 1
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    if not lines:
        return 1
    last = json.loads(lines[-1])
    return int(last["id"].lstrip("#")) + 1


def append_prompt(path: Path, record: dict) -> None:
    """Append a record to the JSONL file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def read_all(path: Path) -> list[dict]:
    """Read all records from the JSONL file."""
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def search_prompts(path: Path, keyword: str) -> list[dict]:
    """Fuzzy search prompts by keyword."""
    records = read_all(path)
    keyword_lower = keyword.lower()
    return [r for r in records if keyword_lower in r["prompt"].lower()]


def get_prompt_by_id(path: Path, id_num: int) -> dict | None:
    """Get a specific prompt by ID number."""
    records = read_all(path)
    for record in records:
        if int(record["id"].lstrip("#")) == id_num:
            return record
    return None


def get_recent_prompts(path: Path, limit: int) -> list[dict]:
    """Get the most recent N prompts."""
    records = read_all(path)
    return records[-limit:]
