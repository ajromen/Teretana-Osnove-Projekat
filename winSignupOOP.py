import os
import ctypes
from tkinter import *
import customtkinter as ctk
import queries
from datetime import date
import helperFunctions

class winSingup:
    def __init__(self,window):
        self.window = window
        self.return_value = 0
        self.setup_window()
        self.create_canvas()
        self.create_widgets()
        
    def start(self):
        self.window.mainloop()
        return self.return_value
        
    def setup_window(self):
        ctk.set_appearance_mode("Dark")
        self.window.title("Uloguj se")
        self.window.geometry("760x450")
        self.window.configure(bg = "#03050B")
        self.window.resizable(False, False)
        helperFunctions.centerWindow(self.window)
        self.window.iconbitmap("src/img/TFLogo.ico")
        if os.name == "nt":
            app_id = "mycompany.myapp.subapp"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
            