import os

from plank import task, depends


@task
def install_requirements():
    import pip
    pip.main(['install', '--upgrade', '-r', 'requirements.txt', '-r', 'build-requirements.txt'])


@task
def check_requirements():
    import pip
    pip.main(['list', '--outdated'])


@task
def unit_tests():
    import pytest
    exit_status = pytest.main(['--cov', 'pock', '--cov-report=', 'tests/unit'])
    os.rename('.coverage', '.unit.coverage')
    if exit_status != 0:
        raise Exception('Unit tests failed')


@task
def integration_tests():
    import pytest
    exit_status = pytest.main(['--cov', 'pock', '--cov-report=', 'tests/integration'])
    os.rename('.coverage', '.integration.coverage')
    if exit_status != 0:
        raise Exception('Integration tests failed')


@task
def functional_tests():
    import pytest
    exit_status = pytest.main(['tests/functional.py'])
    if exit_status != 0:
        raise Exception('Integration tests failed')


@task
def coverage():
    import coverage
    cov = coverage.coverage()
    cov.load()
    cov.combine(['.unit.coverage', '.integration.coverage'])
    cov.save()
    cov.report(show_missing=True)


@task
@depends('unit_tests', 'integration_tests', 'functional_tests', 'coverage')
def tests():
    pass


@task
def package():
    from distutils.core import run_setup

    run_setup('setup.py', script_args=['sdist'])


@task
@depends('check_requirements', 'install_requirements', 'tests', 'package')
def build():
    pass
