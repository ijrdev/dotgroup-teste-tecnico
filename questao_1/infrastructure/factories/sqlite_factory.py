import sqlite3

from pathlib import Path

from sqlite3 import Connection

class SqliteFactory():
    def create_connection(self) -> Connection:
        try:
            return sqlite3.connect(database = Path(__file__).resolve().parents[2] / "biblioteca_livros.db")
        except Exception as ex:
            raise
