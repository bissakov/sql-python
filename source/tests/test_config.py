from source.structs import Config
from source.errors import WrongConfigError


def test_invalid_database_type() -> None:
    """
    Test function for checking the behavior when providing a wrong database type (not sqlite, postgresql, mysql or mssql).

    Raises:
        AssertionError: If the error raised is not an instance of WrongConfigError.
    """
    error = None
    try:
        _ = Config(dbtype='dsakjdkas', dbname='dsdksadas')
    except WrongConfigError as e:
        error = e
    assert isinstance(error, WrongConfigError)


def test_unknown_db() -> None:
    """
    Test function for checking the behavior when providing a non-existing SQLite database.

    Raises:
        AssertionError: If the error raised is not instance of WrongConfigError.
    """
    error = None
    try:
        _ = Config(dbtype='sqlite', dbname='dsdksadas')
    except WrongConfigError as e:
        error = e
    assert isinstance(error, WrongConfigError)

