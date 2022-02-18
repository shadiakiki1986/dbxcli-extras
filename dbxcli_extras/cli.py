from .sync import DbxcliSync
from .getr import DbxcliGetr
import click

@click.group()
def cli():
    pass


@click.command()
@click.argument('localdir', type=click.Path(exists=True))
@click.argument('dbxdir', type=str)
@click.option('--verbosity', default=0, help="Verbosity level: 0, 1, 2")
@click.option('--start-from', default="", help="Files are sorted before sync. Use this field to start from a particular file instead of from the beginning.")
def sync(localdir, dbxdir, verbosity, start_from):
    """
    sync local folder with remote dropbox folder
    Solves https://github.com/dropbox/dbxcli/issues/53
    """
    dcs = DbxcliSync(localdir, dbxdir, verbosity)
    dcs.sync_dir(start_from)


@click.command()
@click.argument('dbxdir', type=str)
@click.argument('localdir', type=click.Path(exists=True))
@click.option('--verify', is_flag=True, default=False, help="Verify downloads (download it several times)")
@click.option('--verbosity', default=0, help="Verbosity level: 0, 1, 2")
def getr(dbxdir, localdir, verify, verbosity):
    """
    Recursive get
    Solves https://github.com/dropbox/dbxcli/issues/60
    """
    dcg = DbxcliGetr(verify, verbosity)
    dcg.getr(dbxdir, localdir)



cli.add_command(sync)
cli.add_command(getr)


if __name__ == '__main__':
    cli()
