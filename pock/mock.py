from .expectation import ValueResult, Expectation
from .matchers import MatchCriteria

overrides = (
    '_add_call_expectation',
    '_add_property_expectation',
    '_add_item_expectation',
    '_call_expectations',
    '_property_expectations',
    '_item_expectations',
    '_call_invocations',
    '_property_invocations',
    '_item_invocations',
    '_sub_mocks',
    '__iter__',
    '__repr__',
    '__str__',
    '__class__',
)


class Mock(object):
    def __init__(self):
        self._call_expectations = {}
        self._property_expectations = {}
        self._item_expectations = {}
        self._call_invocations = []
        self._property_invocations = []
        self._item_invocations = []
        self._sub_mocks = {}
        self._item_mocks = {}

    def _add_call_expectation(self, expectation):
        """ :type expectation: Expectation """
        self._call_expectations[expectation.match_criteria] = expectation

    def _add_property_expectation(self, expectation):
        """ :type expectation: Expectation """
        self._property_expectations[expectation.name] = expectation

    def _add_item_expectation(self, expectation):
        """ :type expectation: Expectation """
        self._item_expectations[expectation.match_criteria] = expectation

    def __getattribute__(self, name):
        if name in overrides:
            return super(Mock, self).__getattribute__(name)
        elif name in self._property_expectations:
            self._property_invocations.append(name)
            return self._property_expectations[name].get_result()
        elif name in self._sub_mocks:
            return self._sub_mocks[name]
        else:
            if name == '__call__':
                sub_mock = self
            else:
                sub_mock = Mock()
            self._sub_mocks[name] = sub_mock
            return sub_mock

    def __getitem__(self, item):
        self._item_invocations.append(item)
        for expectation in self._item_expectations.values():
            if expectation.matches((item,), {}):
                return expectation.get_result((item,), {})

        new_mock = Mock()
        new_expectation = Expectation(name='__getitem__',
                                      match_criteria=MatchCriteria(args=(item, ), kwargs={}),
                                      result=ValueResult(new_mock))
        self._add_item_expectation(new_expectation)
        return new_mock

    def __call__(self, *args, **kwargs):
        self._call_invocations.append((args, kwargs))
        for expectation in self._call_expectations.values():
            if expectation.matches(args, kwargs):
                return expectation.get_result(args, kwargs)

        new_mock = Mock()
        new_expectation = Expectation(name='__call__',
                                      match_criteria=MatchCriteria(args=args, kwargs=kwargs),
                                      result=ValueResult(new_mock))
        self._add_call_expectation(new_expectation)
        return new_mock

    def __iter__(self):
        raise NotImplementedError()
