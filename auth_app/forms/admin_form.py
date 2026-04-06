import tkinter as tk
from tkinter import ttk, messagebox
from requests.auth_requests import AuthRequests
from requests.user_requests import UserRequests
from utils.window_utils import center_window

class AdminForm:
    def __init__(self, user_dao: UserRequests, auth_dao: AuthRequests):
        self.user_dao = user_dao
        self.auth_dao = auth_dao
        self.root = tk.Tk()
        self.root.title("Панель администратора")
        width = 800
        height = 400
        self.root.minsize(width, height)

        self.dialog_add = None
        self.dialog_edit = None

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.create_widgets()
        self.load_users()
        center_window(self.root, width, height)

    def create_widgets(self):
        """Создание виджетов формы"""
        main_frame = ttk.Frame(self.root, padding= "20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)

        exit_button = ttk.Button(
            main_frame,
            text="Выход из учётной записи",
            command=self.exit
        )
        exit_button.grid(row=0, column=0, sticky="w")

        title_label = ttk.Label(
            main_frame,
            text="Панель администратора",
            font=("Arial", 18, "bold")
        )
        title_label.grid(row=1, column=0, pady=(0, 20), columnspan=3)

        add_button = ttk.Button(
            main_frame,
            text="Добавить",
            command=self.show_add_dialog
        )
        add_button.grid(row=2, column=0, sticky="e", pady=(0, 20))

        edit_button = ttk.Button(
            main_frame,
            text="Редактировать",
            command=self.show_edit_dialog
        )
        edit_button.grid(row=2, column=1, sticky="e", pady=(0, 20))

        unblock_button = ttk.Button(
            main_frame,
            text="Снять блокировку",
            command=self.unblock_user
        )
        unblock_button.grid(row=2, column=2, sticky="e", pady=(0, 20))

        columns = ("login", "role", "is_blocked")

        self.users_tree = ttk.Treeview(main_frame, columns=columns, show="headings")
        self.users_tree.grid(row=3, column=0, sticky="nsew", columnspan=3)

        self.users_tree.heading("login", text="Логин")
        self.users_tree.heading("role", text="Роль")
        self.users_tree.heading("is_blocked", text="Заблокирован")

    def load_users(self):
        """
        Заполнение таблицы данными
        """
        for users in self.users_tree.get_children():
            self.users_tree.delete(users)

        users = self.user_dao.get_all_users()
        for user in users:
            self.users_tree.insert("", 'end', values=user)

    def unblock_user(self):
        """
        Разблокировка пользователя по кнопке
        """
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showerror(
                "Выбор пользователя",
                "Сначала выберите пользователя"
            )
            return

        values = self.users_tree.item(selected[0], 'values')
        self.user_dao.unblock_user(values[0])
        self.auth_dao.edit_failed_attempts(values[0],0)
        self.load_users()

    def show_edit_dialog(self):
        """
        Окно редактирования данных пользователя
        """
        if self.dialog_edit is not None:
            self.dialog_edit.destroy()

        selected = self.users_tree.selection()
        if not selected:
            messagebox.showerror(
                "Выбор пользователя",
                "Сначала выберите пользователя"
            )
            return

        values = self.users_tree.item(selected[0], 'values')
        old_login, role, is_blocked = values

        self.dialog_edit = tk.Toplevel(self.root)
        self.dialog_edit.title("Редактировать пользователя")
        width = 400
        height = 400
        self.dialog_edit.minsize(width, height)
        self.dialog_edit.grid_columnconfigure(0, weight=1)
        self.dialog_edit.grid_rowconfigure(0, weight=1)
        center_window(self.dialog_edit, width, height)

        main_frame_dialog = ttk.Frame(self.dialog_edit, padding="20")
        main_frame_dialog.grid(row=0, column=0, sticky="nsew")
        main_frame_dialog.grid_columnconfigure(0, weight=1)

        label_add = ttk.Label(
            main_frame_dialog,
            text="Редактировать пользователя",
            font=("Arial", 18, "bold")
        )
        label_add.grid(column=0, row=0, pady=(0, 20))

        save_button = ttk.Button(
            main_frame_dialog,
            text="Сохранить",
            command= lambda : self.edit_user(old_login)
        )
        save_button.grid(row=2, column=0, pady=(0, 20))

        cancel_button = ttk.Button(
            main_frame_dialog,
            text="Отменить",
            command= lambda : self.cancel_action(self.dialog_edit)
        )
        cancel_button.grid(row=3, column=0, pady=(0, 20))

        login_frame = ttk.Frame(main_frame_dialog, padding="20")
        login_frame.grid(column=0, row=1, sticky="nsew", padx=(0, 10))
        login_frame.grid_columnconfigure(0, weight=1)

        # Логин
        login_label = ttk.Label(login_frame, text=f"Логин:")
        login_label.grid(column=0, row=1, sticky="w", pady=(0, 15))
        self.login_entry = ttk.Entry(login_frame, width=30)
        self.login_entry.grid(column=0, row=2, sticky="ew", pady=(0, 15))
        self.login_entry.insert(0, old_login)

        # Пароль
        password_label = ttk.Label(login_frame, text="Пароль:")
        password_label.grid(column=0, row=3, sticky="w")
        self.password_entry = ttk.Entry(login_frame, show="*", width=30)
        self.password_entry.grid(column=0, row=4, sticky="ew", pady=(0, 15))

        # Роль
        role_label = ttk.Label(login_frame, text="Роль:")
        role_label.grid(column=0, row=5, sticky="w")
        self.role_entry = ttk.Combobox(login_frame, width=30, values=["Пользователь", "Администратор"],
                                       state="readonly")
        self.role_entry.grid(column=0, row=6, sticky="ew", pady=(0, 15))
        self.role_entry.set(role)

        # Блокировка
        self.blocked_var = tk.BooleanVar(value=is_blocked)
        self.blocked_check = ttk.Checkbutton(
            login_frame,
            text="Заблокирован",
            variable=self.blocked_var
        )
        self.blocked_check.grid(column=0, row=7, sticky="ew", pady=(0, 15))

    def show_add_dialog(self):
        """
        Окно добавления нового пользователя
        """
        if self.dialog_add is not None:
            self.dialog_add.destroy()

        self.dialog_add = tk.Toplevel(self.root)
        self.dialog_add.title("Добавить пользователя")
        width = 400
        height = 400
        self.dialog_add.minsize(width, height)
        self.dialog_add.grid_columnconfigure(0, weight=1)
        self.dialog_add.grid_rowconfigure(0, weight=1)
        center_window(self.dialog_add, width, height)

        main_frame_dialog = ttk.Frame(self.dialog_add, padding="20")
        main_frame_dialog.grid(row=0, column=0, sticky="nsew")
        main_frame_dialog.grid_columnconfigure(0, weight=1)

        label_add = ttk.Label(
            main_frame_dialog,
            text="Добавить пользователя",
            font=("Arial", 18, "bold")
            )
        label_add.grid(column=0, row=0, pady=(0, 20))

        add_button = ttk.Button(
            main_frame_dialog,
            text="Сохранить",
            command=self.add_user
        )
        add_button.grid(row=2, column=0, pady=(0, 20))

        cancel_button = ttk.Button(
            main_frame_dialog,
            text="Отменить",
            command= lambda : self.cancel_action(self.dialog_add)
        )
        cancel_button.grid(row=3, column=0, pady=(0, 20))

        login_frame = ttk.Frame(main_frame_dialog, padding="20")
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
        self.password_entry.grid(column=0, row=4, sticky="ew", pady=(0, 15))

        # Роль
        role_label = ttk.Label(login_frame, text="Роль:")
        role_label.grid(column=0, row=5, sticky="w")
        self.role_entry = ttk.Combobox(login_frame, width=30, values=["Пользователь","Администратор"], state="readonly")
        self.role_entry.grid(column=0, row=6, sticky="ew", pady=(0, 15))

    def exit(self):
        from forms.login_form import LoginForm
        self.root.destroy()
        login_form = LoginForm()
        login_form.run()

    def cancel_action(self, dialog):
        dialog.destroy()

    def add_user(self):
        """
        Сохранение нового пользователя
        """
        login = self.login_entry.get()
        password = self.password_entry.get()
        role_name = self.role_entry.get()
        if role_name == "Пользователь":
            role = 1
        else:
            role = 2

        if login == "" or password == "" or role_name == "":
            messagebox.showerror(
                "Ошибка ввода",
                "Все поля должны быть заполнены!!!"
            )
            self.dialog_add.lift()
            return

        if self.auth_dao.user_search(login):
            messagebox.showerror(
                "Ошибка ввода",
                "Пользователь уже существует!!!"
            )
            self.dialog_add.lift()
            return

        if not self.validate_login(login):
            self.dialog_add.lift()
            return
        if not self.validate_password(password):
            self.dialog_add.lift()
            return

        self.user_dao.add_user(login, password, role)
        messagebox.showinfo(
            "Пользователь добавлен",
            "Новый пользователь успешно добавлен."
        )
        self.load_users()
        self.dialog_add.destroy()

    def edit_user(self, old_login:str):
        """
        Обновление данных
        """
        old_login = old_login
        new_login = self.login_entry.get()
        password = self.password_entry.get()
        role_name = self.role_entry.get()
        is_blocked = self.blocked_var.get()
        if not is_blocked:
            self.auth_dao.edit_failed_attempts(old_login, 0)

        if role_name == "Пользователь":
            role = 1
        else:
            role = 2

        if  new_login == "" or role_name == "":
            messagebox.showerror(
                "Ошибка ввода",
                "Все поля должны быть заполнены!!!"
            )
            self.dialog_edit.lift()
            return

        if new_login != old_login:
            if self.auth_dao.user_search(new_login):
                messagebox.showerror(
                    "Ошибка ввода",
                    "Пользователь уже существует!!!"
                )
                self.dialog_edit.lift()
                return
            if not self.validate_login(new_login):
                self.dialog_edit.lift()
                return


        if password == "":
            self.user_dao.edit_user_without_password(old_login, new_login, role, is_blocked)
        else:
            if not self.validate_password(password):
                self.dialog_edit.lift()
                return
            self.user_dao.edit_user(old_login, new_login, password, role, is_blocked)

        messagebox.showinfo(
            "Пользователь отредактирован",
            "Пользователь успешно отредактирован."
        )

        self.load_users()
        self.dialog_edit.destroy()

    def validate_login(self,login: str) -> bool:
        """Проверка корректности логина"""
        if len(login) < 3 or len(login) > 100:
            messagebox.showerror(
                "Ошибка",
                "Логин должен быть от 3 до 100 символов")
            return False
        return True

    def validate_password(self, password: str) -> bool:
        """Проверка корректности пароля"""
        if len(password) < 4 or len(password) > 255:
            messagebox.showerror(
                "Ошибка",
                "Пароль должен быть от 4 до 255 символов")
            return False
        return True

    def set_tab(self):
        self.login_entry.focus_set()
        self.password_entry.bind("<Tab>", lambda e: self.password_entry.focus_set())
        self.role_entry.bind("<Tab>", lambda e: self.role_entry.focus_set())

    def run(self):
        self.root.mainloop()