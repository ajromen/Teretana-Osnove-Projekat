import ctypes
import hashlib
import os
import customtkinter as ctk
from tkinter import *

def hashPassword(password):
   password_bytes = password.encode('utf-8')
   hash_object = hashlib.sha256(password_bytes)
   return hash_object.hexdigest()

def obavestenje(poruka,title="Greška"):
   error_window = ctk.CTkToplevel(fg_color='#000000')
   error_window.title(title)
   error_window.geometry("350x150")
   error_window.resizable(False, False)
   centerWindow(error_window)

   error_label = ctk.CTkLabel(error_window, text=poruka, fg_color="red")
   error_label.pack(pady=20)

   close_button = ctk.CTkButton(error_window, text="Zatvori", command=error_window.destroy)
   close_button.pack(pady=10)

def pitaj(poruka,title="Greška",text1="Da",text2="Ne"):
   error_window = ctk.CTkToplevel(fg_color='#000000')
   error_window.title(title)
   error_window.geometry("350x150")
   error_window.resizable(False, False)
   centerWindow(error_window)

   error_label = ctk.CTkLabel(error_window, text=poruka, fg_color="red")
   error_label.pack(pady=20)

   result = {"value": False}

   button_1 = ctk.CTkButton(error_window, text=text1,fg_color="#252525", command=lambda: (result.update(value=True), error_window.destroy()),width=140)
   button_2 = ctk.CTkButton(error_window, text=text2, command=lambda: (result.update(value=False), error_window.destroy()),width=140)
   button_1.place(x=28,y=108)
   button_2.place(x=181,y=108)

   error_window.wait_window()

   return result["value"]
   
def setup_window(window,title,width_height,bg_color="#000000"):
   ctk.set_appearance_mode("Dark")
   window.title(title)
   window.geometry(width_height)
   window.configure(bg = bg_color)
   window.resizable(False, False)
   centerWindow(window)
   window.iconbitmap("src/img/Logo/TFLogo.ico")
   if os.name == "nt":
      app_id = "mycompany.myapp.subapp"
      ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
        
def centerWindow(window):
   window.update_idletasks()
   screen_width = window.winfo_screenwidth()
   screen_height = window.winfo_screenheight()
   window_width = window.winfo_width()
   window_height = window.winfo_height()
   x = (screen_width // 2) - (window_width//2)
   y = (screen_height // 2) - (window_height//2)
   window.geometry(f"{window_width}x{window_height}+{x}+{y}")
   window.focus()
   window.grab_set()

def napravi_toplevel(width=343,height=485,title=""):
   trenutni_window = ctk.CTkToplevel(fg_color='#000000')
   trenutni_window.title(title)
   trenutni_window.geometry(str(width)+"x"+str(height))
   trenutni_window.resizable(False,False)
   centerWindow(trenutni_window)
   return trenutni_window