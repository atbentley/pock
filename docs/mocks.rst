Types of Mocks
==============

Magic mock
----------

The magic mock will never throw an ``AttributeError`` or ``TypeError``. Instead it will return a new mock when accessed, even if no behaviour has been been defined for the current access method.

.. code-block:: python

  from pock import mock

  my_mock = mock()
  my_mock.method()  # new mock
  my_mock()  # new mock
  my_mock.property  # new mock
  my_mock['item']  # new mock

A magic mock will always return the same mock when accessed in the same manner and different mocks when accessed differently.

.. code-block:: python

  assert my_mock.method_1() == my_mock.method_1()
  assert my_mock.method_1() != my_mock.method_2()

Strict mock
-----------

A strict mock will throw exceptions if used in a way that hasn't had behaviour explicitly defined for it.

.. code-block:: python

  from pock import strict_mock, when

  my_mock = strict_mock()
  when(my_mock).valid().then_return(True)
  my_mock.valid()  # True
  my_mock.method()  # error
  my_mock()  # error
  my_mock.property  # error
  my_mock['item']  # error
