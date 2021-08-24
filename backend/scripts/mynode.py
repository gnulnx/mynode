#!/usr/bin/env python
import click
import scripts.docker_cmds as dc
from scripts.groups import mynode


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
