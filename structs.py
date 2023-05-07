from dataclasses import dataclass
from typing import List, Optional, Tuple


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


@dataclass
class Config:
    """
    Data class representing the database configuration.

    Args:
        dbtype (str): The type of the database (e.g., 'sqlite', 'postgresql', 'mysql').
        dbname (str): The name of the database.
        credentials (Credentials): The credentials for the database. Default is an instance of Credentials with default values.
        host (Optional[str]): The host address of the database. Default is None.
        port (Optional[int]): The port number of the database. Default is None.
    """
    dbtype: str
    dbname: str
    credentials: Credentials = Credentials()
    host: Optional[str] = None
    port: Optional[int] = None


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
