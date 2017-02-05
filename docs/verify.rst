Verifying Interactions
======================

Use the ``verify`` helper to create a verification builder for a mock. Just like when building behaviours, simply invoke the verification builder the same way the mock would have been invoked to check if the mock has been invoked in that way. If the mock has not been invoked in that way a ``VerificationError`` will be raised.

.. code-block:: python

  verify(my_mock).method(*args, **kwargs)
  verify(my_mock)(*args, **kwargs)
  verify(my_mock).property
  verify(my_mock)[arg]


Verifiers also return a list of interactions (these may contain the args and kwargs) that satisfy the condition.

.. code-block:: python

  my_mock.method(1, 2)
  my_mock.method(3, b=4)
  verify(my_mock).method(any_values)  # [((1,2), {}), ((3,), {'b': 4})]

  my_mock.property
  my_mock.property
  verify(my_mock).property  # ['property', 'property']

  my_mock['item']
  my_mock['other_item']
  verify(my_mock)[any_value]  # ['item', 'other_item']

Built-in verifiers
------------------

- ``verify(mock)``: verify at least one interaction
- ``verify_once(mock)``: verify exactly one interaction
- ``verify_n(mock, n)``: verify exactly ``n`` interactions
- ``verify_never(mock)``: verify exactly zero interactions


Creating custom verifiers
-------------------------

Custom verifiers are easy to create and only require two things

1. A function to determine if the verification is successful or not, this function accepts the list of invocations and should return True or False
2. An error message to display when verification fails

.. code-block:: python

  from pock.verification import VerificationBuilder


  def is_even(results):
      return result: len(result) % 2 == 0

  def verify_even(mock):
      msg = ('Expected an even number of {accesses} to {thing}, '
             'but {amount} {were_was} made')
      return VerificationBuilder(mock, is_even, msg)

Then simply call ``verify_even(my_mock).some_method()`` to use the new custom verifier.

When building the error message template, the following values are available for substition

- ``access`` and ``accesses``: the verb used to indicate access, e.g. `call` and `calls` when verify method access or `access` and `accesses` when verifying property access.
- ``thing``: the thing being accessed, e.g. `method(arg)` for ``verify(my_mock).method(arg)``
- ``amount``: the number of invocations that were found
- ``were_was``: Is `were` or `was` depending on whether count is non-zero or zero
