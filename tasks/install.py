import pathlib

from .base import print_done
from .build import build
from .clean import clean_all

import invoke


@invoke.task(
    name='install', 
    default=True, 
    pre=[build, ], 
    post=[clean_all, ], 
    help={'no-dev': 'Use this key to ignore dev dependencies.', 'verbose': 'Show output.'},
)
def install_all(context, no_dev=False, verbose=False):
    print('Installing...')
    extra = {}
    to_devnull = '> /dev/null'
    if verbose:
        to_devnull = ''
        extra = {'pty': True, 'warn': True}
    context.run('poetry install {no_dev} {verbosity}'.format(
        no_dev='--no-dev' if no_dev else "", verbosity=to_devnull,
    ), **extra)
    print_done()


installer = invoke.Collection('install')
installer.add_task(install_all, 'all')
