class VerificationError(Exception):
    pass


class VerificationBuilder(object):
    def __init__(self, mock):
        self.mock = mock
        self.method_name = None

    def __getattribute__(self, name):
        method_name_has_been_defined = super(VerificationBuilder, self).__getattribute__('method_name') is not None
        if not method_name_has_been_defined:
            self.method_name = name
            if self.method_name in self.mock._properties:
                return self.has_accessed_property()
            else:
                return self.has_been_called_with
        return super(VerificationBuilder, self).__getattribute__(name)

    def __call__(self, *args, **kwargs):
        method_name_has_been_defined = super(VerificationBuilder, self).__getattribute__('method_name') is not None
        if not method_name_has_been_defined:
            self.method_name = '__call__'
            return self.has_been_called_with(*args, **kwargs)
        raise TypeError("'{name}' object is not callable".format(name=self.__class__.__name__))

    def has_been_called_with(self, *args, **kwargs):
        sub_mock = getattr(self.mock, self.method_name)
        if (args, kwargs) in sub_mock._invocations:
            return True
        else:
            params = []
            params.extend([str(arg) for arg in args])
            params.extend(['{0}={1}'.format(str(item[0]), str(item[1])) for item in kwargs.items()])
            msg = "Expected call to {method}({params}), but no such call was made.".format(
                method=self.method_name, params=', '.join(params))
            raise VerificationError(msg)

    def has_accessed_property(self):
        if self.method_name in self.mock._property_invocations:
            return True
        else:
            msg = "Expected access to property '{property}', but no such access was made.".format(
                property=self.method_name)
            raise VerificationError(msg)
