import os
import re
from setuptools import setup


def read(path):
    global os
    with open(os.path.join(os.path.dirname(__file__), path), 'r') as f:
        data = f.read()
    return data.strip()


def get_version():
    global os, re, read
    _version_re = re.compile(r'\s*__version__\s*=\s*\'(.*)\'\s*')
    return _version_re.findall(read(os.path.join('pock', '__init__.py')))[0]


test_requires = read('build-requirements.txt').split('\n')

setup(
    name='pock',
    version=get_version(),
    url='http://github.com/atbentley/pock',
    license='MIT',
    author='Andrew Bentley',
    author_email='andrew.t.bentley@gmail.com',
    description="A python mocking framework.",
    long_description=read('README.rst'),
    packages=['pock'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    tests_require=test_requires
)
