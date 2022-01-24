import invoke

from .base import CONFIG_PATH


@invoke.task(default=True, help={'coverage': 'Name an app to coverage.'})
def test(context, report='term', config_path=CONFIG_PATH, coverage='attack_surface_pypy', marker=''):
    print('Running tests...')
    pytest_config_file = config_path / 'pytest.ini'
    coverage_config_file = config_path / '.coveragerc'
    marker = '-m "{marker}"'.format(marker=marker) if marker else ''
    context.run((
        'pytest -c {pytest_config_file} --cov={coverage} --cov-config={coverage_config_file} '
        '--cov-report={report} {marker}'
    ).format(
        pytest_config_file=pytest_config_file,
        coverage=coverage,
        coverage_config_file=coverage_config_file,
        report=report,
        marker=marker,
    ))


test_runner = invoke.Collection('test')
test_runner.add_task(test, 'all')
