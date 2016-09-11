Pock
====

mocking in python


Installation
------------

.. code-block::

  pip install pock


Usage
-----

Creating a basic mock:

.. code-block:: python

  from pock import when, Mock

  my_mock = Mock()
  when(my_mock).something(1).then_return('a')
  when(my_mock).something(2).then_return('b')

  my_mock.something(1)  # 'a'
  my_mock.something(2)  # 'b'
  my_mock.something()  # None
  my_mock.something_else()  # None

  verify(my_mock).something(1)  # True
  verify(my_mock).other()  # VerificationError


Mocking properties:

.. code-block:: python

  property_mock = mock()
  when(property_mock).age.then_return(24)
  property_mock.age  # 24
  verify(property_mock).age  # True


Mocking top level functions:

.. code-block:: python

  function_mock = mock()
  when(function_mock)('a').then_return(1)
  function_mock('a')  # 1
  verify(fuction_mock)('a')  # True


Testing
-------

.. code-block::

  pip install plank
  plank install_requirements
  plank tests


License
-------

MIT
