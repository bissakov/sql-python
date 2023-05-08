from source.database import Database
from source.structs import Config
from sqlalchemy.engine.base import Engine


def test_sqlite_database_connectivity() -> None:
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


