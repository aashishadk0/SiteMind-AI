"""
SQLite database connection.
"""

import sqlite3

from backend.app.config import DATABASE_PATH


class Database:

    _connection = None

    @classmethod
    def connect(cls):

        if cls._connection is None:

            cls._connection = sqlite3.connect(
                DATABASE_PATH,
                check_same_thread=False
            )

            cls._connection.row_factory = sqlite3.Row

        return cls._connection