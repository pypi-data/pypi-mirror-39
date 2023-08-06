import click
import os

from git import Repo
from ant_pkg.context import pass_context
from ant_pkg.utils import dir, logger, try_execpt
from ant_pkg.responses import HELP_DESCRIPTION
from ant_pkg.constants import COMMAND_FOLDER


class AntCLI(click.MultiCommand):
    def list_commands(self, ctx):
        try:
            rv = []
            for filename in os.listdir(COMMAND_FOLDER):
                if filename.endswith('.py'):
                    rv.append(filename[:-3])
            rv.sort()
            return rv
        except Exception as e:
            log = logger.create('list_command_logger')
            log.error(e)

    def get_command(self, ctx, name):
        try:
            ns = {}
            fn = os.path.join(COMMAND_FOLDER, name + '.py')
            with open(fn) as f:
                code = compile(f.read(), fn, 'exec')
                eval(code, ns, ns)
            return ns['command']
        except (KeyError, FileNotFoundError):
            pass
        except Exception as e:
            log = logger.create('get_command_logger')
            log.error(e)


cli = AntCLI(help=HELP_DESCRIPTION)


@click.command(cls=AntCLI)
@click.option('-v', '--verbose', is_flag=True, help="Enabled the code's traceback.")
@click.option('--scaffolds', default=None, type=click.Path(),
              help='Used to establish the absolute path of your custom scaffolds.')
@pass_context
@try_execpt.handler
def cli(ctx, verbose, scaffolds):
    ctx.verbose = verbose

    if scaffolds is not None:
        ctx.scaffolds_local = scaffolds

    if not dir.exists(ctx.scaffolds_local) and scaffolds is None:
        Repo.clone_from(ctx.scaffolds_remote, ctx.scaffolds_local)
