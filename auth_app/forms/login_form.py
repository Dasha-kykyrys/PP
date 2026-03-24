import tkinter as tk
from tkinter import ttk, messagebox
from database.db_manager import DatabaseManager
from forms.admin_form import AdminForm
from forms.captcha_form import CaptchaPuzzle

class LoginForm:
    """Форма авторизации пользователей с капчей"""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.root = tk.Tk()
        self.root.title("Авторизация")
        width = 400
        height = 500
        self.root.minsize(width, height)

        self.max_attempts = 3
        self.failed_attempts_password = 0
        self.failed_attempts_captcha = 0

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.create_widgets()
        self.set_tab()
        self.center_window(self.root, width, height)

    def create_widgets(self):
        """Создание виджетов формы"""
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(column=0, row=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)

        # Заголовок
        title_label = ttk.Label(
            main_frame,
            text="Авторизация",
            font=("Arial", 18, "bold")
        )
        title_label.grid(column=0, row=0, pady=(0, 20))

        # Кнопка входа
        self.enter_button = ttk.Button(
            main_frame,
            text="Войти",
            width=20,
            command=self.handle_login
        )
        self.enter_button.grid(column=0, row=2, pady=(0, 15))

        login_frame = ttk.Frame(main_frame, padding="20")
        login_frame.grid(column=0, row=1, sticky="nsew", padx=(0, 10))
        login_frame.grid_columnconfigure(0, weight=1)

        # Логин
        login_label = ttk.Label(login_frame, text="Логин:")
        login_label.grid(column=0, row=1, sticky="w")
        self.login_entry = ttk.Entry(login_frame, width=30)
        self.login_entry.grid(column=0, row=2, sticky="ew", pady=(0, 15))

        # Пароль
        password_label = ttk.Label(login_frame, text="Пароль:")
        password_label.grid(column=0, row=3, sticky="w")
        self.password_entry = ttk.Entry(login_frame, show="*", width=30)
        self.password_entry.grid(column=0, row=4, sticky="ew")

        # Капча
        self.captcha = CaptchaPuzzle(main_frame)
        self.captcha.grid(column=0, row=3, pady=(5, 0))

    def set_tab(self):
        """Настройка последовательного перехода фокуса по Tab"""
        self.login_entry.focus_set()
        self.password_entry.bind("<Tab>", lambda e: self.enter_button.focus_set())
        self.enter_button.bind("<Tab>", lambda e: self.login_entry.focus_set())

    def handle_login(self):
        """Обработка попытки входа"""
        login = self.login_entry.get()
        password = self.password_entry.get()

        if login == "" or password == "":
            messagebox.showinfo(
                "Ошибка ввода",
                "Все поля должны быть заполнены!!!"
            )
            return

        # Поиск наличия пользователя
        if self.db.user_serch(login):
            # Проверка статуса пользователя
            if self.db.get_user_status(login):
                self.block_user_message(login)
                return
            # Проверка связки пароль и логин
            if self.db.authenticate(login, password):
                # Проверка капчи
                if self.captcha.check_captcha():
                    messagebox.showinfo(
                        "Авторизация",
                        "Вы успешно авторизовались"
                    )
                    # Проверка роли пользователя
                    if self.db.get_user_role(login):
                        self.root.destroy()
                        admin_form = AdminForm(self.db)
                        admin_form.run()
                    else:
                        self.root.destroy()
                else:
                    self.failed_attempts_captcha += 1
                    # Проверка кол-во ошибок в капче
                    if self.failed_attempts_captcha > 2:
                        self.block_user_message(login)
                        self.db.block_user(login)
                        return
                    messagebox.showinfo(
                        "Ошибка проверки",
                        "Картинка собрана неверно."
                    )
            else:
                self.failed_attempts_password += 1
                # Проверка кол-во ошибок в пароле
                if self.failed_attempts_password > 2:
                     self.block_user_message(login)
                     self.db.block_user(login)
                     return
                self.error_authorization_message()
        else:
            self.error_authorization_message()
            return

    def error_authorization_message(self):
        """
        Сообщение о неверных данных
        """
        messagebox.showinfo(
            "Ошибка авторизации",
            "Вы ввели неверный логин или пароль. Пожалуйста проверьте ещё раз введенные данные."
        )

    def block_user_message(self, login:str):
        """
        Сообщение о блокировке
        """
        messagebox.showinfo(
            "Блокировка",
            "Вы заблокированы. Обратитесь к администратору"
        )


    def center_window(self, window, width, height):
        """
        Центрирование окна
        """
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        window.geometry(f"{width}x{height}+{x}+{y}")

    def run(self):
        """Запуск приложения"""
        self.root.mainloop()