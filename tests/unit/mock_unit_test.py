import pytest

from pock.expectation import Expectation
from pock.mock import Mock, overrides


@pytest.fixture
def mock():
    return Mock()


@pytest.mark.parametrize('param', overrides)
def test_getattribute_passes_through_overrides(mock, param):
    expected_param = object.__getattribute__(mock, param)
    actual_param = getattr(mock, param)
    assert actual_param == expected_param


def test_getattribute_creates_sub_mock(mock):
    sub_mock = mock.something

    assert sub_mock != mock
    assert isinstance(sub_mock, Mock)


def test_getattribute_creates_different_sub_mocks(mock):
    some_sub_mock = mock.someting
    some_other_sub_mock = mock.something_else

    assert some_sub_mock is not some_other_sub_mock


def test_getattribute_the_same_sub_mock_for_multiple_access(mock):
    first_sub_mock = mock.something
    second_sub_mock = mock.something

    assert first_sub_mock is second_sub_mock


def test_call_returns_value_if_expectation_matches(mock):
    expected_value = 'returned'
    mock._add_expectation(Expectation(None, (1,), {}, expected_value))

    actual_value = mock(1)

    assert actual_value == expected_value


def test_call_returns_none_if_no_expectations_match(mock):
    actual_value = mock(1, 2)

    assert actual_value is None
