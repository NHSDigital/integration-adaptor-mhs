import asyncio


def awaitable(result=None):
    """
    Create a :class:`asyncio.Future` that is completed and returns result.
    :param result: to return
    :return: a completed :class:`asyncio.Future`
    """
    future = asyncio.Future()
    future.set_result(result)
    return future


def awaitable_exception(exception: Exception):
    """
    Create a :class:`asyncio.Future` that is completed and raises an exception.
    :param exception: to raise
    :return: a completed :class:`asyncio.Future`
    """
    future = asyncio.Future()
    future.set_exception(exception)
    return future
