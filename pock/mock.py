from collections import OrderedDict

from .behaviour import ValueResult, Behaviour
from .matchers import MatchCriteria


overrides = (
    '_spec',
    '_strict',
    '_add_call_behaviour',
    '_add_property_behaviour',
    '_add_item_behaviour',
    '_add_method_behaviour',
    '_call_behaviours',
    '_property_behaviours',
    '_item_behaviours',
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
    def __init__(self, spec=None, strict=False):
        self._spec = spec or []
        self._strict = strict or bool(spec)
        self._call_behaviours = OrderedDict()
        self._property_behaviours = OrderedDict()
        self._item_behaviours = OrderedDict()
        self._call_invocations = []
        self._property_invocations = []
        self._item_invocations = []
        self._sub_mocks = OrderedDict()
        self._item_mocks = OrderedDict()

    def _add_call_behaviour(self, behaviour):
        self._call_behaviours[behaviour.match_criteria] = behaviour

    def _add_property_behaviour(self, behaviour):
        self._property_behaviours[behaviour.name] = behaviour

    def _add_item_behaviour(self, behaviour):
        self._item_behaviours[behaviour.match_criteria] = behaviour

    def _add_method_behaviour(self, behaviour):
        if behaviour.name not in self._sub_mocks:
            if behaviour.name == '__call__':
                sub_mock = self
            else:
                sub_mock = Mock(strict=self._strict)
            self._sub_mocks[behaviour.name] = sub_mock
        self._sub_mocks[behaviour.name]._add_call_behaviour(behaviour)

    def __getattribute__(self, name):
        if name in overrides:
            return super(Mock, self).__getattribute__(name)
        elif name in self._property_behaviours:
            self._property_invocations.append(name)
            return self._property_behaviours[name].get_result()
        elif name in self._sub_mocks:
            return self._sub_mocks[name]
        else:
            if self._strict and name not in self._spec:
                return super(Mock, self).__getattribute__(name)
            else:
                if name == '__call__':
                    sub_mock = self
                else:
                    sub_mock = Mock()
                self._sub_mocks[name] = sub_mock
                return sub_mock

    def __enter__(self,):
        return getattr(self, '__enter__')()

    def __exit__(self, *args):
        return getattr(self, '__exit__')(*args)

    def __getitem__(self, item):
        self._item_invocations.append(item)
        for behaviour in self._item_behaviours.values():
            if behaviour.matches((item,), {}):
                return behaviour.get_result((item,), {})

        if self._strict:
            raise TypeError("'Mock' object has no attribute '__getitem__'")
        else:
            new_mock = Mock()
            new_behaviour = Behaviour(
                name='__getitem__',
                match_criteria=MatchCriteria(args=(item, ), kwargs={}),
                result=ValueResult(new_mock))
            self._add_item_behaviour(new_behaviour)
            return new_mock

    def __call__(self, *args, **kwargs):
        self._call_invocations.append((args, kwargs))
        for behaviour in self._call_behaviours.values():
            if behaviour.matches(args, kwargs):
                return behaviour.get_result(args, kwargs)

        if self._strict:
            raise TypeError("'Mock' object is not callable")

        else:
            new_mock = Mock()
            new_behaviour = Behaviour(
                name='__call__',
                match_criteria=MatchCriteria(args=args, kwargs=kwargs),
                result=ValueResult(new_mock))
            self._add_call_behaviour(new_behaviour)
            return new_mock

    def __iter__(self):
        raise NotImplementedError()
