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
def setup():
    """
        Setup virtual environment and install dependencies.
        Check for all directories and files. like Solution and Migration
        and create them if they don't exist.
    """

    if not Path(f"{LOACTION_OF_SKRIPT}/Solutions").is_dir():
        os.mkdir(f"{LOACTION_OF_SKRIPT}/Solutions")
    
    if not Path(f"{LOACTION_OF_SKRIPT}/Migrations").is_dir():
        os.mkdir(f"{LOACTION_OF_SKRIPT}/Migrations")

@cli.command()
@click.argument('location', required=False, default=None)
def explorer(location):
    """
        Open Spark dir in file manager.
        Or open a specific solution directory.
    """

    target_location = LOACTION_OF_SKRIPT

    if not Path(f"{LOACTION_OF_SKRIPT}/Solutions").is_dir():
        r("Error: Solutions directory not found.")
        return

    if location is not None:
        target_location = f"{LOACTION_OF_SKRIPT}/Solutions/{location}"
        if not Path(target_location).exists():
            r(f"Error: Location '{location}' not found.")
            return

    try:
        if sys.platform == "linux":
            subprocess.Popen(["xdg-open", str(target_location)])
        elif sys.platform == "win32":
            os.startfile(str(target_location))
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(target_location)])
        else:
            r(f"Error: Unsupported platform '{sys.platform}'.")
    except Exception as e:
        r(f"Error opening directory: {str(e)}")

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

    env = os.environ.copy()
    env.update({
        "FLASK_APP":   "main.py",
        "FLASK_ENV":   "development",
        "FLASK_DEBUG": "1",
    })

    proc = None
    try:
        proc = subprocess.Popen([str(python_bin), str(main_py)], env=env, cwd=str(main_py.parent))
        proc.wait()
    except KeyboardInterrupt:
        if proc and proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()
        g("\nApplication stopped.")

@cli.command()
def version():
    y(CFG["VERSION"])


@cli.command()
@click.option("--branch", default="master", help="Branch to pull from (default: master).")
@click.option("--force", is_flag=True, default=False, help="Discard local changes before updating.")
def update(branch, force):
    """Pull latest updates from the remote GitHub repository."""
    script_dir = Path(__file__).parent.resolve()
    os.chdir(script_dir)

    g("=== Spark Update ===\n")

    # ── Check git is available
    if subprocess.run(["git", "--version"], capture_output=True).returncode != 0:
        r("Error: git is not installed or not in PATH.")
        sys.exit(1)

    # ── Check this is a git repo
    if not (script_dir / ".git").is_dir():
        r("Error: this directory is not a git repository.")
        r(f"Run 'git init' and add a remote, or clone the repo into: {script_dir}")
        sys.exit(1)

    # ── Determine remote
    remote_result = subprocess.run(
        ["git", "remote"],
        capture_output=True, text=True, cwd=str(script_dir)
    )
    remotes = remote_result.stdout.strip().splitlines()
    if not remotes:
        r("Error: no git remote configured.")
        r("Add one with: git remote add origin https://github.com/user/repo.git")
        sys.exit(1)
    remote = "origin" if "origin" in remotes else remotes[0]

    y(f"Remote : {remote}")
    y(f"Branch : {branch}\n")

    # ── Save local version before update
    version_before = CFG.get("VERSION", "unknown")

    # ── Capture current HEAD hash to detect changes later
    head_before = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True, text=True, cwd=str(script_dir)
    ).stdout.strip()


    # ── Check if repo has any commits yet
    has_commits = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True, cwd=str(script_dir)
    ).returncode == 0

    # ── Fetch
    g(f"Fetching from {remote}...")
    fetch_result = subprocess.run(
        ["git", "fetch", remote],
        cwd=str(script_dir)
    )
    if fetch_result.returncode != 0:
        r("Error: git fetch failed. Check your internet connection and remote URL.")
        sys.exit(1)

    # ── Reset to remote (discards local changes cleanly without needing index write)
    g(f"Applying {remote}/{branch}...")
    reset_result = subprocess.run(
        ["git", "reset", "--hard", f"{remote}/{branch}"],
        capture_output=True, text=True, cwd=str(script_dir)
    )
    if reset_result.returncode != 0:
        r("Error: git reset failed.")
        r(reset_result.stderr.strip())
        sys.exit(1)

    # ── Remove untracked files
    subprocess.run(["git", "clean", "-fd"], capture_output=True, cwd=str(script_dir))

    pull_output = reset_result.stdout.strip()

    # ── Re-install dependencies if requirements.txt changed
    req = script_dir / "requirements.txt"
    if "requirements.txt" in pull_output and req.is_file():
        venv_dir = script_dir / ".venv"
        pip_bin  = venv_dir / "bin" / "pip"
        if pip_bin.is_file():
            y("requirements.txt changed — updating dependencies...")
            subprocess.run([str(pip_bin), "install", "-q", "--upgrade", "pip"])
            result = subprocess.run([str(pip_bin), "install", "-q", "-r", str(req)])
            if result.returncode != 0:
                r("Warning: some dependencies failed to install.")

    # ── Report result
    # Compare HEAD before/after to detect if anything changed
    head_after = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True, text=True, cwd=str(script_dir)
    ).stdout.strip()

    if pull_output == "Already up to date." or (has_commits and head_before == head_after):
        g("Already up to date. No changes pulled.")
    else:
        # Reload config to get new version
        try:
            new_cfg = ConfigLoader(f"{script_dir}/config.json").load()
            version_after = new_cfg.get("VERSION", "unknown")
        except Exception:
            version_after = "unknown"

        g("\n=== Update complete ===\n")
        if version_before != version_after:
            y(f"Version: {version_before}  →  {version_after}")
        else:
            y(f"Version: {version_after}")

        # Show a compact changelog (last commits pulled)
        log_result = subprocess.run(
            ["git", "log", "--oneline", "-10", f"HEAD@{{1}}..HEAD"],
            capture_output=True, text=True, cwd=str(script_dir)
        )
        if log_result.stdout.strip():
            g("\nWhat's new:")
            for line in log_result.stdout.strip().splitlines():
                click.echo(f"  • {line}")

    click.echo()


if __name__ == "__main__":
    # Check if Solutions and Migrations directories exist
    # #solutions and migrations
    # Solutions/*
    # Migrations/*

    if not Path(f"{LOACTION_OF_SKRIPT}/Solutions").is_dir():
        r("Error: Solutions directory does not exist.")
        os.mkdir(f"{LOACTION_OF_SKRIPT}/Solutions")

    # Check if migrations directory exists
    if not Path(f"{LOACTION_OF_SKRIPT}/Migrations").is_dir():
        r("Error: Migrations directory does not exist.")
        os.mkdir(f"{LOACTION_OF_SKRIPT}/Migrations")
    
    # Start the CLI    
    cli()