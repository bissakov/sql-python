from source.errors import WrongConfigError
from source.structs import Credentials


def test_valid_credentials() -> None:
    """
    Test function for checking the behavior of valid credentials creation.

    Raises:
        AssertionError: If the credentials are not created correctly.
    """
    credentials = Credentials(user='user', password='password')
    assert credentials.user == 'user' and credentials.password == 'password'


def test_invalid_credentials() -> None:
    """
    Test function for checking the behavior when providing credentials of invalid type.

    Raises:
        AssertionError: If the error raised is not an instance of WrongConfigError.
    """
    error = None
    try:
        _ = Credentials(user=213, password=421)
    except WrongConfigError as e:
        error = e
    assert isinstance(error, WrongConfigError)

