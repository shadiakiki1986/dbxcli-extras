from .sync import DbxcliSync
import click

@click.group()
def cli():
    pass


@click.command()
@click.argument('localdir', type=click.Path(exists=True))
@click.argument('dbxdir', type=str)
@click.option('--verbosity', default=0, help="Verbosity level: 0, 1, 2")
def sync(localdir, dbxdir, verbosity):
    """dbxcli_sync command that solves https://github.com/dropbox/dbxcli/issues/53"""
    dcs = DbxcliSync(localdir, dbxdir, verbosity)
    dcs.sync_dir()


cli.add_command(sync)


#if __name__ == '__main__':
#    cli()
