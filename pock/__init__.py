from .expectation import ExpectationBuilder
from .mock import Mock
from .verification import VerificationBuilder

__version__ = '0.0.1'


def when(mock):
    """ :type mock: Mock """
    return ExpectationBuilder(mock)


def verify(mock):
    """ :type mock: Mock """
    return VerificationBuilder(mock)
