import click
from auth.commands import login, register
import webbrowser


@click.group()
def cli():
    """Main entry point for the CLI."""
    pass

@cli.group()
def auth():
    """
    Wapper of auth
    :return:
    """
    pass


# Register the commands
auth.add_command(login.command, name='login')
cli.add_command(register.command, name='register')

if __name__ == '__main__':
    cli()
