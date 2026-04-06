from database.db_connection import DBConnection
from utils.hash_utils import hash_password

class UserRequests:
    def __init__(self):
        self.db = DBConnection()

    def unblock_user(self, login:str):
        """
        Разблокировка пользователя
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE public.user
                SET is_blocked = false
                WHERE login = %s
            """, (login,))
        self.db.commit()

    def edit_user_without_password(self, old_login: str, new_login: str, role: int, is_blocked: bool):
        """
        Изменение данных пользователя без изменения пароля
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                  UPDATE public.user
                  SET login = %s, role = %s, is_blocked = %s
                  WHERE login = %s
              """, (new_login, role, is_blocked, old_login))
        self.db.commit()

    def edit_user(self, old_login: str, new_login: str, password: str, role: int, is_blocked: bool):
        """
        Изменение данных пользователя
        """
        hashed_password = hash_password(password)

        with self.db.get_cursor() as cursor:
            cursor.execute("""
                  UPDATE public.user
                  SET login = %s, password = %s, role = %s, is_blocked = %s
                  WHERE login = %s
              """, (new_login, hashed_password, role, is_blocked, old_login))
        self.db.commit()

    def add_user(self, login: str, password: str, role: int):
        """
        Добавление нового пользователя
        """
        hashed_password = hash_password(password)

        with self.db.get_cursor() as cursor:
            cursor.execute("""
                  INSERT INTO public.user
                  (login, password, role) 
                  VALUES (%s, %s, %s)
              """, (login, hashed_password, role))
        self.db.commit()

    def get_all_users(self):
        """
        Получение всех пользователей
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("""
              SELECT 
              u.login, 
              ur.name, 
              u.is_blocked 
              FROM public.user u
              JOIN public.userrole ur ON u.role = ur.id
              """)
            return cursor.fetchall()