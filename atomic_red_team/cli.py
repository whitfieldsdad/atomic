
from typing import Optional

import click

from atomic_red_team.client import Client


@click.group()
def cli():
    """
    Atomic Red Team
    """

@cli.group()
def tests():
    pass


@cli.command
def get_tests():
    pass


@cli.command()
def get_test():
    pass


def main():
    cli()


if __name__ == "__main":
    main()
