#!/usr/bin/env python3
"""
Install pclaude as claude alias for automatic prompt capture.

This script replaces the 'claude' command with pclaude wrapper,
so all prompts are automatically captured without user action.

Usage:
    python install_alias.py
"""

import os
import sys
import shutil
from pathlib import Path

def get_shell_config():
    """Detect shell and return config file path."""
    home = Path.home()

    if sys.platform == "win32":
        # Windows PowerShell
        return home / "Documents" / "PowerShell" / "Microsoft.PowerShell_profile.ps1"
    else:
        # Unix-like shells
        shell = os.environ.get("SHELL", "")
        if "zsh" in shell:
            return home / ".zshrc"
        elif "bash" in shell:
            return home / ".bashrc"
        else:
            # Default to bash
            return home / ".bashrc"


def get_pclaude_path():
    """Get the path to pclaude command."""
    try:
        import shutil
        return shutil.which("pclaude") or "pclaude"
    except:
        return "pclaude"


def add_alias_to_file(config_file: Path, alias_line: str):
    """Add alias line to config file if not already present."""
    if not config_file.exists():
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config_file.touch()

    content = config_file.read_text()

    if alias_line in content:
        print(f"Alias already exists in {config_file}")
        return False

    # Add to end of file
    with open(config_file, "a", encoding="utf-8") as f:
        f.write(f"\n# pclaude - Automatic prompt capture\n")
        f.write(f"{alias_line}\n")

    return True


def add_to_powershell_profile():
    """Add to PowerShell profile for Windows."""
    profile_path = get_shell_config()
    alias_line = 'Set-Alias -Name claude -Value "pclaude"'

    if add_alias_to_file(profile_path, alias_line):
        print(f"Added alias to PowerShell profile: {profile_path}")
        print("\nTo activate, run:")
        print("  . $PROFILE")
        print("Or restart your terminal.")


def add_to_bashrc():
    """Add to .bashrc for Linux/macOS/Git Bash."""
    config_path = get_shell_config()
    pclaude_path = get_pclaude_path()
    alias_line = f'alias claude="pclaude"'

    if add_alias_to_file(config_path, alias_line):
        print(f"Added alias to {config_path}")
        print("\nTo activate, run:")
        print("  source ~/.bashrc")
        print("Or restart your terminal.")


def add_to_zshrc():
    """Add to .zshrc for Zsh."""
    config_path = get_shell_config()
    pclaude_path = get_pclaude_path()
    alias_line = f'alias claude="pclaude"'

    if add_alias_to_file(config_path, alias_line):
        print(f"Added alias to {config_path}")
        print("\nTo activate, run:")
        print("  source ~/.zshrc")
        print("Or restart your terminal.")


def main():
    print("=" * 60)
    print("pclaude Alias Installer")
    print("=" * 60)
    print("\nThis script will replace 'claude' command with pclaude,")
    print("so all prompts are automatically captured.\n")

    print("Detecting system...")

    if sys.platform == "win32":
        print("\nDetected: Windows")
        add_to_powershell_profile()
    else:
        shell = os.environ.get("SHELL", "")
        if "zsh" in shell:
            print(f"\nDetected: Zsh ({shell})")
            add_to_zshrc()
        else:
            print(f"\nDetected: Bash/Shell ({shell})")
            add_to_bashrc()

    print("\n" + "=" * 60)
    print("Installation complete!")
    print("=" * 60)
    print("\nIMPORTANT: Restart your terminal or run:")
    if sys.platform == "win32":
        print("  . $PROFILE")
    else:
        print("  source ~/.bashrc  # or ~/.zshrc")
    print("\nThen 'claude' command will automatically capture prompts.")


if __name__ == "__main__":
    main()
