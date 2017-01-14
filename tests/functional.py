import pytest

from pock import any_values
from pock import mock, when, verify, any_value, VerificationError


def test_mocking_a_method():
    method_mock = mock()
    when(method_mock).some_method('some_arg').then_return('some_value')
    assert method_mock.some_method('some_arg') == 'some_value'
    verify(method_mock).some_method('some_arg')


def test_mocking_a_top_level_function():
    function_mock = mock()
    when(function_mock)('something').then_return('some_result')
    assert function_mock('something') == 'some_result'
    verify(function_mock)('something')


def test_mocking_a_property():
    property_mock = mock()
    when(property_mock).some_property.then_return('a_result')
    assert property_mock.some_property == 'a_result'
    verify(property_mock).some_property


def test_behaviours_using_matchers():
    some_mock = mock()
    when(some_mock).method(1, any_value, a=3, b=any_value).then_return('a_value')
    assert some_mock.method(1, 2, a=3, b=4) == 'a_value'
    assert some_mock.method(1, 'anything', a=3, b='blah') == 'a_value'
    verify(some_mock).method(1, 2, a=3, b=4)
    verify(some_mock).method(1, 'anything', a=3, b='blah')
    with pytest.raises(VerificationError):
        verify(some_mock).method(1, 'no', a=3, b='no')


def test_verifications_using_matchers():
    some_mock = mock()
    when(some_mock).a_method(1, any_value, a=any_value).then_return('value')
    some_mock.a_method(1, 2, a=5)
    verify(some_mock).a_method(any_value, 2, a=any_value)


def test_raising_errors():
    error_mock = mock()
    when(error_mock).some_method().then_raise(Exception)
    with pytest.raises(Exception):
        error_mock.some_method()


def test_chaining_results():
    chained_mock = mock()
    when(chained_mock).something().then_return(1).then_raise(Exception).then_return(2)
    assert chained_mock.something() == 1
    with pytest.raises(Exception):
        chained_mock.something()
    assert chained_mock.something() == 2
    assert chained_mock.something() == 2


def test_failed_verification():
    some_mock = mock()
    with pytest.raises(VerificationError):
        verify(some_mock).some_method()
    with pytest.raises(VerificationError):
        verify(some_mock).some_method(any_values)
    with pytest.raises(VerificationError):
        verify(some_mock).some_method(1)
    with pytest.raises(VerificationError):
        verify(some_mock)[1]
    with pytest.raises(VerificationError):
        verify(some_mock)[any_values]
