from pathlib import Path
import ctypes
import os
from tkinter import *
import customtkinter as ctk
import queries
import helperFunctions


class LoginWindow:
    def __init__(self,window):
        self.window = window
        
        
    def start(self):
        self.return_value = 0
        self.setup_window()
        self.create_canvas()
        self.create_widgets()
        self.window.mainloop()
        return self.return_value
        
    def setup_window(self):
        ctk.set_appearance_mode("Dark")
        self.window.title("Uloguj se")
        self.window.geometry("760x450")
        self.window.configure(bg = "#03050B")
        self.window.resizable(False, False)
        helperFunctions.centerWindow(self.window)
        self.window.iconbitmap("src/img/Logo/TFLogo.ico")
        if os.name == "nt":
            app_id = "mycompany.myapp.subapp"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
            
    def create_widgets(self):
        #korisnicko ime
        self.entryUsername = self.create_entry(403, 225, "Korisničko ime", self.on_entry_click_username, self.on_focus_out_username) 
        self.entryUsername.bind("<KeyRelease>", self.promeni_pozdrav)
        
        #lozinka
        self.entryPassword = self.create_entry(403, 281, "Lozinka", self.on_entry_click_password, self.on_focus_out_password, show='•')
        self.entryPassword.bind("<Return>", self.prijavi_se)
        
        #login dugme
        self.login_image = PhotoImage(file="src/img/login/button_1.png")
        self.btnLogin = Button(image=self.login_image, borderwidth=0, highlightthickness=0, command=self.prijavi_se, relief="flat")
        self.btnLogin.place(x=475.0, y=351.0, width=160.0, height=35.0)
        
        # nemas nalog dugme
        self.signup_image = PhotoImage(file="src/img/login/button_2.png")
        self.btnSignup = Button(image=self.signup_image, borderwidth=0, highlightthickness=0, command=lambda: self.vrati("signup"), relief="flat")
        self.btnSignup.place(x=513.0, y=396.0, width=80.0, height=15.0)
        
        # promeni tab order jer ide normalno
        self.entryPassword.bind("<Tab>", self.set_custom_tab_order)
        self.entryUsername.bind("<Tab>", self.set_custom_tab_order)
    
    def create_canvas(self):
        self.canvas = Canvas(
            self.window,
            bg="#03050B",
            height=450,
            width=760,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        
        self.imgPozadina = PhotoImage(file="src/img/login/image_1.png")
        self.canvas.create_image(386.0, 226.0, image=self.imgPozadina)

        self.imgLogo = PhotoImage(file="src/img/Logo/TopFormLogoBeliMali2.png")
        self.canvas.create_image(565.0, 74.0, image=self.imgLogo)

        self.text_id = self.canvas.create_text(
            388.0, 171.0, anchor="nw", text="Pozdrav,", fill="#FFFFFF", font=("Inter", 24 * -1)
        )

        self.canvas.create_rectangle(403, 247.7, 706, 248.0, fill="#FFFFFF", outline="")
        self.canvas.create_rectangle(403, 302.7, 706, 303.0, fill="#FFFFFF", outline="")
    
    def create_entry(self, x, y, placeholder, on_focus_in, on_focus_out, show=''):
        entry = Entry(
            bd=0, bg="#1A1B20", fg="#FFFFFF", highlightthickness=0, show=show
        )
        entry.place(x=x, y=y, width=303.0, height=20.0)
        entry.insert(0, placeholder)
        entry.configure(foreground="gray")
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        return entry

    def promeni_pozdrav(self, event):
        self.canvas.itemconfig(self.text_id, text="Pozdrav, " + str(self.entryUsername.get()))
    
    def vrati(self,text):
        #self.window.after_cancel()
        self.window.quit()
        self.return_value=text
        
    def prijavi_se(self,event=None):
        korIme=str(self.entryUsername.get())
        loz=helperFunctions.hashPassword(str(self.entryPassword.get()))
        queries.cursor.execute("SELECT username, uloga FROM Korisnici WHERE username='"+str(korIme)+"' AND password='"+str(loz)+"'")
        ima=queries.cursor.fetchall()
        if(len(ima)!=0):
            self.vrati(ima)
        else:
            helperFunctions.pisi_eror("Pogrešno korisničko ime ili lozinka")
            
    def on_entry_click_username(self,event):
        if self.entryUsername.get() == "Korisničko ime":
            self.entryUsername.delete(0, END)
            self.entryUsername.configure(foreground="white")

    def on_focus_out_username(self,event):
        if self.entryUsername.get() == "":
            self.entryUsername.insert(0, "Korisničko ime")
            self.entryUsername.configure(foreground="gray")
    
    def on_entry_click_password(self,event):
        if self.entryPassword.get() == "Lozinka":
            self.entryPassword.delete(0, END)
            self.entryPassword.configure(foreground="white")
            self.entryPassword.configure(show='•')

    def on_focus_out_password(self,event):
        if self.entryPassword.get() == "":
            self.entryPassword.insert(0, "Lozinka")
            self.entryPassword.configure(foreground="gray",show='')
    
    def set_custom_tab_order(self, event):
        if event.widget == self.entryUsername:
            self.entryPassword.focus_set()
        elif event.widget == self.entryPassword:
            self.entryUsername.focus_set()
        else:
            self.entryUsername.focus_set()
        return "break"