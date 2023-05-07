# Database Class

[Detailed documentation](https://bissakov.github.io/sql-python/docs)

The `Database` class represents a database connection and provides operations based on the database type (sqlite3, postgresql, mysql, or mssql).

## Installation

Dependencies: python3.10
```
python -m venv venv
pip install -r requirements.txt
python source/database.py
```

## Usage

```python
from database import Database

# Create a database configuration object
config = Config(
  dbtype='', # Database type (sqlite, postgresql, mysql or mssql) - Mandatory
  dbname='', # Database name - Mandatory
  credentials=Credentials(user='', password=''), # Optional for sqlite
  host='', # Optional for sqlite
  port=5432 # Optional for sqlite
)

# Create a database instance
db = Database(config)

# Establish a connection to the database
db.connect()

# Execute SQL queries
result = db.execute('SELECT * FROM table_name')

# Commit the current transaction
db.commit()

# Rollback the current transaction
db.rollback()```
