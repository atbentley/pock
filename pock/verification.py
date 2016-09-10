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
            return self.has_been_called_with
        return super(VerificationBuilder, self).__getattribute__(name)

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
