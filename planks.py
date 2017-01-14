import os
import sys
import time

from plank import task, depends


@task
def install_requirements():
    import pip
    pip.main(['install', '--upgrade', '-r', 'build-requirements.txt'])


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


def build_docs():
    import sphinx
    sphinx.main(['', '-c', 'docs', '-b', 'html', 'docs', 'docs/_build/html'])


@task
def docs():
    print('See docs/_build for compiled documentation')
    build_docs()


@task
def docs_watch():
    import sphinx
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    class Handler(FileSystemEventHandler):
        def __init__(self, observer):
            self.observer = observer

        def on_any_event(self, event):
            self.observer.stop()
            try:
                build_docs()
            finally:
                watch()

    def watch():
        observer = Observer()
        handler = Handler(observer)
        observer.schedule(handler, 'docs', recursive=True)
        observer.start()

    watch()
    while True:
        time.sleep(1)


@task
def docs_serve():
    import threading
    try:
        from http.server import test as serve, SimpleHTTPRequestHandler
    except ImportError:
        from SimpleHTTPServer import test as serve, SimpleHTTPRequestHandler
        sys.argv = ['']

    os.chdir('docs/_build/html')
    server = threading.Thread(target=serve, kwargs={'HandlerClass': SimpleHTTPRequestHandler})
    server.run()


@task
def docs_dev():
    from multiprocessing import Process

    try:
        build_docs()
    except SystemExit:
        pass

    builder = Process(target=docs_watch.run)
    server = Process(target=docs_serve.run)
    builder.start()
    server.run()
    try:
        while True:
            time.sleep(1)
    finally:
        builder.terminate()
        server.terminate()
        builder.join()
        server.join()
