Building Behaviours
===================

Behaviours determine what values a mock should return or what exception it should raise when interacted with. Use the ``when`` helper to create a behaviour builder for a mock. Building behaviours has two steps:

1. Interact with the behaviour builder in the same way the mock would be interacted with (e.g. just call it to setup some behaviour for a top-level function).
2. Specify what result should be returned when interacted with in the way specified in step one.

Interaction can be calling a method, calling a function, accessing a property or accessing an item.

.. code-block:: python

  # Mocking methods
  when(my_mock).some_method('some_arg').then_return('some_value')
  my_mock.some_method('some_arg')  # 'some_value'

  # Mocking top-level functions
  when(my_mock)('some_arg').then_return('some_value')
  my_mock('some_arg')  # 'some_value'

  # Mocking properties
  when(my_mock).some_property.then_return('some_value')
  my_mock.some_property  # 'some_value'

  # Mocking items
  when(my_mock)['some_item'].then_return('some_value')
  when(my_mock)[10].then_return('some_other_value')
  my_mock['some_item']  # 'some_value'
  my_mock[10]  # 'some_other_value'

Results
-------

Returning Constants
^^^^^^^^^^^^^^^^^^^

Use ``then_return`` to specify a constant value to return.

.. code-block:: python

  when(my_mock).method().then_return('constant')
  my_mock.method()  # 'constant'

Returning computed values
^^^^^^^^^^^^^^^^^^^^^^^^^

Use ``then_compute`` to specify a function for computing a return value based off the arguments used.

.. code-block:: python

  when(my_mock).method(any_value).then_compute(lambda x: x ** 2)
  my_mock.method(4)  # 16

Raising exceptions
^^^^^^^^^^^^^^^^^^

Use ``then_raise`` to specify an exception to raise.

.. code-block:: python

  when(my_mock).method().then_raise(ValueError)
  my_mock.method()  # ValueError

Chaining results
^^^^^^^^^^^^^^^^

Results can be chained up just by specifying more than one result. When a mock is interacted with more times than results are specified for the last specified result is used again.

.. code-block:: python

  when(my_mock).bind().then_return(True).then_raise(Exception)
  my_mock.bind()  # True
  my_mock.bind()  # Exception
  my_mock.bind()  # Exception

Asyncio
^^^^^^^

See :ref:`asyncio` for notes on how to return asyncio coroutines and futures.