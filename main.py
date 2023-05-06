from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.engine.base import Engine
from dataclasses import dataclass, fields
from typing import Optional, List, Tuple
import rich


@dataclass
class Credentials:
    user: Optional[str] = None
    password: Optional[str] = None


@dataclass
class Config:
    dbtype: str
    dbname: str
    credentials: Optional[Credentials] = None 
    host: Optional[str] = None
    port: Optional[int] = None


@dataclass
class QueryResult:
    rows: List[Tuple]
    columns: Tuple


class ConnectionNotEstablishedError(Exception):
    def __init__(self) -> None:
        super().__init__('Connection not established. Call the connect method first.')


class WrongConfigError(Exception):
    pass


class Database:
    def __init__(self, config: Config) -> None:
        self.config: Config = config
        self.engine: Optional[Engine] = None

    def connect(self) -> None:
        if self.config.dbtype == 'sqlite':
            self.engine = create_engine(f'sqlite:///{self.config.dbname}')
        elif self.config.credentials is None or None in (self.config.host, self.config.port):
            error_msg = ', '.join(field.name for field in fields(self.config) if not getattr(self.config, field.name))
            raise WrongConfigError(f'Config.{error_msg} not provided.')
        else:
            connection_string = f'{self.config.dbtype}+pymysql' if self.config.dbtype == 'mysql' else self.config.dbtype
            user, password = self.config.credentials.user, self.config.credentials.password
            host, port, dbname = self.config.host, self.config.port, self.config.dbname
            self.engine = create_engine(f'{connection_string}://{user}:{password}@{host}:{port}/{dbname}')
        rich.print(self.engine, type(self.engine))

    def execute(self, sql: str) -> QueryResult:
        if self.engine is None:
            raise ConnectionNotEstablishedError() 

        with self.engine.connect() as conn:
            result = conn.execute(text(sql))
            columns = tuple(result.keys())
            rows = [tuple(row) for row in result.fetchall()]
        return QueryResult(rows, columns)
    
    def commit(self) -> None:
        if self.engine is None:
            raise ConnectionNotEstablishedError() 

        with self.engine.connect() as conn:
            conn.commit()
    
    def rollback(self) -> None:
        if self.engine is None:
            raise ConnectionNotEstablishedError() 

        with self.engine.connect() as conn:
            conn.rollback()


if __name__ == '__main__':
    # config = Config(dbtype='sqlite', dbname='chinook.db')
    # db = Database(config)
    # db.connect()
    # data = db.execute('SELECT * FROM customers;')
    # import rich
    #
    # rich.print(data.columns)
    # for row in data.rows:
    #     rich.print(row)
    # rich.print(data)

    config = Config(dbtype='sqlite', dbname='chinook.db')
    db = Database(config)
    db.connect()
    # db.execute('')
