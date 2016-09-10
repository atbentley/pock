from .expectation import ExpectationBuilder
from .verification import VerificationBuilder


def when(mock):
    """ :type mock: Mock """
    return ExpectationBuilder(mock)


def verify(mock):
    """ :type mock: Mock """
    return VerificationBuilder(mock)
