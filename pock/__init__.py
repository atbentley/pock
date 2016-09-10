from .expectation import ExpectationBuilder
from .mock import Mock

__version__ = '0.0.1'


def when(mock):
    """ :type mock: Mock """
    return ExpectationBuilder(mock)
