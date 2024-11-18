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


# input for now should be wphl_results_clean_data file
# suggested run like
#  `pwhlelo calculate --input ../data/input/wphl_results_clean_data.csv --output-dir ../data/output`
@click.command()
@click.option("--input", prompt="path/to/file.json", help=".csv file of fixtures with scores.")
@click.option("--output-dir", prompt="path/to/dir", help="Directory of where to save Elos.")
def calculate(input, output_dir):
    """Calulcates Elos and outputs three files:
    1. wphl_elos_<TIMESTAMP>.csv - file with all fixtures played so far with Elos and
    projections calculated.
    2. chartable_wphl_elos.json - file formatted for a chart. Elos for each date for each team.
    3. pwhl_latest_elos - file with latest calculated Elos for each team and date calculated."""
    handle(input, output_dir)


# run like `pwhlelo projections`
@click.command()
def projections():
    """Builds projections for next 5 fixtures based on latest_pwhl_latest_elos.json."""
    build_upcoming_projects()


@click.command()
def chart():
    """Creates Elo chart for all teams and seasons."""
    create_charts()


# suggested run like
# `pwhlelo revert --input ../data/output/pwhl_latest_elos.json --output-dir ../data/output`
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
