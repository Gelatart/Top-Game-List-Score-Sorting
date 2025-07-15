import pytest
import requests
from unittest.mock import Mock
from unittest.mock import patch

from src.generator.igdb_client import IGDB_Client

"""
my_mock = Mock()

my_mock.some_method.return_value = 42
my_mock.some_attribute = "Hello, world!"
my_mock.some_method.side_effect = ValueError("Something went wrong")

@patch("my_module.some_function")
def test_my_function(mock_some_function):
    #Mock the behavior of some_function
    mock_some_function.return_value = "Mocked value"

    #Test my_function
    assert my_function() == "Mocked value"
# Another best practice is to use the assert_called_with method to verify that a method was called with the
# expected arguments. This helps ensure that your code is being called correctly and with the right inputs.
# Here's an example:
my_mock.some_method.assert_called_with(42, "Hello")

class DatabaseConnection:
    def query(self, sql):
        #Perform the actual query
        return "Result of the query"

mock_connection = Mock(spec=DatabaseConnection)
mock_connection.query.return_value = "Mocked result"

result = my_function(mock_connection)
assert result == "Mocked result"

mock_connection.query.side_effect = [
    "Result 1",
    "Result 2",
    ValueError("Something went wrong"),
]
#Similarly, when mocking API calls, you can use the return_value attribute to specify the expected response from the
# API. You can also use the side_effect attribute to simulate different scenarios, such as network errors or timeouts.

@patch("requests.get")
def test_my_function(mock_get):
    #Mock the API response
    mock_get.return_value.json.return_value = {"message": "Hello, world!"}

    #Test my_function
    assert my_function() == "Hello, world!"


@patch("my_module.some_dependency")
def test_my_function(mock_dependency):
    #Mock the behavior of some_dependency
    mock_dependency.return_value = "Mocked value"

    #Test my_function
    assert my_function() == "Mocked value"
"""

