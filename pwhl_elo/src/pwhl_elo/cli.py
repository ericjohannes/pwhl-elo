import click

from pwhl_elo.calculate_elo import handle
from pwhl_elo.chart_elos import create_charts
from pwhl_elo.revert_elo import revert_elo_file
from pwhl_elo.upcoming_projection import build_upcoming_projects


@click.group()
def cli():
    pass


@click.command()
def hi():
    """Example script."""
    click.echo("Hello World!")


@click.command()
def calculate():
    """Calulcates Elos."""
    handle()


@click.command()
def projections():
    """Builds projections for next 5 fixtures."""
    build_upcoming_projects()


@click.command()
def chart():
    """Creates Elo chart for all teams and seasons."""
    create_charts()


@click.command()
@click.option(
    "--input", prompt="path/to/file.json", help="File of team Elos to revert to the mean."
)
@click.option(
    "--output-dir", prompt="path/to/dir", help="Directory of where to save reverted Elos."
)
def revert(input, output_dir):
    """Reverts all latest team Elo's to the mean for the start of a new season."""
    new_file = revert_elo_file(input, output_dir)
    click.echo(f"Save new file: {new_file}")


cli.add_command(hi)
cli.add_command(calculate)
cli.add_command(projections)
cli.add_command(chart)
cli.add_command(revert)
