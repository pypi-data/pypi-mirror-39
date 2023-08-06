# -*- coding: utf-8 -*-

"""Console script for polr."""
import sys

import click

from .polr import Polr
from . import utils
from . import settings


_client = None


def get_client():
    global _client
    if _client is None:
        _client = Polr(settings.POLR_URL, settings.POLR_API_KEY)
    return _client


@click.group()
def polr(args=None):
    """
    Console script for polr.
    """
    return 0


SHORTEN_HELP_STR = "Return an error if a link with the desired customending already exists"


@polr.command(name="shorten")
@click.argument("url")
@click.option("-e", "--ending", "ending", help="A custom ending for the shortened link.")
@click.option("-f", "--fail", "raise_on_exists", is_flag=True, help=SHORTEN_HELP_STR)
def shorten(url, ending="", raise_on_exists=False):
    """
    Shorten a link with the option to give it a custom ending. Checks to see if a link with
    the given ending exists. Can be configured to fail if it already exists with [-f|--fail].

    Usage:

        jinc go shorten URL [(-e|--ending=)ending] [(-f|--fail)]

    Examples:

        \b
        # Use default ending
        $ polr shorten https://example.com
        http://go/ad14gfwe

        \b
        # Use custom ending, if ending already exists don't return error, return link with that ending.
        $ polr shorten https://example.com -e my-custom-ending
        http://go/my-custom-ending

        \b
        # Use custom ending, return error if it already exists.
        polr shorten https://example.com -e my-custom-ending -f

    """
    client = get_client()
    try:
        shortened = client.shorten(url, ending=ending, raise_on_exists=raise_on_exists)
        click.echo(shortened)
    except client.ShortenerException as err:
        utils.print_error_and_exit(f"{err}")


@polr.command(name="shorten-bulk")
@click.argument("links")
def shorten_bulk(links):
    client = get_client()
    try:
        shortened = client.shorten_bulk(links)
        click.echo(shortened)
    except client.DuplicateEndingException as err:
        utils.print_error_and_exit(f"{err}")


@polr.command(name="exists", help="Check to see if a link with the given ending already exists.")
@click.argument("ending")
def exists(ending):
    client = get_client()
    exists = client.exists(ending)
    utils.print_and_exit(exists, code=int(exists))


@polr.command(name="lookup")
@click.argument("ending")
def lookup(ending):
    client = get_client()
    try:
        data = client.lookup(ending)
        utils.print_and_exit(data, code=0)
    except client.ShortenerException as err:
        utils.print_error_and_exit(f"{err}")


@polr.command(name="data")
@click.argument("ending")
def data(ending):
    client = get_client()
    try:
        data = client.data(ending)
        utils.print_and_exit(data, code=0)
    except client.ShortenerException as err:
        utils.print_error_and_exit(f"{err}")


if __name__ == "__main__":
    sys.exit(polr())  # pragma: no cover
