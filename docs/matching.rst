Matching
========

When defining behaviours or verifying interactions for methods, functions or item access matchers can be used instead of fixed arguments.

Matchers can be used in the following locations.

.. code-block:: python

  when(my_mock).method(matcher1, key=matcher2)
  when(my_mock)(matcher1, key=matcher2)
  when(my_mock)[matcher]

  verify(my_mock).method(matcher1, key=matcher2)
  verify(my_mock)(matcher1, key=matcher2)
  verify(my_mock)[matcher]


Note that methods and functions can accepts an arbitrary amount of positional argument matchers and keyword argument matchers, however item access can only use a single matcher.

Built-in matchers
-----------------

any_value
^^^^^^^^^

Matches any positional argument or keyword argument depending on where it is used.

.. code-block:: python

  when(my_mock).a_method('first', any_value).then_return(1)
  my_mock.a_method('first', 'python')  # 1
  my_mock.a_method('second', None)  # None

  when(my_mock).b_method('first', season=any_value).then_return(2)
  my_mock.b_method('first', season='winter')  # 2
  my_mock.b_method('first')  # None


any_args
^^^^^^^^

Matches all positional arguments, regardless of how many there are.

.. code-block:: python

  when(my_mock).a_method('first', any_value).then_return(1)
  my_mock.a_method('first', 'python')  # 1
  my_mock.a_method('second', None)  # None

  when(my_mock).b_method('first', season=any_value).then_return(2)
  my_mock.b_method('first', season='winter')  # 2
  my_mock.b_method('first')  # None


any_kwargs
^^^^^^^^^^

Matches all keyword arguments, regardless of how many there are, what their keys are and what their values.

any_values
^^^^^^^^^^

Effectively a combination of any_args and any_kwargs.

ExactValueMatcher
^^^^^^^^^^^^^^^^^

Matches a value exactly, any values used when building behaviours of verifying interactions that aren't matchers are converted into ExactValueMatcher's behind the scenes.

.. code-block:: python

  # Equivalent
  when(my_mock).method(24).then_return(True)
  when(my_mock).method(ExactValueMatcher(24)).then_return(True)


Custom matchers
---------------

In order for Pock to efficiently determine whether a set of given arguments match a given set of matches, the magic methods __eq__, __ne__ and __hash__ should be implemented according to the following two principals:

1. Two matchers are equal when they always match for the same set of values and also fail to match for the same set of values.
2. If two matchers are equal they should have the same hash


Simple matchers
^^^^^^^^^^^^^^^

Here is an example of matcher that only matches even numbers.

.. code-block:: python

  from pock import Matcher

  class EvenMatcher(Matcher):
      @staticmethod
      def matches(other):
          return hasattr(other, '__mod__') and
            other % 2 == 0

      def __eq__(self, other):
          return isinstance(other, EvenMatcher)

      def __ne__(self, other):
          return not isinstance(other, EvenMatcher)

      def __hash__(self):
          return hash(EvenMatcher)

  even = EvenMatcher()
  when(number_service_mock).is_good_number(even).then_return(True)

For the EvenMatcher, __eq__ is implemented to return True when compared to any other EvenMatcher since they'll always match for the same values.

Because all EvenMatcher's are equal to each other, the hash value is taken from the hash value of the class.

Parametrised matchers
^^^^^^^^^^^^^^^^^^^^^

A more complicated matcher is one that can take parameters, consider a matcher that matches any number if it is divisible by n.

.. code-block:: python

  from pock import matcher

  class DivisibleByN(Matcher):
      def __init__(self, n):
          self.n = n

      def matches(other):
          return (hasattr(other, '__mod__') and
                  other % self.n == 0)

      def __eq__(self, other):
          return (isinstance(other, DivisibleByN) and
                  self.n == other.n)

      def __ne__(self, other):
          return (not isinstance(other, EvenMatcher) or
                  self.n != other.n)

      def __hash__(self):
          return (hash(DivisibleByN) ^
                  hash(self.n) ^
                  hash((DivisibleByN, self.n)))

  divisible_by_7 = DivisibleByN(7)
  when(lucky).is_lucky(divisible_by_7).then_return(True)

Here the DivisibleByN matcher needs to also compare the value of n in __eq__ and __ne__ and likewise, the value of n is included in the hash function.
