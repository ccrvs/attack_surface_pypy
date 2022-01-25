import invoke


@invoke.task(default=True)
def run(context, file_path, dev=False, host=None, port=None):
    extras = set()
    if host:
        extras.add('--host {host}'.format(host=host))
    if port:
        extras.add('--port {port}'.format(port=port))

    kwargs = dict(file_path=file_path, extras=" ".join(extras))
    if dev:
        context.run('python -m attack_surface_pypy -X dev -f {file_path} {extras}'.format(**kwargs), pty=True)
    else:
        # context.run('python -OO -Wignore -m attack_surface_pypy')  # FIXME: pyparser
        context.run('python -Wignore -m attack_surface_pypy -f {file_path} {extras}'.format(**kwargs))


runner = invoke.Collection('run')
runner.add_task(run, 'all')
