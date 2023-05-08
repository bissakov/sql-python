from typing import Optional


class ConnectionNotEstablishedError(Exception):
    """Exception raised when a database connection has not been established."""
    def __init__(self) -> None:
        super().__init__('Connection not established. Call the connect method first.')


class WrongConfigError(Exception):
    """Exception raised when the database configuration is invalid or missing."""
    pass


class SQLSyntaxError(Exception):
    """Exception raised for SQL syntax errors.

    Attributes:
        error_msg -- explanation of the error
    """
    def __init__(self, error_msg: str) -> None:
        super().__init__(error_msg)


class NoSuchTableError(Exception):
    """Exception raised when trying to access non-existing SQL table."""
    def __init__(self, db_name: str, table_name: str) -> None:
        super().__init__(f'No such table "{table_name}" in database "{db_name}"')


class WrongPasswordError(Exception):
    """Exception raised when database password authentication fails.
    
    Attributes:
        username -- database username
    """

    def __init__(self, username: Optional[str]) -> None:
        super().__init__(f'Password authentication failed for user "{username}"')

