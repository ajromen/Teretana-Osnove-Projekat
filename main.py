from customtkinter import *
import Queries.queries as queries
sys.path.append('./MainProzori')
sys.path.append('./Queries')
import winLogin
import winSignup
import winMain

queries.restartuj_bazu()

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
    return_value=login_startup_loop(ekran,user)
    
    if(return_value=="gost"):
        username=queries.napraviGosta()
        return_value=[[username,-1]]
    if(return_value==0): return
    return winMain.start(return_value[0][0],return_value[0][1])

if __name__ == '__main__':
    window=CTk()
    
    winLogin=winLogin.LoginWindow(window)
    winSignup=winSignup.SignupWindow(window)
    winMain=winMain.MainWindow(window)
    
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
        
    queries.proveri_status_korisnika()
    queries.obrisi_goste()
    queries.connection.commit()
