import tkinter as tk
from tkinter import ttk

class UserForm:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Панель пользователя")
        width = 800
        height = 400
        self.root.minsize(width, height)

        self.dialog_add = None
        self.dialog_edit = None

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.create_widgets()
        self.center_window(self.root, width, height)

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
            text="Панель пользователя",
            font=("Arial", 18, "bold")
        )
        title_label.grid(row=1, column=0, pady=(0, 20), columnspan=3)

    def exit(self):
        from forms.login_form import LoginForm
        self.root.destroy()
        login_form = LoginForm()
        login_form.run()

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
        self.root.mainloop()