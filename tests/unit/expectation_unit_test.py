import pytest

from pock.expectation import ExpectationBuilder


class FakeMock(object):
    def __getattribute__(self, name):
        if name == '_add_expectation':
            return lambda _: None
        return self


@pytest.fixture
def fake_mock():
    return FakeMock()


@pytest.fixture
def expectation_builder(fake_mock):
    """ :type fake_mock: Mock """
    return ExpectationBuilder(fake_mock)


@pytest.fixture
def callable_expectation_builder(expectation_builder):
    """ :type expectation_builder: ExpectationBuilder """
    getattr(expectation_builder, 'first_time_attribute_access')
    return expectation_builder


def test_subsequent_access_throws_error(expectation_builder):
    """ :type expectation_builder: ExpectationBuilder """
    getattr(expectation_builder, 'first_time_attribute_access')
    with pytest.raises(AttributeError):
        getattr(expectation_builder, 'subsequent_attribute_access')


def test_expectation_builder_is_not_callable_after_match_criteria_recorded(callable_expectation_builder):
    """ :type callable_expectation_builder: ExpectationBuilder """
    callable_expectation_builder()
    with pytest.raises(TypeError):
        callable_expectation_builder()
