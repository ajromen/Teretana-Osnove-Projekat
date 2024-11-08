import os
import ctypes
import re
from tkinter import *
import customtkinter as ctk
import queries
from datetime import date
import helperFunctions

class SignupWindow:
    def __init__(self,window):
        self.window = window
          
    def start(self,user=''):
        self.user=user
        self.guest=0
        if(len(user)>0): self.guest=1
        self.return_value = 0
        self.setup_window()
        self.create_canvas()
        self.create_widgets()
        self.window.mainloop()
        return self.return_value
 
    def setup_window(self):
        ctk.set_appearance_mode("Dark")
        self.window.title("Kreiraj nalog")
        self.window.geometry("760x450")
        self.window.configure(bg = "#000000")
        self.window.resizable(False, False)
        helperFunctions.centerWindow(self.window)
        self.window.iconbitmap("src/img/Logo/TFLogo.ico")
        if os.name == "nt":
            app_id = "mycompany.myapp.subapp"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    
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
        
        self.imgPozadina = PhotoImage(file="src/img/Signup/image_1.png")
        self.canvas.create_image(380, 225.0, image=self.imgPozadina)

        self.imgLogo = PhotoImage(file="src/img/Logo/TopFormLogoBeliMali2.png")
        self.canvas.create_image(201.0, 76.0, image=self.imgLogo)

        self.text_id = self.canvas.create_text(39,172, anchor="nw", text="Dobrodošao/la, ", fill="#FFFFFF", font=("Inter SemiBold", 24 * -1))
        self.canvas.create_rectangle(41.0, 230, 352.0, 231, fill="#FFFFFF",outline="")
        self.canvas.create_rectangle(41.0, 274.0, 352, 275.0, fill="#FFFFFF", outline="")
        self.canvas.create_rectangle(41.0, 313.0, 352, 314, fill="#FFFFFF", outline="")
    
    def create_widgets(self):
        self.entryName = self.create_entry(
            x=46.0, y=209.0, placeholder="Ime i Prezime",
            on_focus_in=self.on_name_click, on_focus_out=self.on_name_out
        )
            
        self.entryName.bind("<KeyRelease>", self.promeni_dobrodosao)

        self.entyUsername = self.create_entry(
            x=46.0, y=253.0, placeholder="Korisničko ime",
            on_focus_in=self.on_username_click, on_focus_out=self.on_username_out
        )
        
        if(self.guest):
            self.entyUsername.delete(0, END)
            self.entyUsername.insert(0,self.user)
            self.entyUsername.configure(foreground="white")

        self.entryPassword = self.create_entry(
            x=46.0, y=293.0, placeholder="Lozinka",
            on_focus_in=self.on_password_click, on_focus_out=self.on_password_out, show=''
        )
        self.entryPassword.bind("<Return>", lambda event: self.napraviNalog())

        self.create_button("src/img/Signup/button_3.png", x=121.0, y=337.0, width=160.0, height=35.0, command=self.napraviNalog)
        #self.create_button("src/img/Signup/button_3.png", x=0.0, y=0.0, width=160.0, height=35.0, command=self.List)
        self.create_button("src/img/Signup/button_2.png", x=588.0, y=394.0, width=153.0, height=40.0, command=lambda: self.vrati("gost"))
        self.create_button("src/img/Signup/button_1.png", x=163.0, y=379.0, width=76.0, height=15.0, command=lambda: self.vrati("login"))
    
    
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

    def promeni_dobrodosao(self,event):
        self.canvas.itemconfig(self.text_id, text="Dobrodošao/la, "+str((self.entryName.get().split(' '))[0]))
    
    def create_button(self, image_path, x, y, width, height, command):
        image = PhotoImage(file=image_path)
        button = Button(
            image=image, borderwidth=0, highlightthickness=0, command=command, relief="flat"
        )
        button.image = image  
        button.place(x=x, y=y, width=width, height=height)

    def on_name_click(self, event):
        if self.entryName.get() == "Ime i Prezime":
            self.entryName.delete(0, END)
            self.entryName.configure(foreground="white")

    def on_name_out(self, event):
        if self.entryName.get() == "":
            self.entryName.insert(0, "Ime i Prezime")
            self.entryName.configure(foreground="gray")

    def on_username_click(self, event):
        if self.entyUsername.get() == "Korisničko ime":
            self.entyUsername.delete(0, END)
            self.entyUsername.configure(foreground="white")

    def on_username_out(self, event):
        if self.entyUsername.get() == "":
            self.entyUsername.insert(0, "Korisničko ime")
            self.entyUsername.configure(foreground="gray")

    def on_password_click(self, event):
        if self.entryPassword.get() == "Lozinka":
            self.entryPassword.delete(0, END)
            self.entryPassword.configure(foreground="white", show='•')

    def on_password_out(self, event):
        if self.entryPassword.get() == "":
            self.entryPassword.insert(0, "Lozinka")
            self.entryPassword.configure(foreground="gray", show='')
    
    def vrati(self,text):
        self.return_value=text
        self.window.quit()
    
    def napraviNalog(self):
        username=self.entyUsername.get()
        imeIPrezime=self.entryName.get().split(" ")
        if(len(imeIPrezime)!=2):
            helperFunctions.pisi_eror("Polje ime i prezime mora da ima samo 2 argumenta")
            return
        ime=imeIPrezime[0]
        prezime=imeIPrezime[1]
        lozinka=self.entryPassword.get()
        if(len(lozinka)<6):
            helperFunctions.pisi_eror("Lozinka mora da sadrži više od 6 karaktera")
            return 0
        if(not re.search(r'\d', lozinka)):
            helperFunctions.pisi_eror("Lozinka mora sadržati bar jednu cifru")
            return 0
        uloga=0
        status_clanstva=1
        uplacen_paket=0
        datum_registracije=date.today().strftime("%Y-%m-%d")
        if(not self.guest):
            nalog=queries.napraviNalog(username, lozinka, ime, prezime, uloga,status_clanstva, uplacen_paket,datum_registracije)
        else:
            nalog=queries.azurirajNalog(self.user, username, lozinka, ime, prezime, uloga, status_clanstva, uplacen_paket, datum_registracije)
        self.vrati(nalog)

    def List(self):
        queries.cursor.execute("SELECT * FROM Korisnici")
        print(queries.cursor.fetchall())