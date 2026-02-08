#!/usr/bin/env python3
"""Mock claude CLI for testing pclaude."""

import sys
import json
from datetime import datetime

def main():
    print("=" * 60)
    print("Claude (mock)")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Args: {sys.argv[1:]}")
    print()
    print(f"Received prompt: {sys.argv[1] if len(sys.argv) > 1 else '(none)'}")
    print()
    print("I'm a mock Claude response. In real usage, this would be the")
    print("actual Claude Code CLI output.")
    print("=" * 60)

if __name__ == "__main__":
    main()
