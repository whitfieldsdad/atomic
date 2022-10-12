import itertools

from typing import Optional

import json
import click

from atomic_red_team.cli.helpers import str_to_strs
from atomic_red_team.client import Client


@click.group()
def cli():
    pass


@cli.command()
@click.argument('test-id', required=True)
def get_test(test_id: str):
    client = Client()
    test = client.get_test(test_id=test_id)
    if test:
        click.echo(json.dumps(test))


@cli.command()
@click.option('--test-ids')
@click.option('--test-names')
@click.option('--technique-ids')
@click.option('--limit', type=int)
def get_tests(test_ids: Optional[str], test_names: Optional[str], technique_ids: Optional[str], limit: Optional[int]):
    client = Client()
    tests = client.iter_tests(
        test_ids=str_to_strs(test_ids),
        test_names=str_to_strs(test_names),
        technique_ids=str_to_strs(technique_ids),
    )
    for test in itertools.islice(tests, limit):
        txt = json.dumps(test)
        click.echo(txt)


@cli.command()
@click.option('--test-ids')
@click.option('--test-names')
@click.option('--technique-ids')
def count_tests(test_ids: Optional[str], test_names: Optional[str], technique_ids: Optional[str]):
    client = Client()
    total = client.count_tests(
        test_ids=str_to_strs(test_ids),
        test_names=str_to_strs(test_names),
        technique_ids=str_to_strs(technique_ids),
    )
    click.echo(total)


@cli.command()
@click.option('--technique-ids')
def get_test_paths(technique_ids: Optional[str]):
    client = Client()
    for path in client.iter_test_paths(
        technique_ids=str_to_strs(technique_ids),
    ):
        click.echo(path)


def main():
    cli()


if __name__ == "__main":
    main()
