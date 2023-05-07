from dataclasses import dataclass, fields
from typing import Dict, List, Optional, Tuple

import rich
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError


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


class ConnectionNotEstablishedError(Exception):
    """
    Exception raised when a database connection has not been established.

    Inherits:
        Exception
    """
    def __init__(self) -> None:
        super().__init__("Connection not established. Call the connect method first.")


class WrongConfigError(Exception):
    """
    Exception raised when the database configuration is invalid or missing.

    Inherits:
        Exception
    """
    pass


class SQLSyntaxError(Exception):
    """Exception raised for SQL syntax errors.

    Attributes:
        error_msg -- explanation of the error
    """
    def __init__(self, error_msg: str) -> None:
        super().__init__(error_msg)


class Database:
    """
    Class representing a database connection and operations.

    Args:
        config (Config): The database configuration.

    Attributes:
        config (Config): The database configuration.
        engine (Optional[Engine]): The SQLAlchemy engine object representing the database connection.
        DATABASE_ENGINES (Dict[str, str]): A dictionary mapping database types to SQLAlchemy connection strings.
    """

    def __init__(self, config: Config) -> None:
        """
        Initialize a Database instance.

        Args:
            config (Config): The database configuration.
        """
        self.config: Config = config
        self.engine: Optional[Engine] = None
        self.DATABASE_ENGINES: Dict[str, str] = {
            "sqlite": "sqlite:///{dbname}",
            "postgresql": "postgresql://{user}:{password}@{host}:{port}/{dbname}",
            "mysql": "mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}",
            "mssql": "mssql+pymssql://{user}:{password}@{host}:{port}/{dbname}",
        }

    def connect(self) -> None:
        """
        Establish a connection to the database.

        Raises:
            WrongConfigError: If the database type in the configuration is not supported.
        """
        if self.config.dbtype not in self.DATABASE_ENGINES:
            raise WrongConfigError(f"Unsupported dbtype: {self.config.dbtype}")
        engine_template = self.DATABASE_ENGINES[self.config.dbtype]
        connection_string = engine_template.format(
            user=self.config.credentials.user,
            password=self.config.credentials.password,
            host=self.config.host,
            port=self.config.port,
            dbname=self.config.dbname,
        )
        self.engine = create_engine(connection_string)

    def execute(self, sql: str) -> QueryResult:
        """Executes the provided SQL query and returns the result.

        Args:
            sql: The SQL query to execute.

        Returns:
            QueryResult: The result of the query execution.

        Raises:
            ConnectionNotEstablishedError: If the database connection is not established.
            SQLSyntaxError: If there is a syntax error in the SQL query.
            SQLAlchemyError: If any other error occurs during query execution.
        """
        if self.engine is None:
            raise ConnectionNotEstablishedError()

        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(sql))
                columns = tuple(result.keys())
                rows = [tuple(row) for row in result.fetchall()]
            return QueryResult(rows, columns)
        except SQLAlchemyError as e:
            if 'syntax error' in str(e).lower():
                raise SQLSyntaxError(str(e))
            else:
                raise e

    def commit(self) -> None:
        """
        Commit the current transaction.

        Raises:
            ConnectionNotEstablishedError: If the database connection has not been established.
        """
        if self.engine is None:
            raise ConnectionNotEstablishedError()

        with self.engine.connect() as conn:
            conn.commit()

    def rollback(self) -> None:
        """
        Rollback the current transaction.

        Raises:
            ConnectionNotEstablishedError: If the database connection has not been established.
        """
        if self.engine is None:
            raise ConnectionNotEstablishedError()

        with self.engine.connect() as conn:
            conn.rollback()


if __name__ == "__main__":
    config = Config(dbtype='sqlite', dbname='chinook.db')
    db = Database(config)
    db.connect()
    # data = db.execute('SELECT * FROM customers;')
    data = db.execute('salkdasjlkda')
    import rich

    rich.print(data.columns)
    for row in data.rows:
        print(row)
    # rich.print(data)

    # config = Config(dbtype="sqlite", dbname="chinook.db")
    # db = Database(config)
    # db.connect()
    # db.execute('')
