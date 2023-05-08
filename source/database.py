import re
import sqlite3
from typing import Dict, Optional

import rich
from sqlalchemy import create_engine
from sqlalchemy import exc as sqlalchemy_exc
from sqlalchemy.engine.base import Engine
from sqlalchemy.sql import text

try:
    from errors import (ConnectionNotEstablishedError, NoSuchTableError,
                        SQLSyntaxError)
    from structs import Config, Credentials, QueryResult
except ModuleNotFoundError:
    from .errors import (ConnectionNotEstablishedError, NoSuchTableError,
                         SQLSyntaxError)
    from .structs import Config, Credentials, QueryResult


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
        Raises:
            WrongConfigError: If the database type in the configuration is not supported.
        """
        self.config: Config = config
        self.engine: Optional[Engine] = None
        self.DATABASE_ENGINES: Dict[str, str] = {
            'sqlite': 'sqlite:///{dbname}',
            'postgresql': 'postgresql://{user}:{password}@{host}:{port}/{dbname}',
            'mysql': 'mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}',
            'mssql': 'mssql+pymssql://{user}:{password}@{host}:{port}/{dbname}',
        }

    def connect(self) -> None:
        """
        Establish a connection to the database.
        """
        engine_template = self.DATABASE_ENGINES[self.config.dbtype]
        connection_string = engine_template.format(
            user=self.config.credentials.user,
            password=self.config.credentials.password,
            host=self.config.host,
            port=self.config.port,
            dbname=self.config.dbname,
        )
        self.engine = create_engine(connection_string)

    def execute(self, sql: str) -> Optional[QueryResult]:
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
            raise ConnectionNotEstablishedError() from None

        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(sql))
                columns = tuple(result.keys())
                rows = [tuple(row) for row in result.fetchall()]
            return QueryResult(rows, columns)
        except (sqlite3.OperationalError, sqlalchemy_exc.OperationalError) as e:
            error_msg = str(e).lower().strip()
            if 'syntax error' in error_msg:
                raise SQLSyntaxError(str(e)) from None
            elif 'no such table' in error_msg:
                table_name = match.group(1) if (match := re.search(r'no such table: (.+)', error_msg)) else ''
                raise NoSuchTableError(db_name=self.config.dbname, table_name=table_name) from None
            else:
                raise e

    def commit(self) -> None:
        """
        Commit the current transaction.

        Raises:
            ConnectionNotEstablishedError: If the database connection has not been established.
        """
        if self.engine is None:
            raise ConnectionNotEstablishedError() from None

        with self.engine.connect() as conn:
            conn.commit()

    def rollback(self) -> None:
        """
        Rollback the current transaction.

        Raises:
            ConnectionNotEstablishedError: If the database connection has not been established.
        """
        if self.engine is None:
            raise ConnectionNotEstablishedError() from None

        with self.engine.connect() as conn:
            conn.rollback()


if __name__ == "__main__":
    config = Config(dbtype='sqlite', dbname='chinook.db')
    db = Database(config)
    db.connect()
    # data = db.execute('SELECT * FROM customers;')
    try:
        data = db.execute('select * from sadasda;')
    except NoSuchTableError as e:
        raise e
    # import rich
    #
    # rich.print(data.columns)
    # for row in data.rows:
    #     print(row)
    # rich.print(data)

    # config = Config(dbtype="sqlite", dbname="chinook.db")
    # db = Database(config)
    # db.connect()
    # db.execute('')
