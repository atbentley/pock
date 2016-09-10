overrides = ('_add_expectation', '_expectations', '_members')


class Mock(object):
    def __init__(self):
        self._expectations = []
        self._members = {}

    def _add_expectation(self, expectation):
        self._expectations.append(expectation)

    def __getattribute__(self, name):
        if name in overrides:
            return super(Mock, self).__getattribute__(name)
        elif name in self._members:
            return self._members[name]
        else:
            sub_mock = Mock()
            self._members[name] = sub_mock
            return sub_mock

    def __call__(self, *args, **kwargs):
        for expectation in self._expectations:
            if expectation.args == args and expectation.kwargs == kwargs:
                return expectation.result
