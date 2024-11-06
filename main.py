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
#window=CTk()

winLogin=winLoginOOP.LoginWindow()
print(winLogin.start())

def login_startup_loop(user):
    return_value=0
    while(1):
        return_value=winLogin.start()
        if(return_value!="signup"):
            print(return_value)
            break;
        return_value=winSignup.start(user)
        if(return_value!="login"):
            break;
    return return_value


return_value=login_startup_loop('None')
print("ovja lik : "+str(return_value))


queries.connection.commit()


