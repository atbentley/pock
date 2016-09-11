overrides = (
    '_add_call_expectation',
    '_add_property_expectation',
    '_call_expectations',
    '_property_expectations',
    '_call_invocations',
    '_property_invocations',
    '_sub_mocks'
)


class Mock(object):
    def __init__(self):
        self._call_expectations = []
        self._property_expectations = {}
        self._call_invocations = []
        self._property_invocations = []
        self._sub_mocks = {}

    def _add_call_expectation(self, expectation):
        """ :type expectation: Expectation """
        self._call_expectations.append(expectation)

    def _add_property_expectation(self, expectation):
        """ :type expectation: Expectation """
        self._property_expectations[expectation.name] = expectation

    def __getattribute__(self, name):
        if name in overrides:
            return super(Mock, self).__getattribute__(name)
        elif name in self._property_expectations:
            self._property_invocations.append(name)
            return self._property_expectations[name].result
        elif name in self._sub_mocks:
            return self._sub_mocks[name]
        else:
            if name == '__call__':
                sub_mock = self
            else:
                sub_mock = Mock()
            self._sub_mocks[name] = sub_mock
            return sub_mock

    def __call__(self, *args, **kwargs):
        self._call_invocations.append((args, kwargs))
        for expectation in self._call_expectations:
            if expectation.args == args and expectation.kwargs == kwargs:
                return expectation.result
