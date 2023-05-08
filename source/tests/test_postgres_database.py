import os

from sqlalchemy.engine.base import Connection, Engine

from source.database import Database
from source.errors import (ConnectionNotEstablishedError, NoSuchTableError,
                           SQLSyntaxError, WrongPasswordError)
from source.structs import Config, Credentials


def test_postgres_valid_connectivity() -> None:
    config = Config(
        dbtype='postgresql',
        dbname='dvdrental',
        credentials=Credentials(user='postgres', password='pass'),
        host=os.environ['WSL_HOST_IP'],
        port=5432
    )

    db = Database(config=config)
    db.connect()

    assert isinstance(db.engine, Engine)


def test_postgres_invalid_connectivity() -> None:
    error = None

    config = Config(
        dbtype='postgresql',
        dbname='dvdrental',
        credentials=Credentials(user='postgres', password='pass'),
        host=os.environ['WSL_HOST_IP'],
        port=5432
    )

    db = Database(config=config)

    try:
        db.execute('SELECT * FROM customer;')
    except ConnectionNotEstablishedError as e:
        error = e

    assert isinstance(error, ConnectionNotEstablishedError)


def test_postgres_wrong_credentials() -> None:
    error = None

    config = Config(
        dbtype='postgresql',
        dbname='dvdrental',
        credentials=Credentials(user='postgres', password='wrong_pass'),
        host=os.environ['WSL_HOST_IP'],
        port=5432
    )

    db = Database(config=config)

    try:
        db.connect()
    except WrongPasswordError as e:
        error = e

    assert isinstance(error, WrongPasswordError)
