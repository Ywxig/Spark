# run.py (updated part)
import click
import os
from pathlib import Path

from src.Solution_Manager.template import Template

from cli.command_handler import CommandHandler, g, y, r
from config_loader import ConfigLoader
LOCATION_OF_SCRIPT = os.path.dirname(os.path.realpath(__file__))
CFG = ConfigLoader(f"{LOCATION_OF_SCRIPT}/config.json").load()

# Create command handler instance
cmd_handler = CommandHandler(LOCATION_OF_SCRIPT)

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Spark — Flask application launch utility."""
    # If no command is specified — run 'version' by default
    if ctx.invoked_subcommand is None:
        ctx.invoke(version)
        print(Template.index())
        try:
            os.rmdir("test")
            template = Template("python_cli.json")
            template.create(
                name="test",
                description="test",
                readme="test",
                origin="test"
            )
        except Exception as e:
            print(f"Error: {e}")


@cli.command()
def setup():
    """
        Setup virtual environment and install dependencies.
        Check for all directories and files. like Solution and Migration
        and create them if they don't exist.
    """
    cmd_handler.setup()

@cli.command()
@click.argument('location', required=False, default=None)
def explorer(location):
    """
        Open Spark dir in file manager.
        Or open a specific solution directory.
    """
    cmd_handler.explorer(location)

@cli.command()
def run():
    """Launch Flask application (equivalent to spark.sh)."""
    cmd_handler.run_app()

@cli.command()
def version():
    y(CFG["VERSION"])

@cli.command()
@click.option("--branch", default="master", help="Branch to pull from (default: master).")
@click.option("--force", is_flag=True, default=False, help="Discard local changes before updating.")
def update(branch, force):
    """Pull latest updates from the remote GitHub repository."""
    cmd_handler.update(branch, force)

if __name__ == "__main__":
    # Check if Solutions and Migrations directories exist
    if not Path(f"{LOCATION_OF_SCRIPT}/Solutions").is_dir():
        r("Error: Solutions directory does not exist.")
        os.mkdir(f"{LOCATION_OF_SCRIPT}/Solutions")

    # Check if migrations directory exists
    if not Path(f"{LOCATION_OF_SCRIPT}/Migrations").is_dir():
        r("Error: Migrations directory does not exist.")
        os.mkdir(f"{LOCATION_OF_SCRIPT}/Migrations")
    
    # Start the CLI    
    cli()