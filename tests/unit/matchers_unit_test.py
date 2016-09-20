import pytest

from pock.matchers import ExactValueMatcher, AnyValueMatcher, Matcher, MatchCriteria


def test_base_matcher():
    matcher = Matcher()

    with pytest.raises(NotImplementedError):
        matcher == 1

    with pytest.raises(NotImplementedError):
        matcher != 1

    with pytest.raises(NotImplementedError):
        hash(matcher)

    with pytest.raises(NotImplementedError):
        matcher.matches(None)


def test_exact_value_matcher_equality():
    matcher1 = ExactValueMatcher(15)
    matcher2 = ExactValueMatcher(15)

    assert matcher1 == matcher2


def test_exact_value_matcher_inequality():
    matcher1 = ExactValueMatcher(10)
    matcher2 = ExactValueMatcher(15)
    matcher3 = AnyValueMatcher()

    assert matcher1 != matcher2
    assert matcher1 != matcher3


def test_exact_value_hashes():
    matcher1 = ExactValueMatcher(15)
    matcher2 = ExactValueMatcher(15)

    assert hash(matcher1) == hash(matcher2)


def test_exact_value_matcher_matching():
    matcher = ExactValueMatcher(12)

    assert matcher.matches(12)
    assert not matcher.matches(13)


def test_any_value_matcher_equality():
    matcher1 = AnyValueMatcher()
    matcher2 = AnyValueMatcher()

    assert matcher1 == matcher2


def test_any_value_matcher_inequality():
    matcher1 = AnyValueMatcher()
    matcher2 = ExactValueMatcher(10)

    assert matcher1 != matcher2


def test_any_value_hashes():
    matcher1 = AnyValueMatcher()
    matcher2 = AnyValueMatcher()

    assert hash(matcher1) == hash(matcher2)


def test_any_value_matching():
    matcher = AnyValueMatcher()

    assert matcher.matches(10)
    assert matcher.matches('anything')


def test_match_criteria_converts_non_matcher_args_to_exact_value_matchers():
    match_criteria = MatchCriteria((1, ExactValueMatcher(2)), {'a': 1, 'b': ExactValueMatcher(2)})

    assert all([isinstance(arg, ExactValueMatcher) for arg in match_criteria.arg_matchers])
    assert all([isinstance(arg, ExactValueMatcher) for arg in match_criteria.kwarg_matchers.values()])


def test_match_criteria_equality():
    match_criteria1 = MatchCriteria((1, 5, 3), {'fd': 43, 'asd': 54})
    match_criteria2 = MatchCriteria((1, 5, 3), {'fd': 43, 'asd': 54})

    assert match_criteria1 == match_criteria2


def test_match_criteria_inequality():
    match_criteria1 = MatchCriteria((1, 5, 3), {'fd': 43, 'asd': 54})
    match_criteria2 = MatchCriteria((2, 4, 3), {'fd': 43, 'asd': 54})
    match_criteria3 = False

    assert match_criteria1 != match_criteria2
    assert match_criteria2 != match_criteria3


def test_match_criteria_hash():
    match_criteria1 = MatchCriteria((1, 5, 3), {'fd': 43, 'asd': 54})
    match_criteria2 = MatchCriteria((1, 5, 3), {'fd': 43, 'asd': 54})

    assert hash(match_criteria1) == hash(match_criteria2)


def test_match_criteria_does_not_match_if_args_mismatch():
    match_criteria = MatchCriteria((1,), {})

    assert not match_criteria.matches((2,), {})


def test_match_criteria_does_not_match_if_kwargs_mismatch():
    match_criteria = MatchCriteria((), {'a': 1})

    assert not match_criteria.matches((), {'a': 2})


def test_match_criteria_returns_true_when_matching():
    match_criteria = MatchCriteria((1,), {'a': 1})

    assert match_criteria.matches((1,), {'a': 1})


def test_match_criteria_does_not_match_when_args_length_mismatch():
    match_criteria = MatchCriteria((1,), {})

    assert not match_criteria.matches((1, 2), {})
