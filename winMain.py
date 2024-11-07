from tkinter import *
import customtkinter as ctk
import helperFunctions
import queries
import os
import ctypes

class MainWindow:
    def __init__(self,window):
         self.window=window
         
    def start(self,user,uloga):
        self.user=user
        self.uloga=uloga
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
        
        #self.imgLogo = PhotoImage(file="src/img/Main/imgPozadina.png")
        #self.canvas.create_image(455, 175, image=self.imgLogo)
        
        self.imgUser = PhotoImage(file="src/img/Main/imgUser.png")
        self.canvas.create_image(115, 31, image=self.imgUser)

        self.text_id_user = self.canvas.create_text(64,25, anchor="nw", text=self.user, fill="#FFFFFF", font=("Inter Medium", 12 * -1))
        self.text_id_date_time = self.canvas.create_text(540,313, anchor="nw", text="19:49 / Saturday /  01.11.2024", fill="#DFDFDF", font=("Inter", 24 * -1))
        #self.text_id = self.canvas.create_text(540,313, anchor="nw", text="19:49 / Saturday /  01.11.2024", fill="#DFDFDF", font=("Inter", 24 * -1))
        self.canvas.create_rectangle(218.0, 0, 230.0, 62, fill="#FFFFFF",outline="")
            
        
    def create_widgets(self):
        self.btnVrsteTreninga = self.create_button( "src/img/Main/btnVrsteTreninga.png", x=0, y=501, width=320, height=63, command=lambda: print("btnVrsteTreninga clicked"))
        self.btnTreninzi = self.create_button("src/img/Main/btnTreninzi.png", x=0, y=501, width=320, height=63, command=lambda: print("btnVrsteTreninga clicked"))
        self.btnIzvestaji = self.create_button("src/img/Main/btnIzvestaji.png", x=0, y=501, width=320, height=63, command=lambda: print("btnVrsteTreninga clicked"))
        self.btnAdmin = self.create_button("src/img/Main/btnAdmin.png", x=0, y=501, width=320, height=63, command=lambda: print("btnVrsteTreninga clicked"))
        self.btnClanovi = self.create_button("src/img/Main/btnClanovi.png", x=0, y=501, width=320, height=63, command=lambda: print("btnVrsteTreninga clicked"))
        self.btnTermini = self.create_button("src/img/Main/btnTermini.png", x=0, y=501, width=320, height=63, command=lambda: print("btnVrsteTreninga clicked"))
        self.btnRezervacije = self.create_button("src/img/Main/btnRezervacije.png", x=0, y=501, width=320, height=63, command=lambda: print("btnVrsteTreninga clicked"))
        self.btnProgrami = self.create_button("src/img/Main/btnProgrami.png", x=0, y=501, width=320, height=63, command=lambda: print("btnVrsteTreninga clicked"))
        
        self.btnRegistrujSe = self.create_button("src/img/Main/btnRegistrujSe.png", x=0, y=501, width=320, height=63, command=lambda: print("btnVrsteTreninga clicked"))
        self.btnOdjaviSe = self.create_button("src/img/Main/btnOdjaviSe.png", x=0, y=501, width=320, height=63, command=lambda: print("btnVrsteTreninga clicked"))
    
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