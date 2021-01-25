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

@click.command()
@click.option('-v', '--verbose', count=True)
def run(verbose):

    configure_logging(verbose)

    token = os.getenv('token')
    LootBot.run(token)


if __name__ == '__main__':
    run()
