import tkinter as tk
from customtkinter import *
import sys


import queries
import helperFunctions
import login
import signup

#queries.executeScriptsFromFile("src/sql/Teretana.sql")
#queries.executeScriptsFromFile("src/sql/TeretanaUnosPodataka.sql")

window = CTk()
set_appearance_mode("Dark")
window.update_idletasks()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_width = window.winfo_width()
window_height = window.winfo_height()
x = (screen_width // 2) - (window_width)*2
y = (screen_height // 2) - (window_height)*1.2
window.geometry(f"{window_width}x{window_height}+{x}+{y}")
window.focus()
window.grab_set()


def login_startup_loop(window,user):
    return_value=0
    while(1):
        return_value=login.start(window)
        if(return_value!="signup"):
            print(return_value)
            break;
        return_value=signup.start(window,user)
        if(return_value!="login"):
            break;
    return return_value

return_value=login_startup_loop(window,'None')
print("ovja lik : "+str(return_value))


queries.connection.commit()


