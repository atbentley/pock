import pytest

from pock.matchers import MatchCriteria
from pock.mock import Mock, overrides


@pytest.fixture
def mock():
    return Mock()


@pytest.fixture
def expectation():
    class MatchCriteriaStub(object):
        pass

    class ExpectationStub(object):
        def __init__(self):
            self.name = 'exceptional_expectation'
            self.match_criteria = MatchCriteriaStub()

        def matches(self, *args, **kwargs):
            return True

        def get_result(self, args=None, kwargs=None):
            return 587

    return ExpectationStub()


def test_add_call_expectation_adds_expectation(mock, expectation):
    """
    :type mock: Mock
    :type expectation: Expectation
    """
    mock._add_call_expectation(expectation)

    assert mock._call_expectations[expectation.match_criteria] == expectation


def test_add_property_expectation_adds_expectation(mock, expectation):
    """
    :type mock: Mock
    :type expectation: Expectation
    """
    mock._add_property_expectation(expectation)

    assert mock._property_expectations[expectation.name] == expectation


@pytest.mark.parametrize('param', overrides)
def test_getattribute_passes_through_overrides(mock, param):
    expected_param = object.__getattribute__(mock, param)
    actual_param = getattr(mock, param)
    assert actual_param == expected_param


def test_getattribute_creates_sub_mock(mock):
    """ :type mock: Mock """
    sub_mock = mock.something

    assert sub_mock != mock
    assert isinstance(sub_mock, Mock)


def test_getattribute_adds_property_invocation(mock, expectation):
    """
    :type mock: Mock
    :type expectation: Expectation
    """
    mock._add_property_expectation(expectation)

    getattr(mock, expectation.name)

    assert expectation.name in mock._property_invocations


def test_getattribute_creates_different_sub_mocks(mock):
    """ :type mock: Mock """
    some_sub_mock = mock.someting
    some_other_sub_mock = mock.something_else

    assert some_sub_mock is not some_other_sub_mock


def test_getattribute_the_same_sub_mock_for_multiple_access(mock):
    """ :type mock: Mock """
    first_sub_mock = mock.something
    second_sub_mock = mock.something

    assert first_sub_mock is second_sub_mock


def test_getattribute_returns_self_when_accessing_call(mock):
    """ :type mock: Mock """
    sub_mock = mock.__call__

    assert sub_mock is mock


def test_call_returns_mock_and_adds_expectation_if_no_expectations_match(mock):
    """ :type mock: Mock """
    new_mock = mock(1, 2)

    assert isinstance(new_mock, Mock)
    assert mock._call_expectations[MatchCriteria(args=(1,2), kwargs={})].get_result() == new_mock


def test_call_adds_call_invocation(mock):
    """ :type mock: Mock """
    args = (1,)
    kwargs = {'a': 1}

    mock(*args, **kwargs)

    assert (args, kwargs) in mock._call_invocations


def test_getitem_creates_different_sub_mock(mock):
    """ :type mock: Mock """
    some_sub_mock = mock[1]
    some_other_sub_mock = mock['a']

    assert some_sub_mock is not some_other_sub_mock


def test_getitem_creates_same_sub_mock(mock):
    """ :type mock: Mock """
    some_sub_mock = mock[1]
    some_other_sub_mock = mock[1]

    assert some_sub_mock is some_other_sub_mock


def test_getitem_adds_item_invocation(mock):
    """ :type mock: Mock """
    mock[1]

    assert 1 in mock._item_invocations
