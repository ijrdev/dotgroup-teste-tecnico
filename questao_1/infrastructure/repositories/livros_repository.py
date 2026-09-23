from typing import List
from datetime import datetime

from sqlite3 import Connection, Cursor, Row

from application.utils.decorators.retry_decorator import sync_retry_decorator
from infrastructure.factories.sqlite_factory import SqliteFactory

class LivrosRepository():
    def __init__(self) -> None:
        self.sqlite_factory: SqliteFactory = SqliteFactory()

    def create_table(self) -> None:
        connection: Connection | None = None

        try:
            connection = self.sqlite_factory.create_connection()
            
            cursor: Cursor = connection.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS livros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data_cadastro TEXT NOT NULL,
                    data_publicacao TEXT NOT NULL,
                    titulo TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    resumo TEXT NOT NULL
                );
            """)

            connection.commit()
        except Exception:
            raise
        finally:
            if connection:
                connection.close()

    @sync_retry_decorator(attempts = 3, delay = 1, exceptions = (Exception))
    def create(self, data: dict) -> Row:
        connection: Connection | None = None
        
        try:
            connection = self.sqlite_factory.create_connection()
            
            connection.row_factory = Row

            cursor: Cursor = connection.cursor()

            cursor.execute(
                "INSERT INTO livros (data_cadastro, data_publicacao, titulo, autor, resumo) VALUES (?, ?, ?, ?, ?);",
                (datetime.now(), data["data_publicacao"], data["titulo"], data["autor"], data["resumo"])
            )
            
            connection.commit()

            cursor.execute("SELECT * FROM livros WHERE id = ?;", (cursor.lastrowid,))
            
            return cursor.fetchone()
        except Exception:
            raise
        finally:
            if connection:
                connection.close()

    @sync_retry_decorator(attempts = 3, delay = 1, exceptions = (Exception))
    def get_all(self, data: dict) -> List[Row]:
        connection: Connection | None = None
        
        try:
            connection = self.sqlite_factory.create_connection()
            
            connection.row_factory = Row

            cursor: Cursor = connection.cursor()
            
            where: list = []
            param: list = []

            for col, val in data.items():
                where.append(f"{col} LIKE ?")
                param.append(f"%{val}%")

            cursor.execute(f"SELECT * FROM livros WHERE {' AND '.join(where)}", param)
                           
            return cursor.fetchall()
        except Exception:
            raise
        finally:
            if connection:
                connection.close()
    
