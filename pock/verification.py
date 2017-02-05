from .matchers import MatchCriteria


class VerificationError(Exception):
    pass


class VerificationBuilder(object):
    def __init__(self, mock, test, msg):
        self.mock = mock
        self.test = test
        self.msg = msg
        self.name = None

    def passes_test(self, results):
        return not self.test or self.test(results)

    def get_error_message(self, access, accesses, thing, amount):
        were_was = 'was' if amount == 1 else 'were'
        return self.msg.format(access=access, accesses=accesses, thing=thing, amount=amount, were_was=were_was)

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
        if self.passes_test(invocations):
            return invocations
        else:
            params = []
            params.extend([str(arg) for arg in args])
            params.extend(['{0}={1}'.format(str(item[0]), str(item[1])) for item in kwargs.items()])
            thing = '{method}({params})'.format(method=self.name, params=', '.join(params))
            msg = self.get_error_message('call', 'calls', thing, len(invocations))
            raise VerificationError(msg)

    def has_accessed_property(self):
        count = self.mock._property_invocations.count(self.name)
        invocations = [self.name] * count
        if self.passes_test(invocations):
            return invocations
        else:
            msg = self.get_error_message('access', 'accesses', 'property {0}'.format(self.name), count)
            raise VerificationError(msg)

    def has_accessed_item(self, item):
        invocations = []
        match_criteria = MatchCriteria((item,), {})
        for called_item in self.mock._item_invocations:
            if match_criteria.matches((called_item,), {}):
                invocations.append(called_item)
        if self.passes_test(invocations):
            return invocations
        else:
            msg = self.get_error_message('access', 'accesses', 'item {0}'.format(item), len(invocations))
            raise VerificationError(msg)
