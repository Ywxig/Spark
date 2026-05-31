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

    # ── Handle local changes
    status_result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True, text=True, cwd=str(script_dir)
    )
    has_changes = bool(status_result.stdout.strip())

    stashed = False
    if has_changes:
        if force:
            y("--force flag set. Discarding local changes...")
            subprocess.run(["git", "checkout", "--", "."], cwd=str(script_dir))
            subprocess.run(["git", "clean", "-fd"], cwd=str(script_dir), capture_output=True)
        else:
            y("Local changes detected. Stashing them temporarily...")
            stash_result = subprocess.run(
                ["git", "stash", "push", "-m", "spark-update-autostash"],
                capture_output=True, text=True, cwd=str(script_dir)
            )
            if stash_result.returncode != 0:
                r("Error: could not stash local changes.")
                r(stash_result.stderr.strip())
                sys.exit(1)
            stashed = True

    # ── Fetch & pull
    g(f"Fetching from {remote}...")
    fetch_result = subprocess.run(
        ["git", "fetch", remote],
        cwd=str(script_dir)
    )
    if fetch_result.returncode != 0:
        r("Error: git fetch failed. Check your internet connection and remote URL.")
        if stashed:
            subprocess.run(["git", "stash", "pop"], cwd=str(script_dir))
        sys.exit(1)

    g(f"Pulling {remote}/{branch}...")
    pull_result = subprocess.run(
        ["git", "pull", remote, branch],
        capture_output=True, text=True, cwd=str(script_dir)
    )
    if pull_result.returncode != 0:
        r("Error: git pull failed.")
        r(pull_result.stderr.strip())
        if stashed:
            y("Restoring stashed changes...")
            subprocess.run(["git", "stash", "pop"], cwd=str(script_dir))
        sys.exit(1)

    pull_output = pull_result.stdout.strip()

    # ── Restore stash
    if stashed:
        y("Restoring stashed local changes...")
        pop_result = subprocess.run(
            ["git", "stash", "pop"],
            capture_output=True, text=True, cwd=str(script_dir)
        )
        if pop_result.returncode != 0:
            y("Warning: stash pop had conflicts. Resolve manually with 'git stash pop'.")

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
    if pull_output == "Already up to date.":
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
    cli()