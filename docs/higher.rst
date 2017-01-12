Higher Order Objects
====================

Pock includes helpers for making it easier to mock some of the higher order objects in python.

Context managers
----------------

.. code-block:: python

  from pock import mock, when, context_manager

  file = context_manager()
  when(file).read().then_return('hello')
  file_system = mock()
  when(file_system).open('file.txt', 'r').then_return(file)

  with file_system.open('file.txt', 'r') as f:
      print(f.read())  # hello


Generators
----------
