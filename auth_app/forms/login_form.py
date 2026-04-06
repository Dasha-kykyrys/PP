import tkinter as tk
from tkinter import ttk, messagebox
from requests.user_requests import UserRequests
from requests.auth_requests import AuthRequests
from forms.admin_form import AdminForm
from forms.user_form import UserForm
from forms.captcha_form import CaptchaPuzzle
from utils.window_utils import center_window

class LoginForm:
    """Форма авторизации пользователей с капчей"""

    def __init__(self):
        self.user_dao = UserRequests()
        self.auth_dao = AuthRequests()

        self.root = tk.Tk()
        self.root.title("Авторизация")
        width = 400
        height = 500
        self.root.minsize(width, height)

        self.max_attempts = 3

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.create_widgets()
        self.set_tab()
        center_window(self.root, width, height)

    def create_widgets(self):
        """Создание виджетов формы"""
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(column=0, row=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)

        title_label = ttk.Label(
            main_frame,
            text="Авторизация",
            font=("Arial", 18, "bold")
        )
        title_label.grid(column=0, row=0, pady=(0, 20))

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

    def handle_login(self):
        """Обработка попытки входа"""
        login = self.login_entry.get()
        password = self.password_entry.get()

        if login == "" or password == "":
            messagebox.showerror(
                "Ошибка ввода",
                "Все поля должны быть заполнены!!!"
            )
            return

        if self.auth_dao.user_search(login):
            failed_attempts = self.auth_dao.get_failed_attempts(login)
            if self.auth_dao.get_user_status(login):
                self.block_user_message()
                return
            if self.auth_dao.authenticate(login, password):
                if self.captcha.check_captcha():
                    messagebox.showinfo(
                        "Авторизация",
                        "Вы успешно авторизовались"
                    )
                    if self.auth_dao.get_user_role(login):
                        self.root.destroy()
                        admin_form = AdminForm(self.user_dao, self.auth_dao)
                        admin_form.run()
                    else:
                        self.root.destroy()
                        user_form = UserForm()
                        user_form.run()
                else:
                    failed_attempts += 1
                    self.auth_dao.edit_failed_attempts(login, failed_attempts)
                    if failed_attempts == self.max_attempts:
                        self.block_user_message()
                        self.auth_dao.block_user(login)
                        return
                    messagebox.showerror(
                        "Ошибка проверки",
                        "Картинка собрана неверно."
                    )
            else:
                failed_attempts += 1
                self.auth_dao.edit_failed_attempts(login, failed_attempts)
                if failed_attempts == self.max_attempts:
                     self.block_user_message()
                     self.auth_dao.block_user(login)
                     return
                self.error_authorization_message()
        else:
            self.error_authorization_message()
            return

    def error_authorization_message(self):
        """
        Сообщение о неверных данных
        """
        messagebox.showerror(
            "Ошибка авторизации",
            "Вы ввели неверный логин или пароль. Пожалуйста проверьте ещё раз введенные данные."
        )

    def block_user_message(self):
        """
        Сообщение о блокировке
        """
        messagebox.showwarning(
            "Блокировка",
            "Вы заблокированы. Обратитесь к администратору"
        )

    def set_tab(self):
        """Настройка последовательного перехода фокуса по Tab"""
        self.login_entry.focus_set()
        self.password_entry.bind("<Tab>", lambda e: self.enter_button.focus_set())
        self.enter_button.bind("<Tab>", lambda e: self.login_entry.focus_set())

    def run(self):
        """Запуск приложения"""
        self.root.mainloop()