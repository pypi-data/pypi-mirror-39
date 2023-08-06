import click
import sys

from snark.cli.auth          import login, logout
#from snark.cli.pod_control   import start, stop, ls
from snark.cli.data_transfer import push, pull
from snark.cli.connect       import attach
from snark.cli.hyper            import up, down, ps, logs
from snark.cli.store            import ls, sync, cp, rm, mv
from snark import config
from snark.log import configure_logger

@click.group()
@click.option('-h', '--host', default='{}'.format(config.SNARK_REST_ENDPOINT), help='Snark server rest endpoint')
@click.option('-v', '--verbose', count=True, help='Devel debugging')
def cli(host, verbose):
    configure_logger(verbose)

def add_commands(cli):
    cli.add_command(login)
    cli.add_command(logout)

    cli.add_command(up)
    cli.add_command(down)
    cli.add_command(ps)
    cli.add_command(logs)

    cli.add_command(ls)
    cli.add_command(sync)
    cli.add_command(cp)
    cli.add_command(rm)
    cli.add_command(mv)

add_commands(cli)
