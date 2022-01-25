import invoke

from .base import SRC_PATH, print_done


@invoke.task
def build(context):
    print('Building container...')
    context.run('docker build -t attack_surface_pypy -f Dockerfile .')
    print_done()


@invoke.task
def run(context, port=80, detached=True):
    print('Running container...')
    detached = '-d' if detached else ''
    context.run('docker run attack_surface_pypy -p {port}:{port} {detached}'.format(detached=detached, port=port))
    print_done()


@invoke.task(name='container', default=True, pre=[build, ], post=[run, ])
def run_all(_):
    print("Running container...")


container = invoke.Collection('container')
container.add_task(build, 'build')
container.add_task(run, 'run')
container.add_task(run_all, 'all')
