import tkinter as tk
from customtkinter import *
import sys


import queries
import helperFunctions
#import winLogin
import winSignup
import chatgpt
import winLoginOOP

#queries.executeScriptsFromFile("src/sql/Teretana.sql")
#queries.executeScriptsFromFile("src/sql/TeretanaUnosPodataka.sql")

'''window = CTk()
set_appearance_mode("Dark")
helperFunctions.centerWindow(window)
'''
winLogin=winLoginOOP.LoginWindow()




def login_startup_loop(window,user):
    return_value=0
    while(1):
        return_value=winLogin.start()
        if(return_value!="signup"):
            print(return_value)
            break;
        return_value=winSignup.start(window,user)
        if(return_value!="login"):
            break;
    return return_value

window = CTk()
set_appearance_mode("Dark")
helperFunctions.centerWindow(window)

return_value=login_startup_loop(window,'None')
print("ovja lik : "+str(return_value))


queries.connection.commit()


