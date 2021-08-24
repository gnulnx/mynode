import click


@click.group()
@click.version_option()
@click.pass_context
def mynode(ctx):
    pass
