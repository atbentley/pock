from functools import partial

from .matchers import MatchCriteria

try:
    import asyncio
except ImportError:
    asyncio = None


class Expectation(object):
    def __init__(self, name=None, match_criteria=None, result=None):
        self.name = name
        self.match_criteria = match_criteria
        self.results = []
        self.result_index = 0
        if result:
            self.results.append(result)

    def get_result(self, args=None, kwargs=None):
        result = self.results[self.result_index]
        if self.result_index != len(self.results) - 1:
            self.result_index += 1
        return result.get_result(args or [], kwargs or {})

    def add_result(self, result):
        self.results.append(result)

    def set_match_criteria(self, match_criteria):
        """ :type match_criteria: MatchCriteria """
        self.match_criteria = match_criteria

    def matches(self, args, kwargs):
        return self.match_criteria.matches(args, kwargs)


class Result(object):
    def __init__(self, async=False):
        self.async = async

    def _get_result(self, args, kwargs):
        raise NotImplementedError()

    def get_result(self, args, kwargs):
        if self.async:
            return asyncio.coroutine(partial(self._get_result, args, kwargs))()
        else:
            return self._get_result(args, kwargs)


class ValueResult(Result):
    def __init__(self, value, async=False):
        super(ValueResult, self).__init__(async)
        self.value = value

    def __eq__(self, other):
        return isinstance(other, ValueResult) and self.value == other.value

    def _get_result(self, args, kwargs):
        return self.value


class ErrorResult(Result):
    def __init__(self, exception, async=False):
        super(ErrorResult, self).__init__(async)
        self.exception = exception

    def __eq__(self, other):
        return isinstance(other, ErrorResult) and self.exception == other.exception

    def _get_result(self, args, kwargs):
        raise self.exception


class ComputationResult(Result):
    def __init__(self, function, async=False):
        super(ComputationResult, self).__init__(async)
        self.function = function

    def __eq__(self, other):
        return isinstance(other, ComputationResult) and self.function == other.function

    def _get_result(self, args, kwargs):
        return self.function(*args, **kwargs)


class ExpectationBuilder(object):
    def __init__(self, mock, expectation=None, async=False):
        """ :type expectation: Expectation """
        if async and not asyncio:
            raise RuntimeError('Can only use async feature with Python 3.5+')
        self.mock = mock
        self.async = async
        expectation = expectation or Expectation()
        self.expectation = expectation
        self.name_defined = expectation.name is not None
        self.match_criteria_defined = expectation.match_criteria is not None

    def __getattribute__(self, name):
        name_has_been_defined = super(ExpectationBuilder, self).__getattribute__('name_defined')
        if not name_has_been_defined:
            self.name_defined = True
            self.define_expectation_name(name)
            return self
        return super(ExpectationBuilder, self).__getattribute__(name)

    def __call__(self, *args, **kwargs):
        name_has_been_defined = super(ExpectationBuilder, self).__getattribute__('name_defined')
        if not name_has_been_defined:
            self.name_defined = True
            self.define_expectation_name('__call__')

        match_criteria_has_been_defined = super(ExpectationBuilder, self).__getattribute__('match_criteria_defined')
        if not match_criteria_has_been_defined:
            self.match_criteria_defined = True
            self.define_match_criteria(args, kwargs)
            return self

        raise TypeError("'{name}' object is not callable".format(name=self.__class__.__name__))

    def __getitem__(self, item):
        name_has_been_defined = super(ExpectationBuilder, self).__getattribute__('name_defined')
        if not name_has_been_defined:
            self.name_defined = True
            self.define_expectation_name('__getitem__')
            self.match_criteria_defined = True
            self.define_match_criteria((item,), {})
            return self

        raise TypeError("'{name}' object has no attribute __getitem__".format(name=self.__class__.__name__))

    def define_expectation_name(self, name):
        self.expectation.name = name

    def define_match_criteria(self, args, kwargs):
        match_criteria = MatchCriteria(args, kwargs)
        self.expectation.set_match_criteria(match_criteria)
        if self.expectation.name == '__getitem__':
            self.mock._add_item_expectation(self.expectation)
        else:
            getattr(self.mock, self.expectation.name)._add_call_expectation(self.expectation)

    def then_return(self, value):
        self._add_result(ValueResult(value, async=self.async))
        return self

    def then_raise(self, exception):
        self._add_result(ErrorResult(exception, async=self.async))
        return self

    def then_compute(self, function):
        self._add_result(ComputationResult(function, async=self.async))
        return self

    def _add_result(self, result):
        if not self.match_criteria_defined:
            self.match_criteria_defined = True
            self.mock._add_property_expectation(self.expectation)
        self.expectation.add_result(result)
