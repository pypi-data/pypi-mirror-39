import click

from ..repo import RepoManager


@click.command()
@click.option(
    '--sandbox', is_flag=True,
    help='Validate only on sandbox/deploy branch', default=False)
@click.pass_context
def validate(ctx, sandbox):
    """Check if version of repository is semantic
    """
    m = RepoManager(ctx.obj['agile'])
    if not sandbox or m.can_release('sandbox'):
        click.echo(m.validate_version())
