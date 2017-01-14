Welcome to Pock
===============

Pock is a mocking framework for Python that makes creating complex test behaviour a breeze.

Pock provides an interface for creating and verifying mock behaviour that is natural and easy to read, no matter what the access method is, method, function call, property or item access.

.. code-block:: python

  # Create mock behaviour
  my_mock = mock()
  when(my_mock).hello().then_return('world')
  when(my_mock)('127.0.0.1', 8000).then_return(True)
  when(my_mock)['database'].then_return('postgres')
  when(my_mock).port.then_return(8000)

  # Access the mock
  my_mock.hello()  # 'world'
  my_mock('127.0.0.1', 8000)  # True
  my_mock['database']  # 'postgres'
  my_mock.port  # 8000

  # Verify the access took place
  verify(my_mock).hello()
  verify(my_mock)('127.0.0.1', 8000)
  verify(my_mock)['database']
  verify(my_mock).port


Some select features of Pock are:

- Mock and verify a range of access patterns in Python
- Match arguments during mock creation and verification
- Mock higher level Python objects such as context managers and generators
- Seamlessly mock asyncio code


To learn more, choose a topic from the navigation on the left or dive right into the :ref:`quickstart`.


.. toctree::
  :maxdepth: 3
  :hidden:

  installation
  quickstart
  behaviour
  verify
  matching
  higher
  asyncio
  changelog

Contributions, bugs, suggestions
--------------------------------

All welcome, feel free to open an issue on `Github <https://github.com/atbentley/pock/issues>`_.

Source
------

The main source repository for Pock can be found on `Github <https://github.com/atbentley/pock>`_.

Changelog
---------

See the full :ref:`changelog` for details.


License
-------

Pock is licensed under the MIT License, see the `source code for the full license text <https://raw.githubusercontent.com/atbentley/pock/master/LICENSE.txt>`_.
