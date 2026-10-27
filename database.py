import sqlite3
import numpy as np


class SearchDatabase:

    def __init__(self, db_name="search_engine.db"):

        self.db_name = db_name

        self.connection = sqlite3.connect(
            self.db_name
        )

        self.create_tables()


    # =================================
    # CREATE TABLES
    # =================================

    def create_tables(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (

                filename TEXT PRIMARY KEY,

                content TEXT NOT NULL,

                modified_time REAL NOT NULL
            )
        """)
        # =================================
        # DOCUMENT EMBEDDINGS
        # =================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS embeddings (

                filename TEXT PRIMARY KEY,

                embedding BLOB NOT NULL,

                modified_time REAL NOT NULL
            )
        """)

        self.connection.commit()


    # =================================
    # SAVE / UPDATE DOCUMENT
    # =================================

    def save_document(
        self,
        filename,
        content,
        modified_time
    ):

        cursor = self.connection.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO documents
            (
                filename,
                content,
                modified_time
            )

            VALUES (?, ?, ?)
        """, (
            filename,
            content,
            modified_time
        ))

        self.connection.commit()


    # =================================
    # LOAD ALL DOCUMENTS
    # =================================

    def load_documents(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT filename, content
            FROM documents
        """)

        rows = cursor.fetchall()

        documents = {}

        for filename, content in rows:

            documents[filename] = content

        return documents


    # =================================
    # GET DOCUMENT INFORMATION
    # =================================

    def get_documents_info(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT
                filename,
                content,
                modified_time
            FROM documents
        """)

        rows = cursor.fetchall()

        documents = {}

        for filename, content, modified_time in rows:

            documents[filename] = {
                "content": content,
                "modified_time": modified_time
            }

        return documents


    # =================================
    # DELETE DOCUMENT
    # =================================

    def delete_document(
        self,
        filename
    ):

        cursor = self.connection.cursor()

        cursor.execute("""
            DELETE FROM documents
            WHERE filename = ?
        """, (
            filename,
        ))

        self.connection.commit()

    # =================================
    # SAVE EMBEDDING
    # =================================

    def save_embedding(
        self,
        filename,
        embedding,
        modified_time
    ):

        cursor = self.connection.cursor()

        embedding_bytes = np.array(
            embedding,
            dtype=np.float32
        ).tobytes()

        cursor.execute("""
            INSERT OR REPLACE INTO embeddings
            (
                filename,
                embedding,
                modified_time
            )
            VALUES (?, ?, ?)
        """, (
            filename,
            embedding_bytes,
            modified_time
        ))

        self.connection.commit()


    # =================================
    # LOAD EMBEDDING
    # =================================

    def load_embedding(
        self,
        filename
    ):

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT embedding
            FROM embeddings
            WHERE filename = ?
        """, (
            filename,
        ))

        row = cursor.fetchone()

        if row is None:
            return None

        return np.frombuffer(
            row[0],
            dtype=np.float32
        )


    # =================================
    # GET EMBEDDING INFO
    # =================================

    def get_embedding_info(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT
                filename,
                modified_time
            FROM embeddings
        """)

        rows = cursor.fetchall()

        embeddings = {}

        for filename, modified_time in rows:

            embeddings[filename] = modified_time

        return embeddings


    # =================================
    # DELETE EMBEDDING
    # =================================

    def delete_embedding(
        self,
        filename
    ):

        cursor = self.connection.cursor()

        cursor.execute("""
            DELETE FROM embeddings
            WHERE filename = ?
        """, (
            filename,
        ))

        self.connection.commit()


    # =================================
    # CLOSE
    # =================================

    def close(self):

        self.connection.close()