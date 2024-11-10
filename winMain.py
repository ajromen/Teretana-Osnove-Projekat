import datetime
import sys
from tkinter import *
import customtkinter as ctk
import helperFunctions
import queries
import os
import ctypes
sys.path.append('./MainProzori')
import winProgrami

class MainWindow:
    def __init__(self,window):
         self.window=window
         self.programi_window = None
         
    def start(self,username,uloga):
        self.username=username
        self.uloga=self.nadji_ulogu(uloga)
        self.return_value = 0
        self.setup_window()
        self.create_canvas()
        self.create_widgets()
        self.window.mainloop()
        return self.return_value
    
    def setup_window(self):
        ctk.set_appearance_mode("Dark")
        self.window.title("TopForm")
        self.window.geometry("1080x608")
        self.window.configure(bg = "#04050C")
        self.window.resizable(False, False)
        helperFunctions.centerWindow(self.window)
        self.window.iconbitmap("src/img/Logo/TFLogo.ico")
        if os.name == "nt":
            app_id = "mycompany.myapp.subapp"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
            
    def create_canvas(self):
        self.canvas = Canvas(
            self.window,
            bg = "#04050C",
            height = 608,
            width = 1080,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        self.canvas.place(x=0, y=0)
        
        self.imgPozadina = PhotoImage(file="src/img/Main/imgPozadina.png")
        self.canvas.create_image(655, 304, image=self.imgPozadina)
        
        self.imgLogo = PhotoImage(file="src/img/Logo/TopFormLogoBeliSrednji.png")
        self.canvas.create_image(420+465//2, 180+142//2, image=self.imgLogo)
        
        self.imgUser = PhotoImage(file="src/img/Main/imgUser.png")
        self.canvas.create_image(115, 31, image=self.imgUser)

        self.text_id_user = self.canvas.create_text(64,25, anchor="nw", text=self.username, fill="#FFFFFF", font=("Inter Medium", 12 * -1))
        self.text_id_date_time = self.canvas.create_text(475,313, anchor="nw", text="19:49 / Saturday /  01.11.2024", fill="#DFDFDF", font=("Inter", 24 * -1))
        
        self.rect=self.canvas.create_rectangle(218.0, 0, 230.0, 63, fill="#FFFFFF",outline="")

    def create_widgets(self):
        self.napravi_dugmad_po_ulozi()
    
        self.vreme()
    
    def napravi_dugmad_po_ulozi(self):
        role_buttons = {
            "gost": ["btnProgrami","btnTermini","btnRezervacije","btnRegistrujSe"],
            "admin": ["btnVrsteTreninga", "btnTreninzi", "btnProgrami", "btnClanovi", "btnIzvestaji", "btnAdmin","btnOdjaviSe"],
            "instruktor": ["btnRezervacije","btnClanovi", "btnOdjaviSe"],
            "korisnik": ["btnProgrami","btnTermini","btnRezervacije","btnOdjaviSe"]
        }
        buttons = {
            "btnVrsteTreninga": lambda i: self.create_button("src/img/Main/btnVrsteTreninga.png", x=0, y=63*i, width=230, height=63, command=lambda: print("btnVrsteTreninga clicked")),
            "btnTreninzi": lambda i: self.create_button("src/img/Main/btnTreninzi.png", x=0, y=63*i, width=230, height=63, command=lambda: print("btnTreninzi clicked")),
            "btnIzvestaji": lambda i: self.create_button("src/img/Main/btnIzvestaji.png", x=0, y=63*i, width=230, height=63, command=lambda: print("btnIzvestaji clicked")),
            "btnAdmin": lambda i: self.create_button("src/img/Main/btnAdmin.png", x=0, y=63*i, width=230, height=63, command=lambda: print("btnAdmin clicked")),
            "btnClanovi": lambda i: self.create_button("src/img/Main/btnClanovi.png", x=0, y=63*i, width=230, height=63, command=lambda: print("btnClanovi clicked")),
            "btnTermini": lambda i: self.create_button("src/img/Main/btnTermini.png", x=0, y=63*i, width=230, height=63, command=lambda: print("btnTermini clicked")),
            "btnRezervacije": lambda i: self.create_button("src/img/Main/btnRezervacije.png", x=0, y=63*i, width=230, height=63, command=lambda: print("btnRezervacije clicked")),
            "btnProgrami": lambda i: self.create_button("src/img/Main/btnProgrami.png", x=0, y=63*i, width=230, height=63, command=self.napravi_win_programi),
            "btnRegistrujSe": lambda i: self.create_button("src/img/Main/btnRegistrujSe.png", x=35.0, y=559.0, width=160.0, height=35.0, command=lambda: self.registrujSe()),
            "btnOdjaviSe": lambda i: self.create_button("src/img/Main/btnOdjaviSe.png", x=35.0, y=559.0, width=160.0, height=35.0, command=lambda: self.vrati("login"))
        }

        i = 1
        for btn_name in role_buttons.get(self.uloga, []):
            buttons[btn_name](i)
            i += 1
            
    def vrati(self,text):
        self.return_value=text
        self.window.quit()
                
    def vreme(self):
        sad = datetime.datetime.now()
        datum = sad.strftime("%d. %m. %Y")
        vreme = sad.strftime("%H:%M:%S")
        dan = self.zastoNemaSwitch(sad.strftime("%A"))
        self.canvas.itemconfig(self.text_id_date_time, text=f"{vreme} / {dan} / {datum}")
        self.window.after(1000,self.vreme)
        
    def pomeri_rect(self,x,y):
        self.canvas.coords(self.rect, x, y, x+12, y+63)
    
    def nadji_ulogu(self,uloga):
        mapa = {
            -1 : "gost",
            0 : "korisnik",
            1 : "instruktor",
            2 : "admin"
        }
        return mapa.get(uloga,"Ne znam sta je ovo")
    
    def zastoNemaSwitch(self,dan):
        mapa = {
            "Monday" : "Ponedeljak",
            "Tuesday" : "Utorak",
            "Wednesday" : "Sreda",
            "Thursday" : "Četvrtak",
            "Friday" : "Petak",
            "Saturday" : "Subota",
            "Sunday" : "Nedelja"
        }
        return mapa.get(dan,"Nepoznat dan")
    
    def create_button(self, image_path, x, y, width, height, command):
        image = PhotoImage(file=image_path)
        button = Button(
            image=image, borderwidth=0, highlightthickness=0, command=command, relief="flat"
        )
        button.image = image  
        button.place(x=x, y=y, width=width, height=height)
        return button
    
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
    
    def registrujSe(self):
        niz=["signup",self.username]
        self.vrati(niz)

    def unisti_win_programi(self):
        self.programi_window = None

    def napravi_win_programi(self):
        self.programi_window = winProgrami.ProgramiWindow(self.window, self)
        self.programi_window.start()