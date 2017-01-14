Asyncio Support
===============

Pock has support for asyncio coroutines and futures through the ``when_async`` helper.

.. code-block:: python

  from pock import mock, when_async

  async_mock = mock()
  when_async(async_mock).connect().then_return(True)

  await async_mock.connect()
