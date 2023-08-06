"""Defines a command-line interface for ipgdrive."""

import click

import ipgdrive


@click.group()
def cli():
    """Command-line interface for the ipgdrive package."""
    pass


@cli.command(help="Setup the cronjob for ipgdrive.")
# @click.option(
#     '-m', '--minutes', type=int,
#     help="Run frequency in minutes."
# )
def setup_job():
    """Setup the cronjob for ipgdrive."""
    ipgdrive.setup_job()
