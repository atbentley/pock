import pytest

from pock.behaviour import BehaviourBuilder, Behaviour, ErrorResult, ComputationResult
from pock.mock import Mock


@pytest.fixture
def mock():
    return Mock()


@pytest.fixture
def method_name():
    return 'method'


@pytest.fixture
def behaviour():
    return Behaviour()


@pytest.fixture
def behaviour_builder(mock, behaviour):
    """ :type mock: Mock """
    return BehaviourBuilder(mock, behaviour=behaviour)


@pytest.fixture
def match_ready_behaviour_builder(behaviour_builder, method_name):
    """ :type behaviour_builder: BehaviourBuilder """
    getattr(behaviour_builder, method_name)
    return behaviour_builder


@pytest.fixture
def result_ready_behaviour_builder(match_ready_behaviour_builder):
    """ :type match_ready_behaviour_builder: BehaviourBuilder """
    match_ready_behaviour_builder()
    return match_ready_behaviour_builder


def test_first_attribute_access_defines_name(behaviour_builder, method_name):
    """ :type behaviour_builder: BehaviourBuilder """
    getattr(behaviour_builder, method_name)

    assert behaviour_builder.behaviour.name == method_name


def test_subsequent_attribute_access_does_not_override_name(behaviour_builder, method_name):
    """ :type behaviour_builder: BehaviourBuilder """
    getattr(behaviour_builder, method_name)
    getattr(behaviour_builder, 'name_defined')

    assert behaviour_builder.behaviour.name == method_name


def test_calling_behaviour_builder_before_defining_name_sets_name_as_call(behaviour_builder):
    """ :type behaviour_builder: BehaviourBuilder """
    behaviour_builder()

    assert behaviour_builder.behaviour.name == '__call__'


def test_calling_behaviour_builder_before_defining_name_adds_behaviour_to_mock(behaviour_builder, mock):
    """
    :type behaviour_builder: BehaviourBuilder
    :type mock: Mock
    """
    behaviour_builder()

    assert behaviour_builder.behaviour in mock._call_behaviours.values()


def test_behaviour_builder_adds_behaviour_to_sub_mock_when_called(match_ready_behaviour_builder, mock, method_name):
    """
    :type match_ready_behaviour_builder: BehaviourBuilder
    :type mock: Mock
    """
    match_ready_behaviour_builder()

    assert match_ready_behaviour_builder.behaviour in getattr(mock, method_name)._call_behaviours.values()


def test_defining_a_result_without_defining_match_criteria_will_create_a_property(behaviour_builder, mock):
    """
    :type behaviour_builder: BehaviourBuilder
    :type mock: Mock
    """
    behaviour_builder.property.then_return(5)

    assert mock._property_behaviours[behaviour_builder.behaviour.name] == behaviour_builder.behaviour


def test_accessing_item_adds_item_behaviour(behaviour_builder, mock):
    """
    :type behaviour_builder: BehaviourBuilder
    :type mock: Mock
    """
    behaviour_builder[0].then_return(1)

    assert mock._item_behaviours[behaviour_builder.behaviour.match_criteria] == behaviour_builder.behaviour


def test_then_raise_adds_error_result_to_behaviour(result_ready_behaviour_builder, behaviour):
    """
    :type result_ready_behaviour_builder: BehaviourBuilder
    :type behaviour: Behaviour
    """
    class CustomException(Exception):
        pass

    exception = CustomException()
    result_ready_behaviour_builder.then_raise(exception)

    assert ErrorResult(exception) in behaviour.results


def test_then_compute_adds_computation_result_to_behaviour(result_ready_behaviour_builder, behaviour):
    """
    :type result_ready_behaviour_builder: BehaviourBuilder
    :type behaviour: Behaviour
    """
    def function(*args, **kwargs):
        return None

    result_ready_behaviour_builder.then_compute(function)

    assert ComputationResult(function) in behaviour.results

