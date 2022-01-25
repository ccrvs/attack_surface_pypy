from .base import finalize, SRC_PATH, CONFIG_PATH

import invoke


@invoke.task
def bandit(context, src_path=SRC_PATH, config_path=CONFIG_PATH):
    config_file = config_path / '.banditrc'
    context.run(
        "bandit {src_path} -c {config_file} -r -q".format(src_path=src_path, config_file=config_file)
    )
    print('bandit ok.')


@invoke.task
def vulture(context, src_path=SRC_PATH, min_confidence=100):
    context.run(
        "vulture {src_path} --min-confidence {min_confidence} --exclude *protocols.py".format(src_path=src_path, min_confidence=min_confidence)
    )
    print('vulture ok.')


@invoke.task
def flake(context, src_path=SRC_PATH, config_path=CONFIG_PATH):
    config_file = config_path / '.flake8'
    context.run('flake8 {src_path} --config {config_file}'.format(src_path=src_path, config_file=config_file))
    print('flake8 ok.')


@invoke.task
def pylint(context, src_path=SRC_PATH, config_path=CONFIG_PATH):
    config_file = config_path / '.pylintrc'
    context.run('pylint {src_path} --rcfile="{config_file}" -E'.format(src_path=src_path, config_file=config_file))
    print('pylint ok.')


@invoke.task
def mypy(context, src_path=SRC_PATH):
    context.run('mypy {src_path}'.format(src_path=src_path))
    print('mypy ok.')


@invoke.task(name='lint', default=True, pre=[flake, vulture, pylint, bandit, mypy, finalize])
def lint_all(_):
    print('lint ok.')


lint = invoke.Collection('lint')
lint.add_task(bandit, 'bandit')
lint.add_task(vulture, 'vulture')
lint.add_task(flake, 'flake')
lint.add_task(pylint, 'pylint')
lint.add_task(mypy, 'mypy')
lint.add_task(lint_all, 'all')
