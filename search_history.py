import sqlite3
from datetime import datetime


class SearchHistory:

    def __init__(self, database="search_history.db"):

        self.database = database

        self.create_table()


    # --------------------------------
    # Create database table
    # --------------------------------

    def create_table(self):

        connection = sqlite3.connect(
            self.database
        )

        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS search_history (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                query TEXT NOT NULL,

                corrected_query TEXT,

                search_type TEXT,

                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

            )
        """)

        connection.commit()
        connection.close()


    # --------------------------------
    # Save search
    # --------------------------------

    def save_search(
        self,
        query,
        corrected_query=None,
        search_type=None
    ):

        connection = sqlite3.connect(
            self.database
        )

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO search_history
            (query, corrected_query, search_type)

            VALUES (?, ?, ?)
        """, (
            query,
            corrected_query,
            search_type
        ))

        connection.commit()
        connection.close()


    # --------------------------------
    # Get search history
    # --------------------------------

    def get_history(self, limit=10):

        connection = sqlite3.connect(
            self.database
        )

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                query,
                corrected_query,
                search_type,
                timestamp

            FROM search_history

            ORDER BY id DESC

            LIMIT ?
        """, (limit,))

        history = cursor.fetchall()

        connection.close()

        return history


    # --------------------------------
    # Clear history
    # --------------------------------

    def clear_history(self):

        connection = sqlite3.connect(
            self.database
        )

        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM search_history"
        )

        connection.commit()
        connection.close()