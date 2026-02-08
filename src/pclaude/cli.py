"""CLI subcommands for pclaude."""

import os
import subprocess
import typer
from datetime import datetime
from pathlib import Path
from typing import Optional
from rich.table import Table
from rich.console import Console

from .storage import (
    read_all,
    search_prompts,
    get_prompt_by_id,
    get_recent_prompts,
    get_archive_path,
    append_prompt,
    get_next_id,
)
from .utils import extract_time_only, truncate_text
from .capture import get_claude_command, should_use_shell

app = typer.Typer()
console = Console()


@app.command()
def ls(
    recent: int = typer.Option(10, "--recent", "-n", help="Show recent N prompts"),
    all: bool = typer.Option(False, "--all", help="Show all prompts"),
):
    """List recent prompts."""
    archive_path = get_archive_path()

    if all:
        records = read_all(archive_path)
    else:
        records = get_recent_prompts(archive_path, recent)

    if not records:
        console.print("[dim]No prompts saved yet.[/dim]")
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("ID", width=6, style="cyan")
    table.add_column("Time", width=6)
    table.add_column("Prompt", width=50)

    for record in records:
        record_id = record["id"]
        time_str = extract_time_only(record["timestamp"])
        prompt_preview = truncate_text(record["prompt"], 45)
        table.add_row(record_id, time_str, prompt_preview)

    console.print(table)


@app.command()
def search(keyword: str):
    """Search prompts by keyword."""
    archive_path = get_archive_path()
    results = search_prompts(archive_path, keyword)

    if not results:
        console.print(f"[dim]No matches found for '{keyword}'[/dim]")
        return

    console.print(f"[bold]Found {len(results)} match(es):[/bold]\n")

    for record in results[:10]:  # Limit to 10 results
        console.print(f"[cyan]{record['id']}[/cyan]  {record['timestamp'][:19]}")
        console.print(f"  {truncate_text(record['prompt'], 60)}")
        console.print()


@app.command()
def show(id: int):
    """Show full prompt content."""
    archive_path = get_archive_path()
    record = get_prompt_by_id(archive_path, id)

    if not record:
        console.print(f"[red]Prompt #{id} not found[/red]")
        raise typer.Exit(1)

    console.print(f"[cyan]{record['id']}[/cyan]  {record['timestamp'][:19]}")
    console.print()
    console.print(record["prompt"])


@app.command()
def use(id: int, append: Optional[str] = typer.Argument(None, help="Additional instructions")):
    """Reuse a prompt, optionally with additional instructions."""
    archive_path = get_archive_path()
    record = get_prompt_by_id(archive_path, id)

    if not record:
        console.print(f"[red]Prompt #{id} not found[/red]")
        raise typer.Exit(1)

    # Build the new prompt
    new_prompt = record["prompt"]
    if append:
        new_prompt = f"{new_prompt} {append}"

    # Save the new prompt as a new record
    next_id = get_next_id(archive_path)
    new_record = {
        "id": f"#{next_id}",
        "timestamp": datetime.now().isoformat(),
        "prompt": new_prompt,
        "source": "one-shot",
        "session_id": None,
    }
    append_prompt(archive_path, new_record)

    # Show save feedback
    console.print(f"[SAVED] #{next_id} ({new_record['timestamp'][:19]})")
    console.print(f"[dim]Use: pclaude show {next_id}    or    pclaude use {next_id}[/dim]")

    # Forward to claude
    claude_cmd = get_claude_command()
    subprocess.run(
        claude_cmd + [new_prompt],
        shell=should_use_shell(),
        check=False,
    )


@app.command()
def install_alias():
    """Install 'claude' alias for automatic prompt capture."""
    import platform
    import shutil

    console.print("[bold]pclaude Alias Installer[/bold]\n")
    console.print("This will replace 'claude' command with pclaude.")
    console.print("All prompts will be automatically captured.\n")

    pclaude_path = shutil.which("pclaude") or "pclaude"

    if platform.system() == "Windows":
        # Windows PowerShell
        profile_path = Path.home() / "Documents" / "PowerShell" / "Microsoft.PowerShell_profile.ps1"

        if not profile_path.exists():
            profile_path.parent.mkdir(parents=True, exist_ok=True)
            profile_path.touch()

        content = profile_path.read_text()
        alias_line = 'Set-Alias -Name claude -Value "pclaude"'

        if alias_line in content:
            console.print("[green]Alias already installed.[/green]")
        else:
            with open(profile_path, "a", encoding="utf-8") as f:
                f.write(f"\n# pclaude - Automatic prompt capture\n")
                f.write(f"{alias_line}\n")
            console.print(f"[green]Added alias to {profile_path}[/green]")
            console.print("\n[bold]To activate, run:[/bold]")
            console.print("  . $PROFILE")
    else:
        # Unix-like (bash, zsh)
        shell = os.environ.get("SHELL", "")
        if "zsh" in shell:
            config_path = Path.home() / ".zshrc"
        else:
            config_path = Path.home() / ".bashrc"

        alias_line = f'alias claude="pclaude"'

        if config_path.exists() and alias_line in config_path.read_text():
            console.print("[green]Alias already installed.[/green]")
        else:
            with open(config_path, "a", encoding="utf-8") as f:
                f.write(f"\n# pclaude - Automatic prompt capture\n")
                f.write(f"{alias_line}\n")
            console.print(f"[green]Added alias to {config_path}[/green]")
            console.print("\n[bold]To activate, run:[/bold]")
            console.print("  source ~/.bashrc  # or ~/.zshrc")

    console.print("\n[dim]After activation, 'claude' command will auto-capture prompts.[/dim]")
