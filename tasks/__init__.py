import invoke

from . import build, clean, formatter, run, tests, lint, install


ns = invoke.Collection()
ns.add_collection(build.builder, 'build')
ns.add_collection(clean.clean, 'clean')
ns.add_collection(formatter.formatter, 'format')
ns.add_collection(run.runner, 'run')
ns.add_collection(tests.test_runner, 'test')
ns.add_collection(lint.lint, 'lint')
ns.add_collection(install.installer, 'install')
