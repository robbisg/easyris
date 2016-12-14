import click
from easyris.utils import database_setup
import os

@click.command()
@click.option('--db_config', default='config/database.cfg')
#@click.option('--port', default=27017, help='The port with the database service (default=27017)')
def init_database(db_config):
    """Initialize the database using a db_name and a port"""
    database_setup.run(db_config)



if __name__ == '__main__':
    init_database()