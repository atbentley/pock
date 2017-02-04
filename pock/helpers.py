from .matchers import AnyValueMatcher, AnyArgumentsMatcher, AnyKeywordArgumentsMatcher, AnyValuesMatcher
from .behaviour import BehaviourBuilder
from .verification import VerificationBuilder

try:
    import asyncio
    from .async_mock import AsyncMock as Mock
except ImportError:
    asyncio = None
    from .mock import Mock


def mock(spec=None, extra_spec=None, strict=False):
    return Mock(spec=spec, extra_spec=extra_spec, strict=strict)


def context_manager(returning=None):
    context_manager_mock = Mock()
    if returning is None:
        returning = context_manager_mock
    when(context_manager_mock).__enter__().then_return(returning)
    when(context_manager_mock).__exit__(any_values).then_return(None)
    if asyncio:
        when(context_manager_mock).__aenter__().then_return_future(returning)
        when(context_manager_mock).__aexit__(any_values).then_return_future(None)
    return context_manager_mock


def when(mock):
    return BehaviourBuilder(mock)


def verify(mock):
    return VerificationBuilder(mock)


def verify_once(mock):
    return VerificationBuilder(mock, test=lambda result: len(result) == 1)


any_value = AnyValueMatcher()
any_args = AnyArgumentsMatcher()
any_kwargs = AnyKeywordArgumentsMatcher()
any_values = AnyValuesMatcher()
