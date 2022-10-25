from pickle import FALSE
import click
from config import Config
import os
import asyncio
from udp_multicast import Multicast
from socket_adapter import WebServer
from concurrent.futures import ProcessPoolExecutor


async def asyncNetstat(scan, verbose):
    loop = asyncio.get_event_loop()
    executor = ProcessPoolExecutor()

    await asyncio.gather(*[
        asyncio.create_task(WebServer.run()),
        asyncio.create_task(Multicast.cast(scan, verbose)),
    ])


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
def cli():
    """This script showcases different terminal UI helpers in Click."""
    pass


# @cli.command()
@pass_config
def init(config):
    """Creates config.json + dirs for each mac address found. Warns if run in a project dir. User to optionally provide a list of mac addresses (obtained with mariachi status –-netscan)"""
    if os.path.exists('config.ini'):
        click.echo(
            "Config file already exist in this folder. Please move to an empty directory and run mbroker init again.")
    else:
        return FALSE


@cli.command()
def push():
    """Pushes code out."""
    click.echo("push")


@cli.command()
def pull():
    """Pull code in."""
    click.echo("pull")


@cli.command()
@click.option(
    "--scan",
    is_flag=True,
    show_default=True,
    default=False,
    help="Scan for devices not in network."
)
@click.option(
    "--verbose",
    is_flag=True,
    show_default=True,
    default=False,
    help="Verbose output."
)
def netstat(scan, verbose):
    """Pulls status from all network devices."""
    if scan:
        asyncio.run(asyncNetstat(scan, verbose))
    else:
        if init():
            click.echo(
                "Config file does not Exist in this folder. Add option -scan to look for Mariachi devices in your LAN anyway.")
        else:
            asyncio.run(asyncNetstat(scan, verbose))


@cli.command()
def add():
    """Add Mariachi devices."""
    click.echo("add")


@cli.command()
def remove():
    """Remove Mariachi devices."""
    click.echo("remove")


@cli.command()
@click.option(
    "--safe",
    is_flag=True,
    show_default=True,
    default=False,
    help="Reboots in safe mode."
)
def reboot(safe):
    """Reboots device."""
    click.echo("reboot")
    click.echo(safe)
