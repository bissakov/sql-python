import os
from dataclasses import dataclass
from typing import List, Optional, Tuple
from typing_utils import issubtype

try:
    from errors import WrongConfigError
except ModuleNotFoundError:
    from .errors import WrongConfigError


@dataclass
class Credentials:
    """
    Data class representing database credentials.

    Args:
        user (Optional[str]): The username for the database. Default is None.
        password (Optional[str]): The password for the database. Default is None.
    """
    user: Optional[str] = None
    password: Optional[str] = None

    def __post_init__(self) -> None:
        """
        Validates the user and password attributes after initialization.

        Raises:
            WrongConfigError: If user or password is not of type Optional[str].
        """
        if not issubtype(type(self.user), Optional[str]) or not issubtype(type(self.password), Optional[str]):
            raise WrongConfigError(f'User and password should be strings.')


@dataclass
class Config:
    """
    Data class representing the database configuration.

    Args:
        dbtype (str): The type of the database (e.g., 'sqlite', 'postgresql', 'mysql', 'mssql').
        dbname (str): The name of the database.
        credentials (Credentials): The credentials for the database. Default is an instance of Credentials with default values.
        host (Optional[str]): The host address of the database. Default is None.
        port (Optional[int]): The port number of the database. Default is None.

    Raises:
        WrongConfigError: If an unsupported dbtype is provided or if the specified SQLite database does not exist.
    """
    dbtype: str
    dbname: str
    credentials: Credentials = Credentials()
    host: Optional[str] = None
    port: Optional[int] = None

    def __post_init__(self) -> None:
        """Initialize the Config instance after the dataclass has been instantiated.

        Raises:
            WrongConfigError: If an unsupported dbtype is provided or if the specified SQLite database does not exist.
        """
        if self.dbtype not in ['sqlite', 'postgresql', 'mysql', 'mssql']:
            raise WrongConfigError(f'Unsupported dbtype: {self.dbtype}') from None
        if self.dbtype == 'sqlite' and not os.path.exists(self.dbname):
            raise WrongConfigError(f'SQLite database {self.dbname} does not exist.') from None


@dataclass
class QueryResult:
    """
    Data class representing the result of a database query.

    Args:
        rows (List[Tuple]): The rows returned by the query.
        columns (Tuple): The column names of the result set.
    """
    rows: List[Tuple]
    columns: Tuple
