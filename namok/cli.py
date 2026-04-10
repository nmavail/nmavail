import asyncio
import importlib.metadata

import click

from .checker import check_name
from .config import config_manager


@click.group(invoke_without_command=True)
@click.option("--version", is_flag=True, help="Show version and exit")
@click.pass_context
def cli(ctx, version):
    """Namok: Cross-domain name availability checker"""
    if version:
        click.echo(f"namok version {importlib.metadata.version('namok')}")
        ctx.exit()
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
@click.argument("name")
def check(name):
    """Check the availability of a name"""
    asyncio.run(check_name(name))


@cli.command()
@click.argument("subcommand", required=False)
@click.pass_context
def help(ctx, subcommand):
    """Show help information"""
    if subcommand and subcommand in ctx.parent.command.commands:
        # 显示特定子命令的帮助
        click.echo(ctx.parent.command.commands[subcommand].get_help(ctx.parent))
    else:
        # 显示主命令帮助
        click.echo(ctx.parent.get_help())


@cli.command(name="set")
@click.argument("key")
@click.argument("value")
def set_config(key, value):
    """Set a configuration value, e.g.: namok set github_token <your_token>"""
    # 去除 Token 两端的空格和换行符
    config_manager.set(key, value.strip())
    click.echo(f"✅ Successfully set {key}")


if __name__ == "__main__":
    cli()
