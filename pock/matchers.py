class Matcher(object):
    def __eq__(self, other):
        raise NotImplementedError

    def __ne__(self, other):
        raise NotImplementedError

    def __hash__(self):
        raise NotImplementedError

    def matches(self, value):
        raise NotImplementedError


class ExactValueMatcher(Matcher):
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, ExactValueMatcher):
            return False

        return self.value == other.value

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.value)

    def matches(self, value):
        return self.value == value


class AnyValueMatcher(Matcher):
    def __eq__(self, other):
        return isinstance(other, AnyValueMatcher)

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(AnyValueMatcher)

    def matches(self, value):
        return True


class AnyArgumentsMatcher(Matcher):
    def __eq__(self, other):
        return isinstance(other, AnyArgumentsMatcher)

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(AnyArgumentsMatcher)

    def matches(self, value):
        return True


class AnyKeywordArgumentsMatcher(Matcher):
    def __eq__(self, other):
        return isinstance(other, AnyKeywordArgumentsMatcher)

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(AnyKeywordArgumentsMatcher)

    def matches(self, value):
        return True


class AnyValuesMatcher(Matcher):
    def __eq__(self, other):
        return isinstance(other, AnyValuesMatcher)

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(AnyValuesMatcher)

    def matches(self, value):
        return True


def make_exact_value_matcher(arg_or_matcher):
    if isinstance(arg_or_matcher, Matcher):
        return arg_or_matcher
    else:
        return ExactValueMatcher(arg_or_matcher)


class MatchCriteria(object):
    def __init__(self, args, kwargs):
        self.arg_matchers = [make_exact_value_matcher(arg) for arg in args]
        self.kwarg_matchers = dict(((key, make_exact_value_matcher(value)) for key, value in kwargs.items()))

        self.any_args = False
        self.any_kwargs = False
        self.any_values = False
        while AnyArgumentsMatcher() in self.arg_matchers:
            self.any_args = True
            self.arg_matchers.remove(AnyArgumentsMatcher())
        while AnyKeywordArgumentsMatcher() in self.arg_matchers:
            self.any_kwargs = True
            self.arg_matchers.remove(AnyKeywordArgumentsMatcher())
        while AnyValuesMatcher() in self.arg_matchers:
            self.any_values = True
            self.arg_matchers.remove(AnyValuesMatcher())

    def __eq__(self, other):
        if not isinstance(other, MatchCriteria):
            return False

        return self.arg_matchers == other.arg_matchers and self.kwarg_matchers == other.kwarg_matchers

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(tuple(self.arg_matchers)) + hash(tuple(sorted(self.kwarg_matchers.items())))

    def matches(self, args, kwargs):
        arg_matchers = self.arg_matchers[:]
        if self.any_args or self.any_values:
            arg_matchers.extend([AnyArgumentsMatcher()] * (len(args) - len(arg_matchers)))

        kwarg_matchers = self.kwarg_matchers
        if self.any_kwargs or self.any_values:
            kwarg_matchers = dict(((key, make_exact_value_matcher(value)) for key, value in kwargs.items()))
            kwarg_matchers.update(self.kwarg_matchers)

        if len(arg_matchers) != len(args) or set(kwarg_matchers.keys()) != set(kwargs.keys()):
            return False

        for i in range(len(arg_matchers)):
            if not arg_matchers[i].matches(args[i]):
                return False

        for key, value in kwargs.items():
            if not kwarg_matchers[key].matches(value):
                return False

        return True
