import pytest

from pock.expectation import ExpectationBuilder, Expectation, ErrorResult
from pock.mock import Mock


@pytest.fixture
def mock():
    return Mock()


@pytest.fixture
def method_name():
    return 'method'


@pytest.fixture
def expectation():
    return Expectation()


@pytest.fixture
def expectation_builder(mock, expectation):
    """ :type mock: Mock """
    return ExpectationBuilder(mock, expectation=expectation)


@pytest.fixture
def match_ready_expectation_builder(expectation_builder, method_name):
    """ :type expectation_builder: ExpectationBuilder """
    getattr(expectation_builder, method_name)
    return expectation_builder


@pytest.fixture
def result_ready_expectation_builder(match_ready_expectation_builder):
    """ :type match_ready_expectation_builder: ExpectationBuilder """
    match_ready_expectation_builder()
    return match_ready_expectation_builder


def test_first_attribute_access_defines_name(expectation_builder, method_name):
    """ :type expectation_builder: ExpectationBuilder """
    getattr(expectation_builder, method_name)

    assert expectation_builder.expectation.name == method_name


def test_subsequent_attribute_access_does_not_override_name(expectation_builder, method_name):
    """ :type expectation_builder: ExpectationBuilder """
    getattr(expectation_builder, method_name)
    getattr(expectation_builder, 'name_defined')

    assert expectation_builder.expectation.name == method_name


def test_calling_expectation_builder_before_defining_name_sets_name_as_call(expectation_builder):
    """ :type expectation_builder: ExpectationBuilder """
    expectation_builder()

    assert expectation_builder.expectation.name == '__call__'


def test_calling_expectation_builder_before_defining_name_adds_expectation_to_mock(expectation_builder, mock):
    """
    :type expectation_builder: ExpectationBuilder
    :type mock: Mock
    """
    expectation_builder()

    assert expectation_builder.expectation in mock._call_expectations


def test_expectation_builder_adds_expectation_to_sub_mock_when_called(match_ready_expectation_builder, mock, method_name):
    """
    :type match_ready_expectation_builder: ExpectationBuilder
    :type mock: Mock
    """
    match_ready_expectation_builder()

    assert match_ready_expectation_builder.expectation in getattr(mock, method_name)._call_expectations


def test_defining_a_result_without_defining_match_criteria_will_create_a_property(expectation_builder, mock):
    """
    :type expectation_builder: ExpectationBuilder
    :type mock: Mock
    """
    expectation_builder.property.then_return(5)

    assert expectation_builder.expectation == mock._property_expectations[expectation_builder.expectation.name]


def test_then_raise_adds_error_result_to_expectation(result_ready_expectation_builder, expectation):
    """
    :type result_ready_expectation_builder: ExpectationBuilder
    :type expectation: Expectation
    """
    class CustomException(Exception):
        pass

    exception = CustomException()
    result_ready_expectation_builder.then_raise(exception)

    assert ErrorResult(exception) in expectation.results

