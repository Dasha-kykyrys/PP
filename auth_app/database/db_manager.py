import psycopg2
from config import DB_CONFIG


class DatabaseManager:
    """Управление подключением и запросами к PostgreSQL"""

    def __init__(self):
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

    def user_serch(self, login: str) -> bool:
        """
        Проверка логина существования логина
        """
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM public.user
                WHERE login = %s
            """, (login,))
            return cursor.fetchone() is not None

    def authenticate(self, login: str, password: str) -> bool:
        """
        Проверка пароля
        """
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM public.user
                WHERE login = %s and password = %s
            """, (login, password))
            return cursor.fetchone() is not None

    def block_user(self, login:str):
        """
        Блокировка пользователя
        """
        with self.connection.cursor() as cursor:
            cursor.execute("""
                UPDATE public.user
                SET isblocked = true
                WHERE login = %s
            """, (login,))
        self.connection.commit()

    def get_user_status (self, login:str) -> bool:
        """
        Получение статуса пользователя
        """
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT isblocked FROM public.user
                WHERE login = %s
            """, (login,))
            status = cursor.fetchone()
            return status[0]

    def get_user_role(self, login:str) -> bool:
        """
        Получение роли пользователя
        """
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT role FROM public.user
                WHERE login = %s
            """, (login,))
            status = cursor.fetchone()
            return status[0] == 2

    def edit_user(self, login:str, password:str, role:int, is_blocked:bool):
        """
        Изменение данных пользователя
        """
        with self.connection.cursor() as cursor:
            cursor.execute("""
                UPDATE public.user
                SET password = %s, role = %s, isblocked = %s
                WHERE login = %s
            """, (password, role, is_blocked, login))
        self.connection.commit()


    def add_user(self, login:str, password:str, role:int):
        """
        Добавление нового пользователя
        """
        with self.connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO public.user
                (login, password, role) 
                VALUES (%s, %s, %s)
            """, (login,password,role))
        self.connection.commit()

    def delete_user(self, login:str):
        """
        Удаление пользователя
        """
        with self.connection.cursor() as cursor:
            cursor.execute("""
            DELETE FROM public.user
            WHERE login = %s
            """, (login,))
        self.connection.commit()

    def get_all_users(self):
        """
        Получение всех пользователей
        """
        with self.connection.cursor() as cursor:
            cursor.execute("""
            SELECT 
            u.login, 
            u.password, 
            ur.name, 
            u.isblocked 
            FROM public.user u
            JOIN public.userrole ur ON u.role = ur.id
            """)
            return cursor.fetchall()


