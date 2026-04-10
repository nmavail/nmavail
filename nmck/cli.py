import asyncio
import importlib.metadata

import click

from .checker import check_name
from .config import config_manager


@click.group(invoke_without_command=True)
@click.option("--version", is_flag=True, help="Show version and exit")
@click.pass_context
def cli(ctx, version):
    """Nmck: Cross-domain name availability checker"""
    if version:
        click.echo(f"nmck version {importlib.metadata.version('nmck')}")
        ctx.exit()
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
@click.argument("name")
def check(name):
    """Check the availability of a name. Note: GitHub/GitLab tokens are required for complete repo search results."""
    asyncio.run(check_name(name))


@cli.command()
@click.argument("subcommand", required=False)
@click.pass_context
def help(ctx, subcommand):  # noqa: A001
    """Show help information"""
    if subcommand and subcommand in ctx.parent.command.commands:
        # Show help for specific subcommand
        cmd = ctx.parent.command.commands[subcommand]
        args = " ".join(
            [
                a.name.upper()
                for a in cmd.params
                if isinstance(a, click.Argument) and a.name
            ]
        )
        click.echo(f"Usage: nmck {subcommand} {args}")
        click.echo()
        click.echo(f"  {cmd.help}")
    else:
        # Show main command help
        click.echo(ctx.parent.get_help())


@cli.command(name="set")
@click.argument("key")
@click.argument("value")
def set_config(key, value):
    """Set a configuration value (e.g., github_token or gitlab_token). Required for full GitHub/GitLab functionality."""
    # Remove leading/trailing whitespace and newlines from token
    config_manager.set(key, value.strip())
    click.echo(f"✅ Successfully set {key}")


if __name__ == "__main__":
    cli()
