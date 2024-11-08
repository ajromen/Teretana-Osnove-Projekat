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
            if(return_value=="login"): 
                queries.obrisiKorisnika(user)
                user=''
            if(return_value!="login"): break
    return return_value

def vozi(ekran,user=''):
    return_value=login_startup_loop(ekran,user)
    if(return_value=="gost"):
        username=queries.napraviGosta()
        return_value=[[username,-1]]
    if(return_value==0): return
    return winMain.start(return_value[0][0],return_value[0][1])


if __name__ == '__main__':
    staDaRadim="login"
    user=''
    lista=[0,0]
    while(True):
        staDaRadim=vozi(staDaRadim,user)
        user=''
        if(staDaRadim!="login" and staDaRadim!="signup" and type(staDaRadim)!=type(lista)):
            break
        if(type(staDaRadim)==type(lista)):
            user=staDaRadim[1]
            staDaRadim=staDaRadim[0]
        
    queries.connection.commit()
