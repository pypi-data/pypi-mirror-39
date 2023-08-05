import click

from clusterone import authenticate

from clusterone.messages import project_creation_in_progress_message
from .helper import main


@click.command()
@click.argument('name')
@click.argument('source', default='github')
@click.option('--public/--private', default=False)
@click.option('--description', default='')
@click.pass_obj
@authenticate()
def command(context, name, source, public, description):
    """
    Create a new Clusterone project and output its git remote URL
    """

    click.echo(project_creation_in_progress_message)

    project = main(context, name, source, public, description)

    click.echo("{}: {}".format(source, project.get('full_name')))

    return project.get('full_name')

