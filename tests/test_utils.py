"""Unit tests for utils module."""

from pclaude.utils import (
    format_timestamp,
    extract_time_only,
    extract_prompt_from_args,
    truncate_text,
)


class TestFormatTimestamp:
    """Tests for format_timestamp function."""

    def test_basic_format(self):
        """Should format timestamp correctly."""
        ts = "2026-02-08T10:30:45"
        result = format_timestamp(ts)
        assert "2026-02-08" in result
        assert "10:30:45" in result


class TestExtractTimeOnly:
    """Tests for extract_time_only function."""

    def test_extract_hh_mm(self):
        """Should extract HH:MM only."""
        ts = "2026-02-08T14:30:45"
        result = extract_time_only(ts)
        assert result == "14:30"


class TestExtractPromptFromArgs:
    """Tests for extract_prompt_from_args function."""

    def test_simple_prompt(self):
        """Should extract simple prompt."""
        args = ["hello world"]
        result = extract_prompt_from_args(args)
        assert result == "hello world"

    def test_with_flags(self):
        """Should ignore flags and extract prompt."""
        args = ["-p", "test prompt", "--option", "value"]
        result = extract_prompt_from_args(args)
        assert result == "test prompt value"

    def test_multiple_args(self):
        """Should join multiple non-flag args."""
        args = ["arg1", "arg2", "arg3"]
        result = extract_prompt_from_args(args)
        assert result == "arg1 arg2 arg3"

    def test_only_flags(self):
        """Should return empty if only flags."""
        args = ["--flag1", "--flag2"]
        result = extract_prompt_from_args(args)
        assert result == ""

    def test_empty_list(self):
        """Should return empty for empty list."""
        args = []
        result = extract_prompt_from_args(args)
        assert result == ""


class TestTruncateText:
    """Tests for truncate_text function."""

    def test_under_limit(self):
        """Should not truncate short text."""
        text = "hello"
        result = truncate_text(text, 10)
        assert result == "hello"

    def test_over_limit(self):
        """Should truncate with ellipsis."""
        text = "hello world this is long"
        result = truncate_text(text, 10)
        assert len(result) == 10
        assert result.endswith("...")

    def test_exact_limit(self):
        """Should not truncate exact limit."""
        text = "hello"
        result = truncate_text(text, 5)
        assert result == "hello"
