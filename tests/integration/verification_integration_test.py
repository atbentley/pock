import pytest

from pock.behaviour import Behaviour, ValueResult
from pock.mock import Mock
from pock.verification import VerificationBuilder, VerificationError


@pytest.fixture
def mock():
    return Mock()


@pytest.fixture
def verification_builder(mock):
    return VerificationBuilder(mock, lambda result: len(result) > 0, 'error')


def test_verification_builder_raises_verification_error_when_not_called(verification_builder):
    """ :type verification_builder: VerificationBuilder"""
    with pytest.raises(VerificationError):
        verification_builder.something(1)


def test_accessing_a_property_returns_a_list_of_invocations(verification_builder, mock):
    """
    :type verification_builder: VerificationBuilder
    :type mock: Mock
    """
    mock._add_property_behaviour(Behaviour('property', result=ValueResult(None)))
    mock.property

    assert verification_builder.property.results == ['property']
