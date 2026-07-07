# cli/command_handler.py
import click
import os
import subprocess
import sys
from pathlib import Path
import webbrowser
from config_loader import ConfigLoader

# ANSI colours
GREEN  = '\033[0;32m'
YELLOW = '\033[1;33m'
RED    = '\033[0;31m'
NC     = '\033[0m'

def g(msg): 
    click.echo(f"{GREEN}{msg}{NC}")

def y(msg): 
    click.echo(f"{YELLOW}{msg}{NC}")

def r(msg): 
    click.echo(f"{RED}{msg}{NC}")

class CommandHandler:
    """Handles all CLI commands for the Spark application."""
    
    def __init__(self, script_dir):
        self.script_dir = Path(script_dir)
        self.venv_dir = self.script_dir / ".venv"
        self.python_bin = self.venv_dir / "bin" / "python"
        self.pip_bin = self.venv_dir / "bin" / "pip"
        self.cfg = ConfigLoader(f"{script_dir}/config.json").load()
        
    def setup(self):
        """Setup virtual environment and install dependencies."""
        if not Path(f"{self.script_dir}/Solutions").is_dir():
            os.mkdir(f"{self.script_dir}/Solutions")
        
        if not Path(f"{self.script_dir}/Migrations").is_dir():
            os.mkdir(f"{self.script_dir}/Migrations")
            
        g("Setup completed successfully!")
        
    def explorer(self, location=None):
        """Open Spark dir in file manager or a specific solution directory."""
        target_location = str(self.script_dir)

        if not Path(f"{self.script_dir}/Solutions").is_dir():
            r("Error: Solutions directory not found.")
            return

        if location is not None:
            target_location = f"{self.script_dir}/Solutions/{location}"
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

    def run_app(self):
        """Launch Flask application (equivalent to spark.sh)."""
        os.chdir(self.script_dir)

        g("=== Start Flask-app ===\n")

        # ── Virtual environment
        if not self.venv_dir.is_dir():
            y(".venv not found. Creating...")
            result = subprocess.run([sys.executable, "-m", "venv", str(self.venv_dir)])
            if result.returncode != 0:
                r("Error: failed to create venv")
                sys.exit(1)

        g("Activating venv...")

        # ── Dependencies
        req = self.script_dir / "requirements.txt"
        if req.is_file():
            g("Checking dependencies...")
            subprocess.run([str(self.pip_bin), "install", "-q", "--upgrade", "pip"])
            result = subprocess.run([str(self.pip_bin), "install", "-q", "-r", str(req)])
            if result.returncode != 0:
                r("Error with installing packages from requirements.txt")
                sys.exit(1)
        else:
            y("File requirements.txt not found!")

        # ── Check main.py
        main_py = self.script_dir / "main.py"
        if not main_py.is_file():
            r("File main.py not found!")
            sys.exit(1)

        env = os.environ.copy()
        env.update({
            "FLASK_APP":   "main.py",
            "FLASK_ENV":   "development", 
            "FLASK_DEBUG": "1",
        })

        # Open browser BEFORE starting server
        start_options = self.cfg["START_OPTIONS"]

        if start_options["open_in_browser"]:
            ip = start_options["host"]
            port = start_options["port"] 
            url = f"http://{ip}:{port}"
            should_open = False

            if not start_options["check_open_in_browser"]:
                should_open = True
            else:
                # Only open if not running as the reloader child process
                if not os.environ.get("WERKZEUG_RUN_MAIN"):
                    should_open = True

            if should_open:
                # Add a small delay to ensure server has time to start
                import threading
                import time

                def open_browser_delayed():
                    time.sleep(2)  # Wait 2 seconds for server to start
                    webbrowser.open(url)

                thread = threading.Thread(target=open_browser_delayed)
                thread.daemon = True
                thread.start()

        # Start the server AFTER browser opening is scheduled
        try:
            proc = subprocess.Popen([str(self.python_bin), str(main_py)], env=env, cwd=str(main_py.parent))
            proc.wait()
        except KeyboardInterrupt:
            g("Application stopped.")

    def update(self, branch="master", force=False):
        """Pull latest updates from the remote GitHub repository."""
        from config_loader import ConfigLoader
        
        os.chdir(self.script_dir)

        g("=== Spark Update ===\n")

        # ── Check git is available
        if subprocess.run(["git", "--version"], capture_output=True).returncode != 0:
            r("Error: git is not installed or not in PATH.")
            sys.exit(1)

        # ── Check this is a git repo
        if not (self.script_dir / ".git").is_dir():
            r("Error: this directory is not a git repository.")
            r(f"Run 'git init' and add a remote, or clone the repo into: {self.script_dir}")
            sys.exit(1)

        # ── Determine remote
        remote_result = subprocess.run(
            ["git", "remote"],
            capture_output=True, text=True, cwd=str(self.script_dir)
        )
        remotes = remote_result.stdout.strip().splitlines()
        if not remotes:
            r("Error: no git remote configured.")
            r("Add one with: git remote add origin https://github.com/user/repo.git")
            sys.exit(1)
        remote = "origin" if "origin" in remotes else remotes[0]

        y(f"Remote : {remote}")
        y(f"Branch : {branch}\n")

        # ── Load config to save version before update
        CFG = ConfigLoader(f"{self.script_dir}/config.json").load()
        version_before = CFG.get("VERSION", "unknown")

        # ── Capture current HEAD hash to detect changes later
        head_before = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, cwd=str(self.script_dir)
        ).stdout.strip()

        # ── Check if repo has any commits yet
        has_commits = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, cwd=str(self.script_dir)
        ).returncode == 0

        # ── Fetch
        g(f"Fetching from {remote}...")
        fetch_result = subprocess.run(
            ["git", "fetch", remote],
            cwd=str(self.script_dir)
        )
        if fetch_result.returncode != 0:
            r("Error: git fetch failed. Check your internet connection and remote URL.")
            sys.exit(1)

        # ── Reset to remote (discards local changes cleanly without needing index write)
        g(f"Applying {remote}/{branch}...")
        reset_result = subprocess.run(
            ["git", "reset", "--hard", f"{remote}/{branch}"],
            capture_output=True, text=True, cwd=str(self.script_dir)
        )
        if reset_result.returncode != 0:
            r("Error: git reset failed.")
            r(reset_result.stderr.strip())
            sys.exit(1)

        # ── Remove untracked files
        subprocess.run(["git", "clean", "-fd"], capture_output=True, cwd=str(self.script_dir))

        pull_output = reset_result.stdout.strip()

        # ── Re-install dependencies if requirements.txt changed
        req = self.script_dir / "requirements.txt"
        if "requirements.txt" in pull_output and req.is_file():
            if self.pip_bin.is_file():
                y("requirements.txt changed — updating dependencies...")
                subprocess.run([str(self.pip_bin), "install", "-q", "--upgrade", "pip"])
                result = subprocess.run([str(self.pip_bin), "install", "-q", "-r", str(req)])
                if result.returncode != 0:
                    r("Warning: some dependencies failed to install.")

        # ── Report result
        # Compare HEAD before/after to detect if anything changed
        head_after = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, cwd=str(self.script_dir)
        ).stdout.strip()

        if pull_output == "Already up to date." or (has_commits and head_before == head_after):
            g("Already up to date. No changes pulled.")
        else:
            # Reload config to get new version
            try:
                new_cfg = ConfigLoader(f"{self.script_dir}/config.json").load()
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
                capture_output=True, text=True, cwd=str(self.script_dir)
            )
            if log_result.stdout.strip():
                g("\nWhat's new:")
                for line in log_result.stdout.strip().splitlines():
                    click.echo(f"  • {line}")

        click.echo()
