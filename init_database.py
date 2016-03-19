import click
from easyris.utils import database_setup


@click.command()
@click.option('--db_name', default='easyris', help='Indicate the name of the database (default=easyris)')
@click.option('--port', default=27017, help='The port with the database service (default=27017)')
def init_database(db_name, port):
    """Simple program that greets NAME for a total of COUNT times."""
    database_setup.run(db_name, port)
    # TODO: save config to file


if __name__ == '__main__':
    init_database()