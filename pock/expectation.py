class Expectation(object):
    def __init__(self, method_name, args, kwargs, result):
        self.method_name = method_name
        self.args = args
        self.kwargs = kwargs
        self.result = result


class ExpectationBuilder(object):
    def __init__(self, mock, expectation=None):
        self._mock = mock
        expectation = expectation or Expectation(None, None, None, None)
        self.expectation = expectation
        self.method_name_defined = expectation.method_name is not None
        self.match_criteria_defined = expectation.args is not None

    def __getattribute__(self, name):
        method_name_has_been_defined = super(ExpectationBuilder, self).__getattribute__('method_name_defined')
        if not method_name_has_been_defined:
            self.method_name_defined = True
            self.define_method_name(name)
            return self
        return super(ExpectationBuilder, self).__getattribute__(name)

    def __call__(self, *args, **kwargs):
        match_criteria_has_been_defined = super(ExpectationBuilder, self).__getattribute__('match_criteria_defined')
        if not match_criteria_has_been_defined:
            self.match_criteria_defined = True
            self.define_match_criteria(args, kwargs)
            return self
        raise TypeError("'{name}' object is not callable")

    def define_method_name(self, method_name):
        self.expectation.method_name = method_name

    def define_match_criteria(self, args, kwargs):
        self.expectation.args = args
        self.expectation.kwargs = kwargs
        sub_mock = getattr(self._mock, self.expectation.method_name)
        sub_mock._add_expectation(self.expectation)
        return self

    def then_return(self, value):
        self.expectation.result = value
