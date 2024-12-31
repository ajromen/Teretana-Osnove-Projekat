import sys
sys.path.append('./misc')
from imports import *
import winLogin
import winSignup
import winMain
import bp_korisnici
import bp_termini
from baza_podataka import BazaPodataka

def login_startup_loop(ekran,user=''):
    return_value=ekran
    while True:   
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
        username=bp_korisnici.dodaj_gosta()
        return_value=[[username,-1]]
    if(return_value==0): return
    return winMain.start(return_value[0][0],return_value[0][1])

def azuriraj_podatke():
    bp_termini.generisi_termine()
    bp_korisnici.proveri_status_korisnika()
    bp_korisnici.obrisi_goste()
    BazaPodataka.commit()
    

if __name__ == '__main__':
    # BazaPodataka.restart()
    azuriraj_podatke()
    
    window=ctk.CTk()
    winLogin=winLogin.LoginWindow(window)
    winSignup=winSignup.SignupWindow(window)
    winMain=winMain.MainWindow(window)
    staDaRadim="login"
    user=''
    lista=[]
    while(True):
        staDaRadim=vozi(staDaRadim,user)
        user=''
        if(staDaRadim!="login" and staDaRadim!="signup" and type(staDaRadim)!=type(lista)):
            break
        if(type(staDaRadim)==type(lista)):
            user=staDaRadim[1]
            staDaRadim=staDaRadim[0]
    
    azuriraj_podatke()
        
    