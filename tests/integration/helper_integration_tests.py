import pytest

from pock import Mock, when, verify, VerificationError


@pytest.fixture
def mock():
    return Mock()


def test_when_creates_behaviour(mock):
    """ :type mock: Mock """
    when(mock).some_method('some_arg').then_return('some_value')

    assert mock.some_method('some_arg') == 'some_value'


def test_verify_asserts_invocation(mock):
    """ :type mock: Mock """
    with pytest.raises(VerificationError):
        verify(mock).some_method('some_arg')

    mock.some_method('some_arg')
    assert verify(mock).some_method('some_arg') is True
