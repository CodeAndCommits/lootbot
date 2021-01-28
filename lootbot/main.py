import click
import os
import logging

from .bot import LootBot

logger = logging.getLogger(__name__)


def configure_logging(verbose):
    logging.basicConfig(level={
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG,
    }[min(verbose, 3)])


def run_migrations():
    from alembic import command
    from alembic.config import Config
    from .database import engine

    config = Config(f'{os.getcwd()}/alembic.ini')

    with engine.begin() as connection:
        config.attributes['connection'] = connection
        command.upgrade(config, "head")


@click.command()
@click.option('-v', '--verbose', count=True)
@click.option('-n', '--migrate', is_flag=True)
def run(verbose: int, migrate: bool):
    configure_logging(verbose)

    if migrate:
        run_migrations()

    token = os.getenv('token')
    LootBot.run(token)


if __name__ == '__main__':
    run()
