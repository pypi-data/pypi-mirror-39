from cli import pyke, commands
import click

@click.group(help='This CLI will allow you to interact with the Lumavate platform from your terminal. For setup instructions, look in github. \
Each command below has subcommands. Pass the --help flag to those commands for more information on how to use them.')
def cli():
    pass

cli.add_command(commands.env)
cli.add_command(commands.profile)
cli.add_command(commands.organization)
cli.add_command(commands.widget)
cli.add_command(commands.widget_version)
cli.add_command(commands.component_set)
cli.add_command(commands.component_set_version)
cli.add_command(commands.microservice)
cli.add_command(commands.microservice_version)
cli.add_command(commands.version)
cli.add_command(commands.api)

if __name__ == '__main__':
    cli(help='')
