from .sync import DbxcliSync
from .getr import getr
import click

@click.group()
def cli():
    pass


@click.command()
@click.argument('localdir', type=click.Path(exists=True))
@click.argument('dbxdir', type=str)
@click.option('--verbosity', default=0, help="Verbosity level: 0, 1, 2")
def sync(localdir, dbxdir, verbosity):
    """
    sync local folder with remote dropbox folder
    Solves https://github.com/dropbox/dbxcli/issues/53
    """
    dcs = DbxcliSync(localdir, dbxdir, verbosity)
    dcs.sync_dir()


@click.command()
@click.argument('dbxdir', type=str)
@click.argument('localdir', type=click.Path(exists=True))
@click.option('--verify', is_flag=True, default=False, help="Verify downloads (download it several times)")
@click.option('--verbose', is_flag=True, default=False, help="Be verbose")
def getr(dbxdir, localdir, verify, verbose):
    """
    Recursive get
    Solves https://github.com/dropbox/dbxcli/issues/60
    """
    print(dbxdir, localdir, verify, verbose)
    getr(dbxdir, localdir, verify, verbose)



cli.add_command(sync)
cli.add_command(getr)


#if __name__ == '__main__':
#    cli()
