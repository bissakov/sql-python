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
    credentials: Optional[Credentials] = None 
    host: Optional[str] = None
    port: Optional[int] = None


@dataclass
class QueryResult:
    rows: List
    columns: Tuple


class ConnectionNotEstablishedError(Exception):
    def __init__(self) -> None:
        super().__init__('Connection not established. Call the connect method first.')


class WrongConfigError(Exception):
    def __init__(self, error_msg: str) -> None:
        super().__init__(error_msg)


class Database:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.engine = None

    def _check_config(self):
        errored_items = []
        if self.config.credentials is None:
            errored_items.append('credentials')
        if self.config.host is None:
            errored_items.append('host')
        if self.config.port is None:
            errored_items.append('port')
        if errored_items:
            error_msg = ', '.join(errored_items)
            print(error_msg, errored_items)
            raise WrongConfigError(error_msg=f'{error_msg.capitalize()} not provided.')


    def connect(self):
        if self.config.dbtype == 'sqlite':
            self.engine = create_engine('sqlite:///' + self.config.dbname)
        else:
            try:
                self._check_config()
            except WrongConfigError as e:
                raise e
            if self.config.dbtype == 'postgresql':
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

    config = Config(dbtype='postgresql', dbname='test', host='test', port=5000)
    db = Database(config)
    db.connect()
