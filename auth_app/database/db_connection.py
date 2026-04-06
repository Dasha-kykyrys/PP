import psycopg2
from config import DB_CONFIG

class DBConnection:
    """Управление подключением к PostgreSQL"""

    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        """Установка соединения с PostgreSQL"""
        self.connection = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            database=DB_CONFIG['database'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )

    def get_cursor(self):
        return self.connection.cursor()

    def commit(self):
            self.connection.commit()

    def close(self):
        if self.connection:
            self.connection.close()