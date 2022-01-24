import pathlib

import invoke


ROOT_PATH = pathlib.Path.cwd()
SRC_PATH = ROOT_PATH / 'src'
CONFIG_PATH = ROOT_PATH / 'config'


def print_done():
    print('ok.')


@invoke.task
def finalize(_):
    print_done()
