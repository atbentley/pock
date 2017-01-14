Verifying Interactions
======================

Use the ``verify`` helper to create a verification builder for a mock. Just like when building behaviours, simply invoke the verification builder the same way the mock would have been invoked to check if the mock has been invoked in that way. If the mock has not been invoked in that way a ``VerificationError`` will be raised.

.. code-block:: python

  verify(my_mock).method(*args, **kwargs)
  verify(my_mock)(*args, **kwargs)
  verify(my_mock).property
  verify(my_mock)[arg]
