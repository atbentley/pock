overrides = (
    '_add_expectation',
    '_add_property',
    '_expectations',
    '_invocations',
    '_property_invocations',
    '_members',
    '_properties'
)


class Mock(object):
    def __init__(self):
        self._expectations = []
        self._invocations = []
        self._property_invocations = []
        self._members = {}
        self._properties = {}

    def _add_expectation(self, expectation):
        self._expectations.append(expectation)

    def _add_property(self, expectation):
        self._properties[expectation.method_name] = expectation

    def __getattribute__(self, name):
        if name in overrides:
            return super(Mock, self).__getattribute__(name)
        elif name in self._properties:
            self._property_invocations.append(name)
            return self._properties[name].result
        elif name in self._members:
            return self._members[name]
        else:
            if name == '__call__':
                sub_mock = self
            else:
                sub_mock = Mock()
            self._members[name] = sub_mock
            return sub_mock

    def __call__(self, *args, **kwargs):
        self._invocations.append((args, kwargs))
        for expectation in self._expectations:
            if expectation.args == args and expectation.kwargs == kwargs:
                return expectation.result
