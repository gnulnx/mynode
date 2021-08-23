#!/usr/bin/env python
import click
import scripts.docker_cmds as dc


@click.group()
@click.version_option()
@click.pass_context
def mynode(ctx):
    pass


@mynode.command()
def init():
    dc.init()


@mynode.command()
def up():
    dc.up()


@mynode.command()
def stop():
    dc.stop()


@mynode.command()
def rebuild():
    dc.stop()
    dc.remove()
    dc.init()


@mynode.command()
def status():
    dc.status()


if __name__ == "__main__":
    mynode()
