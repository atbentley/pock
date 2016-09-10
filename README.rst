Pock
====

Pock is a python mocking framework.


Installation
------------

```
pip install pock
```


Usage
-----

```
from pock import when, Mock

my_mock = Mock()
when(my_mock).something(1).then_return('a')
when(my_mock).something(2).then_return('b')

my_mock.something(1)  # 'a'
my_mock.something(2)  # 'b'
my_mock.something()  # None
my_mock.something_else()  # None

verify(my_mock).something(1)  # True
verify(my_mock).other()  # VerificationError
```


Testing
-------

```
pip install -r requirements.txt -r build-requirements.txt
py.test tests
```


License
-------

MIT
