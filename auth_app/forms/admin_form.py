import tkinter as tk
from tkinter import ttk, messagebox
from database.db_manager import DatabaseManager

class AdminForm:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
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
        self.center_window(self.root, width, height)

    def create_widgets(self):
        """Создание виджетов формы"""
        main_frame = ttk.Frame(self.root, padding= "20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)

        title_label = ttk.Label(
            main_frame,
            text="Панель администратора",
            font=("Arial", 18, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 20), columnspan=3)

        add_button = ttk.Button(
            main_frame,
            text="Добавить",
            command=self.show_add_dialog
        )
        add_button.grid(row=1, column=0, sticky="e", pady=(0, 20))

        edit_button = ttk.Button(
            main_frame,
            text="Редактировать",
            command=self.show_edit_dialog
        )
        edit_button.grid(row=1, column=1, sticky="e", pady=(0, 20))

        delete_button = ttk.Button(
            main_frame,
            text="Удалить",
            command=self.delete_user
        )
        delete_button.grid(row=1, column=2, sticky="e", pady=(0, 20))

        columns = ("login", "password", "role", "is_blocked")

        self.users_tree = ttk.Treeview(main_frame, columns=columns, show="headings")
        self.users_tree.grid(row=2, column=0, sticky="nsew", columnspan=3)

        self.users_tree.heading("login", text="Логин")
        self.users_tree.heading("password", text="Пароль")
        self.users_tree.heading("role", text="Роль")
        self.users_tree.heading("is_blocked", text="Заблокирован")

    def load_users(self):
        """
        Заполнение таблицы данными
        """
        for users in self.users_tree.get_children():
            self.users_tree.delete(users)

        users = self.db.get_all_users()
        for user in users:
            self.users_tree.insert("", 'end', values=user)

    def show_edit_dialog(self):
        """
        Окно редактирования данных пользователя
        """
        if self.dialog_edit is not None:
            self.dialog_edit.destroy()

        selected = self.users_tree.selection()
        if not selected:
            messagebox.showinfo(
                "Выбор пользователя",
                "Сначала выберите пользователя"
            )
            self.dialog_edit.lift()
            return

        values = self.users_tree.item(selected[0], 'values')
        login, password, role, is_blocked = values

        self.dialog_edit = tk.Toplevel(self.root)
        self.dialog_edit.title("Редактировать пользователя")
        width = 400
        height = 400
        self.dialog_edit.minsize(width, height)
        self.dialog_edit.grid_columnconfigure(0, weight=1)
        self.dialog_edit.grid_rowconfigure(0, weight=1)
        self.center_window(self.dialog_edit, width, height)

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
            command= lambda : self.edit_user(login)
        )
        save_button.grid(row=2, column=0, pady=(0, 20))

        login_frame = ttk.Frame(main_frame_dialog, padding="20")
        login_frame.grid(column=0, row=1, sticky="nsew", padx=(0, 10))
        login_frame.grid_columnconfigure(0, weight=1)

        # Логин
        login_label = ttk.Label(login_frame, text=f"Логин: {login}")
        login_label.grid(column=0, row=1, sticky="w", pady=(0, 15))

        # Пароль
        password_label = ttk.Label(login_frame, text="Пароль:")
        password_label.grid(column=0, row=3, sticky="w")
        self.password_entry = ttk.Entry(login_frame, width=30)
        self.password_entry.grid(column=0, row=4, sticky="ew", pady=(0, 15))
        self.password_entry.insert(0, password)

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
        self.center_window(self.dialog_add, width, height)

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
        self.password_entry = ttk.Entry(login_frame, width=30)
        self.password_entry.grid(column=0, row=4, sticky="ew", pady=(0, 15))

        # Роль
        role_label = ttk.Label(login_frame, text="Роль:")
        role_label.grid(column=0, row=5, sticky="w")
        self.role_entry = ttk.Combobox(login_frame, width=30, values=["Пользователь","Администратор"], state="readonly")
        self.role_entry.grid(column=0, row=6, sticky="ew", pady=(0, 15))

    def add_user(self):
        """
        Сохранение нового пользователя
        """
        role = 0
        login = self.login_entry.get()
        password = self.password_entry.get()
        role_name = self.role_entry.get()
        if role_name == "Пользователь":
            role = 1
        else:
            role = 2

        if login == "" or password == "" or role_name == "":
            messagebox.showinfo(
                "Ошибка ввода",
                "Все поля должны быть заполнены!!!"
            )
            self.dialog_add.lift()
            return

        if self.db.user_serch(login):
            messagebox.showinfo(
                "Ошибка ввода",
                "Пользователь уже существует!!!"
            )
            self.dialog_add.lift()
            return

        self.db.add_user(login, password, role)
        messagebox.showinfo(
            "Пользователь добавлен",
            "Новый пользователь успешно добавлен."
        )
        self.load_users()
        self.dialog_add.destroy()

    def edit_user(self, login:str):
        """
        Обновление данных
        """
        role = 0
        login = login
        password = self.password_entry.get()
        role_name = self.role_entry.get()
        is_blocked = self.blocked_var.get()

        if role_name == "Пользователь":
            role = 1
        else:
            role = 2

        if password == "" or role_name == "":
            messagebox.showinfo(
                "Ошибка ввода",
                "Все поля должны быть заполнены!!!"
            )
            self.dialog_edit.lift()
            return

        self.db.edit_user(login, password, role, is_blocked)
        messagebox.showinfo(
            "Пользователь отредактирован",
            "Пользователь успешно отредактирован."
        )

        self.load_users()
        self.dialog_edit.destroy()

    def delete_user(self):
        """
        Удаление пользователя
        """
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showinfo(
                "Выбор пользователя",
                "Сначала выберите пользователя."
            )
            return

        values = self.users_tree.item(selected[0], 'values')
        login = values[0]

        self.db.delete_user(login)
        messagebox.showinfo(
            "Удаление пользователя",
            "Пользователь успешно удалён."
        )
        self.load_users()

    def center_window(self, window, width, height):
        """
        Центрирование окна
        """
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        window.geometry(f"{width}x{height}+{x}+{y}")

    def set_tab(self):
        self.login_entry.focus_set()
        self.password_entry.bind("<Tab>", lambda e: self.password_entry.focus_set())
        self.role_entry.bind("<Tab>", lambda e: self.role_entry.focus_set())

    def run(self):
        self.root.mainloop()