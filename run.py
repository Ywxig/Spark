#!/usr/bin/env python3

import click
import os
import subprocess
import sys
from pathlib import Path

LOACTION_OF_SKRIPT = os.path.dirname(os.path.realpath(__file__))
from config_loader import ConfigLoader

CFG = ConfigLoader(f"{LOACTION_OF_SKRIPT}/config.json").load()

# ANSI colours
GREEN  = '\033[0;32m'
YELLOW = '\033[1;33m'
RED    = '\033[0;31m'
NC     = '\033[0m'

def g(msg): click.echo(f"{GREEN}{msg}{NC}")
def y(msg): click.echo(f"{YELLOW}{msg}{NC}")
def r(msg): click.echo(f"{RED}{msg}{NC}")


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Spark — Flask application launch utility."""
    # If no command is specified — run 'run' by default
    if ctx.invoked_subcommand is None:
        ctx.invoke(version)


@cli.command()
def run():
    """Launch Flask application (equivalent to spark.sh)."""
    script_dir = Path(__file__).parent.resolve()
    os.chdir(script_dir)

    g("=== Start Flask-app ===\n")

    venv_dir = script_dir / ".venv"
    python_bin = venv_dir / "bin" / "python"
    pip_bin    = venv_dir / "bin" / "pip"

    # ── Virtual environment
    if not venv_dir.is_dir():
        y(".venv not found. Creating...")
        result = subprocess.run([sys.executable, "-m", "venv", str(venv_dir)])
        if result.returncode != 0:
            r("Error: failed to create venv")
            sys.exit(1)

    g("Activating venv...")

    # ── Dependencies
    req = script_dir / "requirements.txt"
    if req.is_file():
        g("Checking dependencies...")
        subprocess.run([str(pip_bin), "install", "-q", "--upgrade", "pip"])
        result = subprocess.run([str(pip_bin), "install", "-q", "-r", str(req)])
        if result.returncode != 0:
            r("Error with installing packages from requirements.txt")
            sys.exit(1)
    else:
        y("File requirements.txt not found!")

    # ── Check main.py
    main_py = script_dir / "main.py"
    if not main_py.is_file():
        r("File main.py not found!")
        sys.exit(1)

    # ── Launch
    click.clear()
    g("=== App started ===\n")
    y(f"Available at: {CFG["START_OPTIONS"]["host"]}/{CFG["START_OPTIONS"]["port"]}\n")
    y("To stop, press Ctrl+C\n")
    g("=" * 40 + "\n")

    env = os.environ.copy()
    env.update({
        "FLASK_APP":   "main.py",
        "FLASK_ENV":   "development",
        "FLASK_DEBUG": "1",
    })

    try:
        subprocess.run([str(python_bin), str(main_py)], env=env, cwd=str(main_py.parent))
    except KeyboardInterrupt:
        g("\nApplication stopped.")

@cli.command()
def version():
    y(CFG["VERSION"])

if __name__ == "__main__":
    cli()