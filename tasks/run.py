import invoke


@invoke.task(default=True)
def run(context, dev=False):
    if dev:
        context.run('python -m attack_surface_pypy -X dev', pty=True)
    else:
        context.run('python -OO -Wignore -m attack_surface_pypy')


runner = invoke.Collection('run')
runner.add_task(run, 'all')
