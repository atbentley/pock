Types of Mocks
==============

Magic mock
----------

The magic mock will never throw an ``AttributeError`` or ``TypeError``. Instead it will return a new mock when accessed, even if no behaviour has been been defined for the current access method.

.. code-block:: python

  magic_mock = mock()
  magic_mock.method()  # new magic mock
  magic_mock()  # new magic mock
  magic_mock.property  # new magic mock
  magic_mock['item']  # new magic mock

A magic mock will always return the same mock when accessed in the same manner and different mocks when accessed differently.

.. code-block:: python

  assert my_mock.method_1() == my_mock.method_1()
  assert my_mock.method_1() != my_mock.method_2()

Strict mock
-----------

A strict mock will throw exceptions if used in a way that hasn't had behaviour explicitly defined for it.

.. code-block:: python

  strict_mock = mock(strict=True)
  when(strict_mock).valid().then_return(True)
  strict_mock.valid()  # True
  strict_mock.method()  # error
  strict_mock()  # error
  strict_mock.property  # error
  strict_mock['item']  # error


Specced mock
------------

A specced mock is a mix between a magic mock and a strict mock. When a method or property falls into the spec the mock will behave like a magic mock, when the method or property falls outside of the spec then the mock will behave like a strict mock.

A spec can be an object in which case it is inspected and its methods and properties are pulled off it or the spec can be a list of acceptable methods or properties. If an object creates some methods or properties dynamically (for instance in the constructor) then those will have to be passed in using ``extra_spec``.

.. code-block:: python

  class Database:
      def __init__(self, host, port):
          self.host = host
          self.port = port

      def select(self):
          pass

  specced_mock = mock(Database, extra_spec=('host', 'port'))
  specced_mock.select()  # new magic mock
  specced_mock.port  # new magic mock
  specced_mock.method()  # error

  specced_mock2 = mock(['select', 'insert'])
  specced_mock2.insert()  # new magic mock
  specced_mock2.method()  # error
