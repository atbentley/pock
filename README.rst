Pock
====

Pock is a mocking framework for python. Pock supports:

 - Creating magic mocks
 - Defining the behaviour of mocks
 - Asserting on the access of mocks

Pock does not make assumptions about which testing framework it's being run inside, so it'll work nicely with unittest, nosetest, pytest or whatever you choose to use.


Installation
------------

.. code-block::

  pip install pock


Usage
-----

Create a mock and add some basic behaviour:

.. code-block:: python

  from pock import mock, when, verify, any_value

  my_mock = mock()
  when(my_mock).greet('Andrew').then_return('Hi, Andrew')

  my_mock.greet('Andrew')  # 'Hi, Andrew'


Assert on the access of the mock

.. code-block:: python

  verify(my_mock).greet('Andrew')  # True
  verify(my_mock).greet('Someone else')  # VerificationError


Use matchers to be a little less specific

.. code-block:: python

  when(my_mock).start(any_value).then_return(True)
  my_mock.start('pock')  # True
  verify(my_mock).start(any_value)  # True


Mix and match exact values and matchers

.. code-block:: python

  when(my_mock).complex_call(1, 2, any_value, a=4, b=any_value)
  my_mock.complex_call(1, 2, 3, a=4, b=5)  # None
  verify(my_mock).complex_call(1, any_value, any_valuem a=any_value, b=any_value)


Raise exceptions on mock access

.. code-block:: python

  when(my_mock).connect('remotehost').then_raise(ConnectionError('Could not resolve host name'))
  my_mock.connect('remotehost')  # ConnectionError


Mocking properties:

.. code-block:: python

  property_mock = mock()
  when(property_mock).age.then_return(24)
  property_mock.age  # 24
  verify(property_mock).age  # True


Mocking top level functions:

.. code-block:: python

  function_mock = mock()
  when(function_mock)('c').then_return(3)
  function_mock('c')  # 3
  verify(fuction_mock)('c')  # True


Testing
-------

.. code-block::

  pip install plank
  plank install_requirements
  plank tests


License
-------

MIT
