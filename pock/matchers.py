class Matcher(object):
    def __eq__(self, other):
        raise NotImplemented

    def matches(self, value):
        raise NotImplemented


class ExactValueMatcher(Matcher):
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, ExactValueMatcher):
            return False

        return self.value == other.value

    def matches(self, value):
        return self.value == value


class AnyValueMatcher(Matcher):
    def __eq__(self, other):
        return isinstance(other, AnyValueMatcher)

    def matches(self, value):
        return True


class MatchCriteria(object):
    def __init__(self, args, kwargs):
        arg_matchers = []
        for arg in args:
            if isinstance(arg, Matcher):
                arg_matchers.append(arg)
            else:
                arg_matchers.append(ExactValueMatcher(arg))

        kwarg_matchers = {}
        for key, value in kwargs.items():
            if isinstance(value, Matcher):
                kwarg_matchers[key] = value
            else:
                kwarg_matchers[key] = ExactValueMatcher(value)
        self.arg_matchers = arg_matchers
        self.kwarg_matchers = kwarg_matchers

    def __eq__(self, other):
        if not isinstance(other, MatchCriteria):
            return False

        return self.arg_matchers == other.arg_matchers and self.kwarg_matchers == other.kwarg_matchers

    def __hash__(self):
        return hash(tuple(self.arg_matchers)) + hash(tuple(sorted(self.kwarg_matchers.items())))

    def matches(self, args, kwargs):
        if len(self.arg_matchers) != len(args) or set(self.kwarg_matchers.keys()) != set(kwargs.keys()):
            return False

        for i in range(len(self.arg_matchers)):
            if not self.arg_matchers[i].matches(args[i]):
                return False

        for key, kwarg_matcher in self.kwarg_matchers.items():
            if not kwarg_matcher.matches(kwargs[key]):
                return False

        return True
