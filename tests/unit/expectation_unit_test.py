import pytest

from pock.expectation import ExpectationBuilder, Expectation, ErrorResult, ValueResult
from pock.matchers import MatchCriteria


class FakeMock(object):
    def __getattribute__(self, name):
        if name in ['_add_call_expectation', '_add_item_expectation']:
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
def match_ready_expectation_builder(expectation_builder):
    """ :type expectation_builder: ExpectationBuilder """
    getattr(expectation_builder, 'first_time_attribute_access')
    return expectation_builder


@pytest.fixture
def result_ready_expectation_builder(match_ready_expectation_builder):
    """ :type match_ready_expectation_builder: ExpectationBuilder """
    match_ready_expectation_builder()
    return match_ready_expectation_builder


def test_subsequent_access_throws_error(expectation_builder):
    """ :type expectation_builder: ExpectationBuilder """
    getattr(expectation_builder, 'first_time_attribute_access')
    with pytest.raises(AttributeError):
        getattr(expectation_builder, 'subsequent_attribute_access')


def test_expectation_builder_is_not_callable_after_match_criteria_recorded(result_ready_expectation_builder):
    """ :type result_ready_expectation_builder: ExpectationBuilder """
    with pytest.raises(TypeError):
        result_ready_expectation_builder()


def test_getitem_sets_name_to_getitem(expectation_builder):
    """ :type expectation_builder: ExpectationBuilder """
    expectation_builder[0]

    assert expectation_builder.expectation.name == '__getitem__'


def test_getitem_sets_match_criteria(expectation_builder):
    """ :type expectation_builder: ExpectationBuilder """
    expectation_builder[27]

    assert expectation_builder.expectation.match_criteria == MatchCriteria(args=(27,), kwargs={})


def test_getitem_passes_back_expectation_builer(expectation_builder):
    """ :type expectation_builder: ExpectationBuilder """
    assert expectation_builder[0] == expectation_builder


def test_getitem_throws_error_after_name_has_been_defined(result_ready_expectation_builder):
    """ :type result_ready_expectation_builder: ExpectationBuilder """
    with pytest.raises(TypeError):
        result_ready_expectation_builder[0]


def test_then_return_passes_back_expectation_builder(result_ready_expectation_builder):
    """ :type result_ready_expectation_builder: ExpectationBuilder """
    assert result_ready_expectation_builder.then_return('something') == result_ready_expectation_builder


def test_then_raise_passes_back_expectation_builder(result_ready_expectation_builder):
    """ :type result_ready_expectation_builder: ExpectationBuilder """
    assert result_ready_expectation_builder.then_raise(Exception) == result_ready_expectation_builder


def test_then_compute_passes_back_expectation_builder(result_ready_expectation_builder):
    """ :type result_ready_expectation_builder: ExpectationBuilder """
    assert result_ready_expectation_builder.then_compute(lambda *_, **__: None) == result_ready_expectation_builder


def test_error_result_raises_exception():
    class CustomException(Exception):
        pass
    expectation = Expectation()
    expectation.add_result(ErrorResult(CustomException))
    with pytest.raises(CustomException):
        expectation.get_result()


def test_get_result_rotates_through_expectations():
    expectation = Expectation()
    expectation.add_result(ValueResult('first'))
    expectation.add_result(ValueResult('second'))
    assert expectation.get_result() == 'first'
    assert expectation.get_result() == 'second'
    assert expectation.get_result() == 'second'
