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
            if self.name in self.mock._property_expectations:
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
        if any(isinstance(value, Matcher) for value in values):
            # One of the values is a matcher so we need to construct a match criteria
            match_criteria = MatchCriteria(args, kwargs)
            for called_args, called_kwargs in sub_mock._call_invocations:
                if match_criteria.matches(called_args, called_kwargs):
                    return called_args, called_kwargs
        elif (args, kwargs) in sub_mock._call_invocations:
            # All values are basic values, just compare to the invoked args and kwargs
            return args, kwargs
        else:
            params = []
            params.extend([str(arg) for arg in args])
            params.extend(['{0}={1}'.format(str(item[0]), str(item[1])) for item in kwargs.items()])
            msg = "Expected call to {method}({params}), but no such call was made.".format(
                method=self.name, params=', '.join(params))
            raise VerificationError(msg)

    def has_accessed_property(self):
        if self.name in self.mock._property_invocations:
            return True
        else:
            msg = "Expected access to property '{property}', but no such access was made.".format(property=self.name)
            raise VerificationError(msg)

    def has_accessed_item(self, item):
        if isinstance(item, Matcher):
            match_criteria = MatchCriteria((item,), {})
            for called_item in self.mock._item_invocations:
                if match_criteria.matches((called_item,), {}):
                    return called_item
        elif item in self.mock._item_invocations:
            return item
        else:
            msg = "Expected access to item {item}, but no such access was made.".format(item=item)
            raise VerificationError(msg)
