import asyncio
import importlib.metadata
import sys

import click

from .checker import check_name


@click.command()
@click.argument("name", required=False)
@click.option("--version", "-V", is_flag=True, help="Show version and exit")
@click.option("--help", "-H", is_flag=True, help="Show this message and exit")
def cli(name, version, help_flag):
    """Nmck: Cross-domain name availability checker"""
    if version:
        click.echo(f"nmck version {importlib.metadata.version('nmck')}")
        sys.exit(0)

    if help_flag:
        click.echo("Usage: nmck [OPTIONS] NAME")
        click.echo()
        click.echo("Nmck: Cross-domain name availability checker")
        click.echo()
        click.echo("Options:")
        click.echo("  -V, --version  Show version and exit")
        click.echo("  -H, --help     Show this message and exit")
        click.echo()
        click.echo("Examples:")
        click.echo("  nmck test")
        click.echo("  nmck google")
        click.echo("  nmck myproject")
        sys.exit(0)

    if not name:
        click.echo("Error: NAME is required")
        click.echo("Use 'nmck --help' for more information")
        sys.exit(1)

    asyncio.run(check_name(name))


def main():
    """Entry point for the nmck command"""
    cli()


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
