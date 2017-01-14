import pytest

from pock.behaviour import BehaviourBuilder, Behaviour, ErrorResult, ValueResult
from pock.matchers import MatchCriteria


class FakeMock(object):
    def __getattribute__(self, name):
        if name in ['_add_call_behaviour', '_add_item_behaviour']:
            return lambda _: None
        return self


@pytest.fixture
def fake_mock():
    return FakeMock()


@pytest.fixture
def behaviour_builder(fake_mock):
    """ :type fake_mock: Mock """
    return BehaviourBuilder(fake_mock)


@pytest.fixture
def match_ready_behaviour_builder(behaviour_builder):
    """ :type behaviour_builder: BehaviourBuilder """
    getattr(behaviour_builder, 'first_time_attribute_access')
    return behaviour_builder


@pytest.fixture
def result_ready_behaviour_builder(match_ready_behaviour_builder):
    """ :type match_ready_behaviour_builder: BehaviourBuilder """
    match_ready_behaviour_builder()
    return match_ready_behaviour_builder


def test_subsequent_access_throws_error(behaviour_builder):
    """ :type behaviour_builder: BehaviourBuilder """
    getattr(behaviour_builder, 'first_time_attribute_access')
    with pytest.raises(AttributeError):
        getattr(behaviour_builder, 'subsequent_attribute_access')


def test_behaviour_builder_is_not_callable_after_match_criteria_recorded(result_ready_behaviour_builder):
    """ :type result_ready_behaviour_builder: BehaviourBuilder """
    with pytest.raises(TypeError):
        result_ready_behaviour_builder()


def test_getitem_sets_name_to_getitem(behaviour_builder):
    """ :type behaviour_builder: BehaviourBuilder """
    behaviour_builder[0]

    assert behaviour_builder.behaviour.name == '__getitem__'


def test_getitem_sets_match_criteria(behaviour_builder):
    """ :type behaviour_builder: BehaviourBuilder """
    behaviour_builder[27]

    assert behaviour_builder.behaviour.match_criteria == MatchCriteria(args=(27,), kwargs={})


def test_getitem_passes_back_behaviour_builer(behaviour_builder):
    """ :type behaviour_builder: BehaviourBuilder """
    assert behaviour_builder[0] == behaviour_builder


def test_getitem_throws_error_after_name_has_been_defined(result_ready_behaviour_builder):
    """ :type result_ready_behaviour_builder: BehaviourBuilder """
    with pytest.raises(TypeError):
        result_ready_behaviour_builder[0]


def test_then_return_passes_back_behaviour_builder(result_ready_behaviour_builder):
    """ :type result_ready_behaviour_builder: BehaviourBuilder """
    assert result_ready_behaviour_builder.then_return('something') == result_ready_behaviour_builder


def test_then_raise_passes_back_behaviour_builder(result_ready_behaviour_builder):
    """ :type result_ready_behaviour_builder: BehaviourBuilder """
    assert result_ready_behaviour_builder.then_raise(Exception) == result_ready_behaviour_builder


def test_then_compute_passes_back_behaviour_builder(result_ready_behaviour_builder):
    """ :type result_ready_behaviour_builder: BehaviourBuilder """
    assert result_ready_behaviour_builder.then_compute(lambda *_, **__: None) == result_ready_behaviour_builder


def test_error_result_raises_exception():
    class CustomException(Exception):
        pass
    behaviour = Behaviour()
    behaviour.add_result(ErrorResult(CustomException))
    with pytest.raises(CustomException):
        behaviour.get_result()


def test_get_result_rotates_through_behaviours():
    behaviour = Behaviour()
    behaviour.add_result(ValueResult('first'))
    behaviour.add_result(ValueResult('second'))
    assert behaviour.get_result() == 'first'
    assert behaviour.get_result() == 'second'
    assert behaviour.get_result() == 'second'
