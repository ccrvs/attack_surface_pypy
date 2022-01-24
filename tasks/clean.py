from .base import print_done, finalize

import invoke


@invoke.task
def clean_pyc(context):
    print('Cleaning compiled files...')
    context.run('find . -type f -name ".py[co]" -delete')
    context.run('find . -type d -name "__pycache__" -delete')
    print_done()


@invoke.task
def clean_build(context):
    print("Cleaning build files...")
    context.run('rm --force --recursive build/')
    context.run('rm --force --recursive dist/')
    context.run('rm --force --recursive *.egg-info')
    print_done()


@invoke.task
def clean_test(context):
    print('Cleaning tests temp files...')
    context.run('rm -rf .tox/')
    context.run('rm -f .coverage/')
    context.run('rm -rf htmlcov/')
    context.run('rm -rf .mypy_cache/')
    context.run('rm -rf .hypothesis/')
    print_done()


@invoke.task(name='clean', default=True, post=[clean_build, clean_pyc, clean_test, finalize, ])
def clean_all(_):
    print("Cleaning build, compiled files, tests...")


clean = invoke.Collection('clean')
clean.add_task(clean_test, 'test')
clean.add_task(clean_pyc, 'pyc')
clean.add_task(clean_build, 'build')
clean.add_task(clean_all, 'all')
