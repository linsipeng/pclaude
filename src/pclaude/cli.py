"""CLI subcommands for pclaude."""

import typer
from typing import Optional
from rich.table import Table
from rich.console import Console

from .storage import (
    read_all,
    search_prompts,
    get_prompt_by_id,
    get_recent_prompts,
    get_archive_path,
)
from .utils import extract_time_only, truncate_text

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

    # Forward to claude
    import subprocess
    subprocess.run(
        ["claude", new_prompt],
        shell=False,
        check=False,
    )
