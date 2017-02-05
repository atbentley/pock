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
    msg = 'Expected at least one {access} to {thing}, but no such {access} was made'
    return VerificationBuilder(mock, lambda result: len(result) > 0, msg)


def verify_once(mock):
    msg = 'Expected exactly one {access} to {thing}, but {amount} {were_was} made'
    return VerificationBuilder(mock, lambda result: len(result) == 1, msg)


def verify_n(mock, n):
    msg = 'Expected exactly {n} {{accesses}} to {{thing}}, but {{amount}} {{were_was}} made'.format(n=n)
    return VerificationBuilder(mock, lambda result: len(result) == n, msg)


any_value = AnyValueMatcher()
any_args = AnyArgumentsMatcher()
any_kwargs = AnyKeywordArgumentsMatcher()
any_values = AnyValuesMatcher()
