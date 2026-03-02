import PyInstaller.__main__
import customtkinter
import os

ctk_path = os.path.dirname(customtkinter.__file__)

PyInstaller.__main__.run([
    'src/passkeeper/gui/app.py',
    '--noconfirm',
    '--onedir',
    '--windowed',
    '--name', 'Passkeeper',
    '--add-data', f'{ctk_path};customtkinter/'
])
