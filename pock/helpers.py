from .matchers import AnyValueMatcher, AnyArgumentsMatcher, AnyKeywordArgumentsMatcher, AnyValuesMatcher
from .expectation import ExpectationBuilder
from .verification import VerificationBuilder
from .mock import Mock


def mock():
    return Mock()


def context_manager(returning=None):
    context_manager_mock = Mock()
    if returning is None:
        returning = context_manager_mock
    when(context_manager_mock).__enter__().then_return(returning)
    when(context_manager_mock).__exit__(any_values).then_return(None)
    return context_manager_mock


def when(mock):
    """ :type mock: Mock """
    return ExpectationBuilder(mock)


def verify(mock):
    """ :type mock: Mock """
    return VerificationBuilder(mock)


any_value = AnyValueMatcher()
any_args = AnyArgumentsMatcher()
any_kwargs = AnyKeywordArgumentsMatcher()
any_values = AnyValuesMatcher()
