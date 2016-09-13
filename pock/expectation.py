class Expectation(object):
    def __init__(self, name=None, args=None, kwargs=None, result=None):
        self.name = name
        self.args = args
        self.kwargs = kwargs
        self.results = []
        self.result_index = 0
        if result:
            self.results.append(ValueResult(result))

    def get_result(self):
        result = self.results[self.result_index].get_result()
        if self.result_index != len(self.results) - 1:
            self.result_index += 1
        return result

    def add_result(self, result):
        self.results.append(result)


class ValueResult(object):
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, ValueResult) and self.value == other.value

    def get_result(self):
        return self.value


class ErrorResult(object):
    def __init__(self, exception):
        self.exception = exception

    def __eq__(self, other):
        return isinstance(other, ErrorResult) and self.exception == other.exception

    def get_result(self):
        raise self.exception


class ExpectationBuilder(object):
    def __init__(self, mock, expectation=None):
        """ :type expectation: Expectation """
        self.mock = mock
        expectation = expectation or Expectation(None, None, None, None)
        self.expectation = expectation
        self.name_defined = expectation.name is not None
        self.match_criteria_defined = expectation.args is not None

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

    def define_expectation_name(self, name):
        self.expectation.name = name

    def define_match_criteria(self, args, kwargs):
        self.expectation.args = args
        self.expectation.kwargs = kwargs
        getattr(self.mock, self.expectation.name)._add_call_expectation(self.expectation)

    def then_return(self, value):
        if not self.match_criteria_defined:
            self.match_criteria_defined = True
            self.mock._add_property_expectation(self.expectation)
        self.expectation.add_result(ValueResult(value))
        return self

    def then_raise(self, exception):
        if not self.match_criteria_defined:
            self.match_criteria_defined = True
            self.mock._add_property_expectation(self.expectation)
        self.expectation.add_result(ErrorResult(exception))
        return self
