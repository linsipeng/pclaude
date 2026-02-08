"""Utility functions for pclaude."""

from datetime import datetime
from typing import List


def format_timestamp(ts: str) -> str:
    """Convert ISO 8601 to readable format."""
    dt = datetime.fromisoformat(ts)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def extract_time_only(ts: str) -> str:
    """Extract time only (for ls compact display)."""
    dt = datetime.fromisoformat(ts)
    return dt.strftime("%H:%M")


def extract_prompt_from_args(args: List[str]) -> str:
    """Extract user prompt text from command line arguments.

    Args:
        args: List of command line arguments

    Returns:
        The extracted prompt text (non-flag arguments joined with space)
    """
    # Filter out flags (arguments starting with -)
    prompt_parts = [arg for arg in args if not arg.startswith("-")]
    return " ".join(prompt_parts)


def truncate_text(text: str, max_length: int = 40) -> str:
    """Truncate text with ellipsis for compact display."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."
