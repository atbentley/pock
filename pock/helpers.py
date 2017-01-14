from .matchers import AnyValueMatcher, AnyArgumentsMatcher, AnyKeywordArgumentsMatcher, AnyValuesMatcher
from .behaviour import BehaviourBuilder
from .verification import VerificationBuilder

try:
    import asyncio
    from .async_mock import AsyncMock as Mock
except ImportError:
    asyncio = None
    from .mock import Mock


def mock():
    return Mock()


def context_manager(returning=None):
    context_manager_mock = Mock()
    if returning is None:
        returning = context_manager_mock
    when(context_manager_mock).__enter__().then_return(returning)
    when(context_manager_mock).__exit__(any_values).then_return(None)
    if asyncio:
        when_async(context_manager_mock).__aenter__().then_return(returning)
        when_async(context_manager_mock).__aexit__(any_values).then_return(None)
    return context_manager_mock


def when(mock):
    return BehaviourBuilder(mock)


def when_async(mock):
    return BehaviourBuilder(mock, async=True)


def verify(mock):
    return VerificationBuilder(mock)


any_value = AnyValueMatcher()
any_args = AnyArgumentsMatcher()
any_kwargs = AnyKeywordArgumentsMatcher()
any_values = AnyValuesMatcher()
