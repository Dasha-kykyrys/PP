from database.db_connection import DBConnection
from utils.hash_utils import verify_password


class AuthRequests:
    def __init__(self):
        self.db = DBConnection()

    def user_search(self, login: str) -> bool:
        """
        Проверка существования логина
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                SELECT * FROM public.user
                WHERE login = %s
            """, (login,))
            return cursor.fetchone() is not None

    def get_user_status (self, login:str) -> bool:
        """
        Получение статуса пользователя
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                SELECT is_blocked FROM public.user
                WHERE login = %s
            """, (login,))
            status = cursor.fetchone()
            return status[0]

    def get_user_role(self, login:str) -> bool:
        """
        Получение роли пользователя
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                SELECT role FROM public.user
                WHERE login = %s
            """, (login,))
            status = cursor.fetchone()
            return status[0] == 2

    def get_failed_attempts(self, login: str):
        """
        Получение значения счётчика ошибок
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                 SELECT failed_attempts FROM public.user
                 WHERE login = %s
             """, (login,))
            failed_attempts = cursor.fetchone()
            if failed_attempts and failed_attempts[0]:
                return int(failed_attempts[0])
            return 0

    def edit_failed_attempts(self, login: str, failed_attempts: int):
        """
        Изменение счётчика ошибок
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                 UPDATE public.user
                 SET failed_attempts = %s
                 WHERE login = %s
             """, (failed_attempts, login))
        self.db.commit()

    def authenticate(self, login: str, password: str) -> bool:
        """
        Проверка пароля
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                SELECT password FROM public.user
                WHERE login = %s
            """, (login,))
            hashed_password = cursor.fetchone()
            return verify_password(password, hashed_password[0])

    def block_user(self, login:str):
        """
        Блокировка пользователя
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE public.user
                SET is_blocked = true
                WHERE login = %s
            """, (login,))
        self.db.commit()