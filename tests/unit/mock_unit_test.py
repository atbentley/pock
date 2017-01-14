import pytest

from pock.matchers import MatchCriteria
from pock.mock import Mock, overrides


@pytest.fixture
def mock():
    return Mock()


@pytest.fixture
def strict_mock():
    return Mock(strict=True)


@pytest.fixture
def behaviour():
    class MatchCriteriaStub(object):
        pass

    class BehaviourStub(object):
        def __init__(self):
            self.name = 'exceptional_behaviour'
            self.match_criteria = MatchCriteriaStub()

        def matches(self, *args, **kwargs):
            return True

        def get_result(self, args=None, kwargs=None):
            return 587

    return BehaviourStub()


def test_add_call_behaviour_adds_behaviour(mock, behaviour):
    """
    :type mock: Mock
    :type behaviour: Behaviour
    """
    mock._add_call_behaviour(behaviour)

    assert mock._call_behaviours[behaviour.match_criteria] == behaviour


def test_add_property_behaviour_adds_behaviour(mock, behaviour):
    """
    :type mock: Mock
    :type behaviour: Behaviour
    """
    mock._add_property_behaviour(behaviour)

    assert mock._property_behaviours[behaviour.name] == behaviour


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


def test_getattribute_adds_property_invocation(mock, behaviour):
    """
    :type mock: Mock
    :type behaviour: Behaviour
    """
    mock._add_property_behaviour(behaviour)

    getattr(mock, behaviour.name)

    assert behaviour.name in mock._property_invocations


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


def test_getattribute_raises_attribute_error_when_strict(strict_mock):
    """ :type strict_mock: Mock """
    with pytest.raises(AttributeError):
        strict_mock.nope()


def test_getattribute_does_not_raise_attribute_error_when_specced():
    specced_mock = Mock(spec=['sample'])

    assert specced_mock._strict is True
    assert specced_mock.sample()
    with pytest.raises(AttributeError):
        specced_mock.nope()


def test_call_returns_mock_and_adds_behaviour_if_no_behaviours_match(mock):
    """ :type mock: Mock """
    new_mock = mock(1, 2)

    assert isinstance(new_mock, Mock)
    assert mock._call_behaviours[MatchCriteria(args=(1,2), kwargs={})].get_result() == new_mock


def test_call_adds_call_invocation(mock):
    """ :type mock: Mock """
    args = (1,)
    kwargs = {'a': 1}

    mock(*args, **kwargs)

    assert (args, kwargs) in mock._call_invocations


def test_call_raises_type_error_when_strict(strict_mock):
    """ :type strict_mock: Mock """
    with pytest.raises(TypeError):
        strict_mock()


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


def test_getitem_raises_type_error_when_strict(strict_mock):
    """ :type strict_mock: Mock """
    with pytest.raises(TypeError):
        strict_mock['nope']
