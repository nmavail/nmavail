import asyncio
import importlib.metadata
import sys

import click

from .checker import check_name


@click.command()
@click.argument("name", required=False)
@click.option("--version", "-V", is_flag=True, help="Show version and exit")
def cli(name, version):
    """Nmavail: Cross-domain name availability checker"""
    if version:
        click.echo(f"nmavail version {importlib.metadata.version('nmavail')}")
        sys.exit(0)

    if not name:
        click.echo("Error: NAME is required")
        click.echo("Use 'nmavail --help' for more information")
        sys.exit(1)

    asyncio.run(check_name(name))


def main():
    """Entry point for the nmavail command"""
    cli()


if __name__ == "__main__":
    main()
