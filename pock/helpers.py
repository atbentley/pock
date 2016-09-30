from .matchers import AnyValueMatcher, AnyArgumentsMatcher, AnyKeywordArgumentsMatcher, AnyValuesMatcher
from .expectation import ExpectationBuilder
from .verification import VerificationBuilder
from .mock import Mock


def mock():
    return Mock()


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
