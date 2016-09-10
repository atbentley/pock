import pytest

from pock.mock import Mock
from pock.verification import VerificationBuilder, VerificationError


@pytest.fixture
def mock():
    return Mock()


@pytest.fixture
def verification_builder(mock):
    return VerificationBuilder(mock)


def test_verification_builder_returns_true_when_called(verification_builder, mock):
    """ :type verification_builder: VerificationBuilder"""
    mock.something(1)

    assert verification_builder.something(1) is True


def test_verification_builder_raises_verification_error_when_not_called(verification_builder):
    """ :type verification_builder: VerificationBuilder"""
    with pytest.raises(VerificationError):
        verification_builder.something(1)
