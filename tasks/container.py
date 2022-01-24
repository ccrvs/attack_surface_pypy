from email.policy import default
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
    context.run('docker run attack_surface_pypy -p {port}:{port} {detached}'.format(detached=detached))
    print_done()
