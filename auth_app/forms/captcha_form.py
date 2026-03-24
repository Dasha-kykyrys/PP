import tkinter as tk
from PIL import Image, ImageTk
import random

class CaptchaPuzzle(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.images = []
        self.buttons = []
        self.orders = [0, 1, 2, 3]

        # Загрузка изображений
        for i in range(1, 5):
            self.images.append(ImageTk.PhotoImage(Image.open(f"images/{i}.png").resize((100, 100))))

        self.pressed_button = None

        self.create_widgets()

    def create_widgets(self):
        random.shuffle(self.orders)

        # Присваивание изображений по перемешанному порядку
        for i, (row, col) in enumerate([(0, 0), (0, 1), (1, 0), (1, 1)]):
            image_button = tk.Button(self, image=self.images[self.orders[i]],
                            command=lambda idx=i: self.on_click(idx))
            image_button.grid(row=row, column=col)
            self.buttons.append(image_button)

    def on_click(self, i):
        """
        Смена картинок между кнопками, сохранение текущего порядка картиноке
        """
        if self.pressed_button is not None:
            # Изменение порядка
            temp_order = self.orders[i]
            self.orders[i] =  self.orders[self.pressed_button]
            self.orders[self.pressed_button] = temp_order

            # Изменение картинок
            self.buttons[i].config(image=[self.images[self.orders[i]]])
            self.buttons[self.pressed_button].config(image=self.images[self.orders[self.pressed_button]])
            self.pressed_button = None
        else:
            self.pressed_button = i

    def check_captcha(self) -> bool:
        return self.orders == [0, 1, 2, 3]

