from .matchers import Matcher, MatchCriteria


class VerificationError(Exception):
    pass


class VerificationBuilder(object):
    def __init__(self, mock):
        self.mock = mock
        self.name = None

    def __getattribute__(self, name):
        name_has_been_defined = super(VerificationBuilder, self).__getattribute__('name') is not None
        if not name_has_been_defined:
            self.name = name
            if self.name in self.mock._property_behaviours:
                return self.has_accessed_property()
            else:
                return self.has_been_called_with
        return super(VerificationBuilder, self).__getattribute__(name)

    def __getitem__(self, item):
        name_has_been_defined = super(VerificationBuilder, self).__getattribute__('name') is not None
        if not name_has_been_defined:
            self.name = '__getitem__'
            return self.has_accessed_item(item)
        return super(VerificationBuilder, self)[item]

    def __call__(self, *args, **kwargs):
        name_has_been_defined = super(VerificationBuilder, self).__getattribute__('name') is not None
        if not name_has_been_defined:
            self.name = '__call__'
            return self.has_been_called_with(*args, **kwargs)
        raise TypeError("'{name}' object is not callable".format(name=self.__class__.__name__))

    def has_been_called_with(self, *args, **kwargs):
        sub_mock = getattr(self.mock, self.name)
        values = list(args)
        values.extend(kwargs.values())
        invocations = []
        match_criteria = MatchCriteria(args, kwargs)
        for called_args, called_kwargs in sub_mock._call_invocations:
            if match_criteria.matches(called_args, called_kwargs):
                invocations.append((called_args, called_kwargs))
        if invocations:
            return invocations

        params = []
        params.extend([str(arg) for arg in args])
        params.extend(['{0}={1}'.format(str(item[0]), str(item[1])) for item in kwargs.items()])
        msg = "Expected call to {method}({params}), but no such call was made.".format(
            method=self.name, params=', '.join(params))
        raise VerificationError(msg)

    def has_accessed_property(self):
        count = self.mock._property_invocations.count(self.name)
        if count:
            return [self.name] * count
        else:
            msg = "Expected access to property '{property}', but no such access was made.".format(property=self.name)
            raise VerificationError(msg)

    def has_accessed_item(self, item):
        invocations = []
        match_criteria = MatchCriteria((item,), {})
        for called_item in self.mock._item_invocations:
            if match_criteria.matches((called_item,), {}):
                invocations.append(called_item)
        if invocations:
            return invocations

        msg = "Expected access to item {item}, but no such access was made.".format(item=item)
        raise VerificationError(msg)
