"""Unit tests for storage module."""

import json
import os
import tempfile
from pathlib import Path

import pytest

from pclaude.storage import (
    get_archive_path,
    get_next_id,
    append_prompt,
    read_all,
    search_prompts,
    get_prompt_by_id,
    get_recent_prompts,
)


class TestGetNextId:
    """Tests for get_next_id function."""

    def test_new_file_returns_1(self):
        """New archive file should return ID 1."""
        with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
            path = Path(f.name)
        try:
            assert get_next_id(path) == 1
        finally:
            path.unlink(missing_ok=True)

    def test_after_one_record_returns_2(self):
        """After one record, should return ID 2."""
        with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
            path = Path(f.name)
        try:
            append_prompt(path, {
                "id": "#1",
                "timestamp": "2026-02-08T10:00:00",
                "prompt": "test",
                "source": "one-shot",
                "session_id": None,
            })
            assert get_next_id(path) == 2
        finally:
            path.unlink(missing_ok=True)

    def test_empty_file_returns_1(self):
        """Empty file should return ID 1."""
        with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
            path = Path(f.name)
            f.write(b"")  # Write empty content
        try:
            assert get_next_id(path) == 1
        finally:
            path.unlink(missing_ok=True)


class TestAppendPrompt:
    """Tests for append_prompt function."""

    def test_append_creates_parent_dir(self, tmp_path):
        """Append should create parent directory if needed."""
        path = tmp_path / "new_dir" / "prompts.jsonl"
        assert not path.parent.exists()
        append_prompt(path, {
            "id": "#1",
            "timestamp": "2026-02-08T10:00:00",
            "prompt": "test",
            "source": "one-shot",
            "session_id": None,
        })
        assert path.exists()

    def test_append_writes_valid_jsonl(self, tmp_path):
        """Append should write valid JSONL."""
        path = tmp_path / "prompts.jsonl"
        append_prompt(path, {
            "id": "#1",
            "timestamp": "2026-02-08T10:00:00",
            "prompt": "hello world",
            "source": "one-shot",
            "session_id": None,
        })
        with open(path, "r", encoding="utf-8") as f:
            line = f.readline()
        record = json.loads(line)
        assert record["id"] == "#1"
        assert record["prompt"] == "hello world"


class TestReadAll:
    """Tests for read_all function."""

    def test_empty_file_returns_empty_list(self, tmp_path):
        """Empty file should return empty list."""
        path = tmp_path / "empty.jsonl"
        path.touch()
        assert read_all(path) == []

    def test_nonexistent_file_returns_empty_list(self):
        """Non-existent file should return empty list."""
        path = Path("/tmp/nonexistent12345.jsonl")
        assert read_all(path) == []

    def test_read_multiple_records(self, tmp_path):
        """Should read all records correctly."""
        path = tmp_path / "prompts.jsonl"
        records = [
            {"id": "#1", "timestamp": "2026-02-08T10:00:00", "prompt": "test1", "source": "one-shot", "session_id": None},
            {"id": "#2", "timestamp": "2026-02-08T11:00:00", "prompt": "test2", "source": "one-shot", "session_id": None},
        ]
        for r in records:
            append_prompt(path, r)
        result = read_all(path)
        assert len(result) == 2
        assert result[0]["id"] == "#1"
        assert result[1]["id"] == "#2"


class TestSearchPrompts:
    """Tests for search_prompts function."""

    def test_find_exact_match(self, tmp_path):
        """Should find prompt with exact keyword."""
        path = tmp_path / "prompts.jsonl"
        append_prompt(path, {
            "id": "#1",
            "timestamp": "2026-02-08T10:00:00",
            "prompt": "Write a Python script to scrape Amazon",
            "source": "one-shot",
            "session_id": None,
        })
        results = search_prompts(path, "Amazon")
        assert len(results) == 1
        assert "Amazon" in results[0]["prompt"]

    def test_case_insensitive(self, tmp_path):
        """Search should be case insensitive."""
        path = tmp_path / "prompts.jsonl"
        append_prompt(path, {
            "id": "#1",
            "timestamp": "2026-02-08T10:00:00",
            "prompt": "HELLO WORLD",
            "source": "one-shot",
            "session_id": None,
        })
        results = search_prompts(path, "hello")
        assert len(results) == 1

    def test_no_match_returns_empty(self, tmp_path):
        """No match should return empty list."""
        path = tmp_path / "prompts.jsonl"
        append_prompt(path, {
            "id": "#1",
            "timestamp": "2026-02-08T10:00:00",
            "prompt": "test",
            "source": "one-shot",
            "session_id": None,
        })
        results = search_prompts(path, "nonexistent")
        assert results == []


class TestGetPromptById:
    """Tests for get_prompt_by_id function."""

    def test_find_existing_id(self, tmp_path):
        """Should find prompt by ID."""
        path = tmp_path / "prompts.jsonl"
        append_prompt(path, {
            "id": "#123",
            "timestamp": "2026-02-08T10:00:00",
            "prompt": "test prompt",
            "source": "one-shot",
            "session_id": None,
        })
        result = get_prompt_by_id(path, 123)
        assert result is not None
        assert result["prompt"] == "test prompt"

    def test_not_found_returns_none(self, tmp_path):
        """Non-existent ID should return None."""
        path = tmp_path / "prompts.jsonl"
        result = get_prompt_by_id(path, 999)
        assert result is None


class TestGetRecentPrompts:
    """Tests for get_recent_prompts function."""

    def test_limit_results(self, tmp_path):
        """Should return limited results."""
        path = tmp_path / "prompts.jsonl"
        for i in range(5):
            append_prompt(path, {
                "id": f"#{i+1}",
                "timestamp": f"2026-02-08T0{i}:00:00",
                "prompt": f"test {i}",
                "source": "one-shot",
                "session_id": None,
            })
        results = get_recent_prompts(path, 3)
        assert len(results) == 3
        # Should be the most recent (last 3)
        assert results[0]["id"] == "#3"
        assert results[2]["id"] == "#5"

    def test_less_than_limit(self, tmp_path):
        """Should return all if less than limit."""
        path = tmp_path / "prompts.jsonl"
        for i in range(2):
            append_prompt(path, {
                "id": f"#{i+1}",
                "timestamp": f"2026-02-08T0{i}:00:00",
                "prompt": f"test {i}",
                "source": "one-shot",
                "session_id": None,
            })
        results = get_recent_prompts(path, 10)
        assert len(results) == 2
