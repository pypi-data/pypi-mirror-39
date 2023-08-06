# -*- coding: utf-8 -*-

"""Console script for trialbureautools."""
import sys
import click

from trialbureautools import PERMISSIONS


@click.group()
def cli():
    pass


@click.command()
@click.argument('folder', type=click.Path(exists=True, resolve_path=True))
@click.argument('permissions', type=click.Choice([list(PERMISSIONS.keys())]))
def set_folder_permissions(folder, permissions):
    print(f"setting folder'{folder}' permissions to {permissions}")


@click.command()
def say_hello():
    print("Hello")


cli.add_command(set_folder_permissions)
cli.add_command(say_hello)

if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
