Pock
====

.. image:: https://travis-ci.org/atbentley/pock.svg?branch=master
  :target:  https://travis-ci.org/atbentley/pock

.. image:: https://coveralls.io/repos/github/atbentley/pock/badge.svg?branch=master
  :target: https://coveralls.io/github/atbentley/pock?branch=master

Pock is a mocking framework for Python that makes creating complex test behaviour a breeze. See the `documentation <http://pock.bentley.codes>`_ for more information.

Installation
------------

.. code-block::

  pip install pock


Usage
-----

Create a mock and add some basic behaviour:

.. code-block:: python

  from pock import mock, when, verify

  my_mock = mock()

  when(my_mock).greet('Andrew').then_return('Hi, Andrew')
  my_mock.greet('Andrew')  # 'Hi, Andrew'
  verify(my_mock).greet('Andrew')


Testing
-------

.. code-block::

  pip install plank
  plank install_requirements
  plank tests


License
-------

MIT
