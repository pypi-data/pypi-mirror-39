import click

from .database import database
from .dataset import dataset

@click.group()
def cli():
    # CLI Entrypoint
    pass

cli.add_command(database)
cli.add_command(dataset)

cli()