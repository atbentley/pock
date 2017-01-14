.. _asyncio:

Asyncio Support
===============

Pock has support for asyncio coroutines and futures through the ``then_return_future``, ``then_compute_future`` and ``then_raise_future`` results types.

.. code-block:: python

  from pock import mock, when_async

  async_mock = mock()
  when(async_mock).connect().then_return_future(True)

  await async_mock.connect()  # True
