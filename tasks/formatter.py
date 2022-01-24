from email.policy import default
from .base import print_done, finalize, SRC_PATH, CONFIG_PATH

import invoke


@invoke.task
def isort(context, src_path=SRC_PATH):
    print('Running isort...')
    context.run('isort {src_path} -m VERTICAL_HANGING_INDENT --tc'.format(src_path=src_path))
    print_done(indent=4)


@invoke.task
def yapf(context, src_path=SRC_PATH, config_path=CONFIG_PATH):
    print('Running yapf...')
    config_file = config_path / '.style.yapf'
    context.run('yapf --style="{config_file}" {src_path} -r -i'.format(src_path=src_path, config_file=config_file))
    print_done(indent=4)


@invoke.task
def unify(context, src_path=SRC_PATH):
    print('Running unify...')
    context.run('unify {src_path} -r -i --quote "\""'.format(src_path=src_path))
    print_done(indent=4)


@invoke.task(name='format', default=True, post=[isort, yapf, unify, ])
def format_task(_):
    print("Running formatters...")


formatter = invoke.Collection('format')
formatter.add_task(isort, 'isort')
formatter.add_task(yapf, 'yapf')
formatter.add_task(unify, 'unify')
formatter.add_task(format_task, 'all')
