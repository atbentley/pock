import pytest

from pock.expectation import ExpectationBuilder, Expectation
from pock.mock import Mock


@pytest.fixture
def mock():
    return Mock()


@pytest.fixture
def method_name():
    return 'method'


@pytest.fixture
def expectation_builder(mock):
    """ :type mock: Mock """
    return ExpectationBuilder(mock)


@pytest.fixture
def callable_expectation_builder(mock, method_name):
    """ :type mock: Mock """
    return ExpectationBuilder(mock, expectation=Expectation(method_name, None, None, None))


def test_first_attribute_access_defines_method_name(expectation_builder, method_name):
    """ :type expectation_builder: ExpectationBuilder """
    getattr(expectation_builder, method_name)

    assert expectation_builder.expectation.method_name == method_name


def test_subsequent_attribute_access_does_not_override_method_name(expectation_builder, method_name):
    """ :type expectation_builder: ExpectationBuilder """
    getattr(expectation_builder, method_name)
    getattr(expectation_builder, 'method_name_defined')

    assert expectation_builder.expectation.method_name == method_name


def test_expectation_builder_records_args_and_kwargs_when_called(callable_expectation_builder):
    """ :type callable_expectation_builder: ExpectationBuilder """
    args = (1, 5, 2, 7)
    kwargs = {'a': 43, 'b': 5, 'd5g': 33}

    callable_expectation_builder(*args, **kwargs)

    assert callable_expectation_builder.expectation.args == args
    assert callable_expectation_builder.expectation.kwargs == kwargs


def test_expectation_builder_adds_expectation_to_sub_mock_when_called(callable_expectation_builder, mock, method_name):
    """
    :type callable_expectation_builder: ExpectationBuilder
    :type mock: Mock
    """
    callable_expectation_builder()

    assert callable_expectation_builder.expectation in getattr(mock, method_name)._expectations
