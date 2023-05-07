import unittest

try:
    from database import Database
    from errors import ConnectionNotEstablishedError, SQLSyntaxError
    from structs import Config, QueryResult
except ModuleNotFoundError:
    from .database import Database
    from .errors import ConnectionNotEstablishedError, SQLSyntaxError
    from .structs import Config, QueryResult


class DatabaseTestCase(unittest.TestCase):
    def test_execute_valid_query(self):
        config = Config(dbtype='sqlite', dbname='chinook.db')
        db = Database(config)
        db.connect()

        result = db.execute('SELECT * FROM customers')

        self.assertIsNotNone(result)
        self.assertIsInstance(result, QueryResult)
        self.assertIsInstance(result.rows, list)
        self.assertIsInstance(result.columns, tuple)

    def test_execute_invalid_query(self):
        config = Config(dbtype='sqlite', dbname='chinook.db')
        db = Database(config)
        db.connect()

        with self.assertRaises(SQLSyntaxError):
            db.execute('SELECT * FROM non_existent_table')

    def test_execute_without_connect(self):
        config = Config(dbtype='sqlite', dbname='chinook.db')
        db = Database(config)

        with self.assertRaises(ConnectionNotEstablishedError):
            db.execute('SELECT * FROM users')

    def test_commit(self):
        config = Config(dbtype='sqlite', dbname='chinook.db')
        db = Database(config)
        db.connect()

        with self.assertRaises(ConnectionNotEstablishedError):
            db.commit()

    def test_rollback(self):
        config = Config(dbtype='sqlite', dbname='chinook.db')
        db = Database(config)
        db.connect()

        with self.assertRaises(ConnectionNotEstablishedError):
            db.rollback()


if __name__ == '__main__':
    unittest.main()
