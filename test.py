import unittest
from unittest.mock import patch

from sqlalchemy.exc import SQLAlchemyError

from database import *


class DatabaseTestCase(unittest.TestCase):
    def test_execute_valid_query(self):
        # Arrange
        config = Config(dbtype='sqlite', dbname='chinook.db')
        db = Database(config)
        db.connect()

        # Act
        result = db.execute('SELECT * FROM customers')

        # Assert
        self.assertIsNotNone(result)
        self.assertIsInstance(result, QueryResult)
        self.assertIsInstance(result.rows, list)
        self.assertIsInstance(result.columns, tuple)

    def test_execute_invalid_query(self):
        # Arrange
        config = Config(dbtype='sqlite', dbname='chinook.db')
        db = Database(config)
        db.connect()

        # Act and Assert
        with self.assertRaises(SQLSyntaxError):
            db.execute('SELECT * FROM non_existent_table')

    def test_execute_without_connect(self):
        # Arrange
        config = Config(dbtype='sqlite', dbname='chinook.db')
        db = Database(config)

        # Act and Assert
        with self.assertRaises(ConnectionNotEstablishedError):
            db.execute('SELECT * FROM users')

    def test_commit(self):
        # Arrange
        config = Config(dbtype='sqlite', dbname='chinook.db')
        db = Database(config)
        db.connect()

        # Act and Assert
        with self.assertRaises(ConnectionNotEstablishedError):
            db.commit()

    def test_rollback(self):
        # Arrange
        config = Config(dbtype='sqlite', dbname='chinook.db')
        db = Database(config)
        db.connect()

        # Act and Assert
        with self.assertRaises(ConnectionNotEstablishedError):
            db.rollback()


if __name__ == '__main__':
    unittest.main()
