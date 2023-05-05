from sqlalchemy import create_engine
from sqlalchemy.sql import text
from dataclasses import dataclass
from typing import Optional, List, Tuple


@dataclass
class Credentials:
    user: Optional[str] = None
    password: Optional[str] = None


@dataclass
class Config:
    dbtype: str
    dbname: str
    credentials: Credentials = Credentials()
    host: Optional[str] = None
    port: Optional[int] = None


@dataclass
class QueryResult:
    rows: List
    columns: Tuple


class ConnectionNotEstablishedError(Exception):
    def __init__(self) -> None:
        super().__init__('Connection not established. Call the connect method first.')


class Database:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.engine = None
    
    def connect(self):
        if self.config.dbtype == 'sqlite':
            self.engine = create_engine('sqlite:///' + self.config.dbname)
        elif self.config.dbtype == 'postgresql':
            self.engine = create_engine(f'postgresql://{self.config.credentials.user}:{self.config.credentials.password}@' \
                                        f'{self.config.host}:{self.config.port}/{self.config.dbname}')
        elif self.config.dbtype == 'mysql':
            self.engine = create_engine(f'mysql+pymysql://{self.config.credentials.user}:{self.config.credentials.password}@' \
                                        f'{self.config.host}:{self.config.port}/{self.config.dbname}')
    
    def execute(self, sql: str) -> QueryResult:
        if self.engine is None:
            raise ConnectionNotEstablishedError()
        with self.engine.connect() as conn:
            result = conn.execute(text(sql))
            columns = tuple(result.keys())
            rows = [tuple(row) for row in result.fetchall()]
        return QueryResult(rows, columns)
    
    def commit(self):
        if self.engine is None:
            raise ConnectionNotEstablishedError()
        with self.engine.connect() as conn:
            conn.commit()
    
    def rollback(self):
        if self.engine is None:
            raise ConnectionNotEstablishedError()
        with self.engine.connect() as conn:
            conn.rollback()


if __name__ == '__main__':
    config = Config(dbtype='sqlite', dbname='chinook.db')
    db = Database(config)
    db.connect()
    data = db.execute('SELECT * FROM customers;')
    import rich

    rich.print(data.columns)
    for row in data.rows:
        rich.print(row)
    rich.print(data)
