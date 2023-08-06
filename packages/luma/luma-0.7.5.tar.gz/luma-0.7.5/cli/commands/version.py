import click

@click.command(help='Show the current version of the CLI.')
def version():
    click.echo("luma 0.7.5")
