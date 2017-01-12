.. _quickstart:

Quickstart
==========

The basic Pock workflow looks like this:

\1. Create a mock

.. code-block:: python

  from pock import mock, when, verify

  my_mock = mock()


\2. Define some behaviour for that mock

.. code-block:: python


  when(my_mock).hello().then_return('world')


\3. Interact with the mock

.. code-block:: python

  my_mock.hello()  # 'world'


\4. Verify which interactions took place on the mock

.. code-block:: python

  verify(my_mock).hello()  # truthy
  verify(my_mock).something_else()  # Exception


A brief introduction to mocking
-------------------------------

In software testing, a mock is an object which imitates the behaviour of a real object to a certain degree. By substituting the real object for the mock, code can be tested in isolation of other code.

For example, consider the case of a user service which fetches information about a user from a database:

.. code-block:: python

  class Database:
      def select(query, **kwargs):
          pass


  class UserService:
      def __init__(self, database=None):
          self.database = database or Database()

      def get_user_from_email(self, email):
          query = 'select * from users where email = :email'
          data = self.database.select(query, email=email)
          if not data:
              msg = 'No user with email: {0}'.format(email)
              raise UserNotFound(msg)
          name = data[0]['name']
          return User(name, email)


Since get_user_from_email has a dependency on the database, if we wanted to write a unit test for get_user_from_email we would need to replace the real database with a mocked database that returns the same format of data that a real database would, but in a more deterministic way.

Your first test
---------------

Lets actually write some unit tests for the above user service's get_user_from_email method. A standard unit test for this method might check to see that `get_user_from_email` pulls all the right details out of the database response:

.. code-block:: python

  def test_get_user_should_construct_user_from_database_response():
      database = mock()
      when(database).select(any_values).then_return(
          [{'name': 'andrew', 'email': 'andrew@example.come'}])
      user_service = UserService(database=database)

      user = user_service.get_user_from_email('andrew@example.com')

      assert user.name == 'andrew'
      assert user.email = 'andrew@example.com'
      assert verify(database).select(
          'select * from users where email = :email',
          email='andrew@example.com')


And a unit test to check the sad path for this method could look like this:

.. code-block:: python

  def test_get_user_from_email_should_return_user_not_found_error():
      database = mock()
      when(database).select(any_values).then_return([])
      user_service = UserService(database=database)

      with pytest.raises(UserNotFound):
          user_service.get_user_from_email('andrew@example.com')
      verify(database).select(any_values)


Concepts
--------

Two main concepts exist in Pock, expectations and verifications. Expectations allow the behaviour of a mock to be defined and verification allows a mock to be inspected post test to see what interactions occurred on it.

Expectations can be created for methods, functions, properties and items. Expectations can return constant values, computed values and raise exceptions. See building expectations for more.

When creating expectations on methods, functions or items the arguments can be specified to match exactly or according to some criteria. See argument matching for more.

Verification can be performed on methods, functions, properties and items just the same as expectations and argument matching also works in a similar manner. See verifying interactions for more.
