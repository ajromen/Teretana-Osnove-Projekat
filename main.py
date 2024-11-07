from customtkinter import *
import queries
import helperFunctions
import winLogin
import winSignup
import winMain

#queries.restartuj_bazu()

window=CTk()
winLogin=winLogin.LoginWindow(window)
winSignup=winSignup.SignupWindow(window)
winMain=winMain.MainWindow(window)

def login_startup_loop(ekran,user=''):
    return_value=ekran
    while(1):
        if(return_value=="login"):
            return_value=winLogin.start()
            if(return_value!="signup"): break
        if(return_value=="signup"):
            return_value=winSignup.start(user)
            if(return_value!="login"): break
    return return_value

def vozi(ekran,user=''):
    return_value=login_startup_loop(ekran)
    print("ovja lik : "+str(return_value))
    if(return_value=="gost"):
        username=queries.napraviGosta()
        return_value=[[username,-1]]
    if(return_value==0): return
    return winMain.start(return_value[0][0],return_value[0][1])

staDaRadim="login"
user=''
while(True):
    staDaRadim=vozi(staDaRadim,user)
    print(staDaRadim)
    if(staDaRadim!="login" and staDaRadim!="signup" and type(staDaRadim)!="list"):
        break
    
queries.connection.commit()
