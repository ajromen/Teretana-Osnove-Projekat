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

def login_startup_loop():
    return_value=0
    while(1):
        return_value=winLogin.start()
        if(return_value!="signup"):
            break;
        
        return_value=winSignup.start()
        if(return_value!="login"):
            break;
    return return_value

return_value=login_startup_loop()
print("ovja lik : "+str(return_value))
if(return_value=="gost"):
    pass

winMain.start(return_value[0][0],return_value[0][1])

queries.connection.commit()
