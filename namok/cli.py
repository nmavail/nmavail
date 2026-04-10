import asyncio

import click

from .checker import check_name
from .config import config_manager


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Namok: 全领域名字可用性检查器"""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
@click.argument("name")
def check(name):
    """检查单个名字的可用性"""
    asyncio.run(check_name(name))


@cli.command(name="set")
@click.argument("key")
@click.argument("value")
def set_config(key, value):
    """设置配置项，例如: namok set github_token <your_token>"""
    # 去除 Token 两端的空格和换行符
    config_manager.set(key, value.strip())
    click.echo(f"✅ Successfully set {key}")


@cli.command(name="get")
@click.argument("key")
def get_config(key):
    """获取配置项的值"""
    val = config_manager.get(key)
    if val:
        # 为了安全，如果是 token 则只显示前几位
        if "token" in key.lower():
            click.echo(f"{key}: {val[:4]}... (hidden)")
        else:
            click.echo(f"{key}: {val}")
    else:
        click.echo(f"{key} is not set")


if __name__ == "__main__":
    cli()
