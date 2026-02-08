"""Core prompt capture logic."""

import subprocess
import sys
from datetime import datetime

from rich.console import Console

from .storage import (
    get_archive_path,
    get_next_id,
    append_prompt,
)
from .utils import extract_prompt_from_args, format_timestamp

console = Console()


def show_save_feedback(prompt_id: int, timestamp: str) -> None:
    """Show save confirmation feedback."""
    ts = format_timestamp(timestamp)
    console.print(f"[SAVED] #{prompt_id} ({ts})")
    console.print(f"[dim]Use: pclaude show {prompt_id}    or    pclaude use {prompt_id}[/dim]")


def capture_and_run(args: list[str]) -> None:
    """Main flow: capture prompt -> save -> forward to claude."""
    archive_path = get_archive_path()

    # 1. Extract prompt text
    prompt_text = extract_prompt_from_args(args)

    # 2. Generate record
    next_id = get_next_id(archive_path)
    record = {
        "id": f"#{next_id}",
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt_text,
        "source": "one-shot",
        "session_id": None,
    }

    # 3. Save
    append_prompt(archive_path, record)

    # 4. Feedback (unless --quiet)
    if "--quiet" not in args:
        show_save_feedback(next_id, record["timestamp"])

    # 5. Forward to claude
    subprocess.run(
        ["claude"] + args,
        shell=False,
        check=False,
    )
