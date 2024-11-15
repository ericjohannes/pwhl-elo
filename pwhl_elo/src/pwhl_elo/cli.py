import click
from pwhl_elo.calculate_elo import handle
from pwhl_elo.upcoming_projection import build_upcoming_projects
from pwhl_elo.chart_elos import create_charts

@click.group()
def cli():
    pass


@click.command()
def hi():
    """Example script."""
    click.echo('Hello World!')


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


cli.add_command(hi)
cli.add_command(calculate)
cli.add_command(projections)
cli.add_command(chart)
