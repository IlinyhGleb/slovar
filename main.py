import tkinter as tk
import json
import os
import sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class TextChanger:
    texts_file_path = resource_path("texts.json")

    def __init__(self, master):
        self.master = master
        self.current_text_index = 0
        self.texts = self.load_texts()  # Загружаем тексты из файла
        self.update_interval = 1000  # Интервал обновления текста (1 секунда)
        self.is_running = True  # Состояние переключения текстов
        self.is_mode_one = True  # Состояние режима отображения

        # Кнопки "Старт", "Стоп" и "Переключить режим"
        button_frame = tk.Frame(master)
        button_frame.pack(pady=10)

        self.start_button = tk.Button(button_frame, text="Старт", command=self.start_text_change)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(button_frame, text="Стоп", command=self.stop_text_change)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.toggle_button = tk.Button(button_frame, text="Переключить режим", command=self.toggle_mode)
        self.toggle_button.pack(side=tk.LEFT, padx=5)

        self.label1 = tk.Label(master, text=self.texts[self.current_text_index]["text1"] if self.texts else '',
                               font=("Arial", 24))
        self.label1.pack(pady=20)

        # Фрейм для ограничения размеров label2
        self.text_frame = tk.LabelFrame(master, width=400, height=200)  # Задаем размеры фрейма
        self.text_frame.pack_propagate(False)  # Отключаем изменение размеров фрейма под содержимое
        self.text_frame.pack(expand='yes', fill='both')

        self.label2 = tk.Label(self.text_frame, wraplength=380, justify="left",
                               font=("Arial", 24))  # Устанавливаем wraplength
        self.label2.pack(expand=True)

        self.delete_button = tk.Button(master, text="Удалить текущий текст", command=self.delete_text)
        self.delete_button.pack(pady=10)

        self.slider = tk.Scale(master, from_=100, to_=10000, orient='horizontal', label='Время обновления (мс)',
                               command=self.update_interval_value, length=300)
        self.slider.set(self.update_interval)
        self.slider.pack(pady=20)

        self.text_entry1 = tk.Entry(master, font=("Arial", 16))
        self.text_entry1.pack(pady=10)
        self.text_entry2 = tk.Entry(master, font=("Arial", 16))
        self.text_entry2.pack(pady=10)

        self.add_button = tk.Button(master, text="Добавить текст", command=self.add_text)
        self.add_button.pack(pady=10)

        self.change_text()  # Запускаем смену текста

    def load_texts(self):
        if os.path.exists(self.texts_file_path):
            with open(self.texts_file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        return []

    def save_texts(self):
        with open(self.texts_file_path, 'w', encoding='utf-8') as file:
            json.dump(self.texts, file, ensure_ascii=False, indent=4)

    def update_interval_value(self, value):
        self.update_interval = int(value)

    def change_text(self):
        if self.is_running:
            if self.texts:
                text1 = self.texts[self.current_text_index]["text1"]
                text2 = self.texts[self.current_text_index]["text2"]

                self.update_labels()

                # Переключение на следующий текст через полный интервал времени
                self.current_text_index = (self.current_text_index + 1) % len(self.texts)
        # Запускаем следующий цикл
        self.master.after(self.update_interval, self.change_text)

    def add_text(self):
        new_text1 = self.text_entry1.get().strip()
        new_text2 = self.text_entry2.get().strip()
        if new_text1 and new_text2:
            self.texts.append({"text1": new_text1, "text2": new_text2})
            self.save_texts()
            self.text_entry1.delete(0, tk.END)
            self.text_entry2.delete(0, tk.END)

    def delete_text(self):
        if self.texts:
            self.texts.pop(self.current_text_index)
            self.current_text_index = max(self.current_text_index - 1, 0)
            self.save_texts()

            if self.texts:
                self.label1.config(text=self.texts[self.current_text_index]["text1"] if self.is_mode_one else self.texts[self.current_text_index]["text2"])
                self.label2.config(text='')  # Убираем текст из label2
            else:
                self.label1.config(text='')
                self.label2.config(text='')

    def toggle_mode(self):
        self.is_mode_one = not self.is_mode_one
        self.update_labels()  # Обновляем метки сразу при переключении

    def update_labels(self):
        if self.texts:
            text1 = self.texts[self.current_text_index]["text1"]
            text2 = self.texts[self.current_text_index]["text2"]
            # В зависимости от режима отображения выводим определённый текст
            if self.is_mode_one:
                self.label1.config(text=text1)
                self.label2.config(text='')  # Убрать текст из label2 заранее
                self.master.after(self.update_interval // 2, lambda: self.label2.config(text=text2))
            else:
                self.label1.config(text=text2)
                self.label2.config(text='')  # Убрать текст из label2 заранее
                self.master.after(self.update_interval // 2, lambda: self.label2.config(text=text1))

    def start_text_change(self):
        self.is_running = True

    def stop_text_change(self):
        self.is_running = False


# Создаем главное окно
root = tk.Tk()
root.title("Slovar")
root.geometry("400x600")  # Устанавливаем исходную ширину и высоту окна

# Создаем объект класса
text_changer = TextChanger(root)

# Запускаем главный цикл
root.mainloop()
