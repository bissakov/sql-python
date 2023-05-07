import re
from typing import Dict, Optional

import rich
from sqlalchemy import exc as sqlalchemy_exc
from sqlalchemy import create_engine, table
from sqlalchemy.engine.base import Engine
import sqlite3
from sqlalchemy.sql import text

from errors import *
from structs import *


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
            raise ConnectionNotEstablishedError()

        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(sql))
                columns = tuple(result.keys())
                rows = [tuple(row) for row in result.fetchall()]
            return QueryResult(rows, columns)
        except (sqlite3.OperationalError, sqlalchemy_exc.OperationalError) as e:
            error_msg = str(e).lower().strip()
            if 'syntax error' in error_msg:
                raise SQLSyntaxError(str(e))
            elif 'no such table' in error_msg:
                table_name = match.group(1) if (match := re.search(r'no such table: (.+)', error_msg)) else ''
                raise NoSuchTableError(db_name=self.config.dbname, table_name=table_name)
            # else:
            #     raise e

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
