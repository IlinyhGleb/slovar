from setuptools import setup
import os
import sys
from PyInstaller.__main__ import run

# Определите имя вашего исполняемого файла
exe_name = 'slovar'

# Опции для PyInstaller
pyinstaller_options = [
    '--onefile',  # Создание одного исполняемого файла
    '--add-data', 'texts.json;.',  # Копирование файла рядом с .exe
    'main.py',  # Ваш скрипт
]


class PyInstallerCommand:
    """Команда для вызова PyInstaller из setup.py."""

    def run(self):
        run(pyinstaller_options)


setup(
    name='slovar',
    version='0.1.0',
    author='Gleb Ilinyh',
    author_email='gleb@ilinyh.ru',
    description='Мини-программа для запоминания слов',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/IlinyhGleb/slovar',  # Укажите ссылку на ваш репозиторий
    cmdclass={'build_exe': PyInstallerCommand},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Укажите тип лицензии
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Минимальная версия Python
)
