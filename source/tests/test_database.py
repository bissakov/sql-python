from source.database import Database
from source.structs import Config
from source.errors import ConnectionNotEstablishedError, NoSuchTableError, SQLSyntaxError
from sqlalchemy.engine.base import Engine


def test_sqlite_connectivity() -> None:
    """
    Test function for checking the connectivity to an SQLite database.

    This function establishes a connection to an SQLite database using the
    chinook.db file. It verifies the connectivity by asserting that
    the engine object created from the connection is an instance of the
    Engine class.

    Raises:
        AssertionError: If the engine object is not an instance of Engine.

    """
    config = Config(
        dbtype='sqlite',
        dbname='chinook.db'
    )

    db = Database(config=config)
    db.connect()

    assert isinstance(db.engine, Engine)


def test_sqlite_action_without_connection() -> None:
    """
    Test function to verify the behavior of executing a SQLite database action without establishing a connection.

    Raises:
        AssertionError: If the error generated is not an instance of ConnectionNotEstablishedError.
    """
    error = None

    config = Config(
        dbtype='sqlite',
        dbname='chinook.db'
    )
    
    db = Database(config=config)
    try:
        db.execute('SELECT * FROM customer;')
    except ConnectionNotEstablishedError as e:
        error = e

    assert isinstance(error, ConnectionNotEstablishedError)


def test_sqlite_query_execution_unknown_table() -> None:
    """
    Test the execution of an SQLite query on an unknown table.

    This function tests the execution of an SQLite query on a table that does not exist in the database.
    It verifies that a `NoSuchTableError` is raised and captured correctly.

    Raises:
        NoSuchTableError: If the specified table does not exist in the database.
    """    
    error = None

    config = Config(
        dbtype='sqlite',
        dbname='chinook.db'
    )
    
    db = Database(config=config)
    db.connect()
    try:
        db.execute('SELECT * FROM unknown_table;')
    except NoSuchTableError as e:
        error = e

    assert isinstance(error, NoSuchTableError)


def test_sqlite_wrong_syntax_query() -> None:
    """
    Tests the execution of a SQLite query with incorrect syntax.

    This function connects to a SQLite database using the provided configuration, attempts to execute a query with
    incorrect syntax, and verifies that the correct exception is raised.

    Raises:
        SQLSyntaxError: If the specified query contains incorrect SQL syntax.
    """
    error = None

    config = Config(
        dbtype='sqlite',
        dbname='chinook.db'
    )
    
    db = Database(config=config)
    db.connect()
    try:
        db.execute('FLKJASLKFASj * FROM customer;')
    except SQLSyntaxError as e:
        error = e

    assert isinstance(error, SQLSyntaxError)


