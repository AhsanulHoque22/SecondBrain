"""Runs a shell command in build/, then renders a terminal-style screenshot
of the exact prompt + output using render_terminal.render().
"""
import subprocess
import sys
from render_terminal import render


def shot(title: str, command: str, out_path: str, before: list[str] | None = None):
    lines = list(before or [])
    lines.append(f"$ {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = (result.stdout + result.stderr).rstrip("\n")
    lines += output.split("\n") if output else []
    render(title, lines, out_path)
    return result.returncode


if __name__ == "__main__":
    title, command, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    sys.exit(shot(title, command, out_path))
