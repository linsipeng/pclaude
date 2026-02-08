"""Entry point for pclaude CLI."""

import sys

from .cli import app
from .capture import capture_and_run


def main():
    # If no arguments, show help
    if len(sys.argv) < 2:
        app(["--help"])
        return

    first_arg = sys.argv[1]

    # Subcommand list
    subcommands = ["ls", "list", "search", "show", "use", "install-alias", "--help", "-h"]

    if first_arg in subcommands or first_arg.startswith("-"):
        # Subcommand or global flag
        app()
    else:
        # Proxy mode: capture and forward
        capture_and_run(sys.argv[1:])


if __name__ == "__main__":
    main()
