from imports import *
import widgets as wid
import winIzvestaji
import winProgrami
import winTermini
import winTrening
import winVrsteTreninga
import winClanovi
import winAdmin
import winRezervacije

class MainWindow:
    def __init__(self,window):
         self.window=window
         self.trenutni_window = None
         
    def start(self,username,uloga):
        self.username=username
        self.uloga=self.nadji_ulogu(uloga)
        self.return_value = 0
        helperFunctions.setup_window(self.window,"TopForm","1080x603","#04050C")
        self.create_canvas()
        self.create_widgets()
        self.window.mainloop()
        return self.return_value

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
        
        self.imgPozadina = wid.create_canvas_image(self.canvas,"src/img/Main/imgPozadina2.png",230, 0)
        self.imgLogo = wid.create_canvas_image(self.canvas,"src/img/Logo/TopFormLogoBeliSrednji.png",445, 190)#465142
        self.imgUser = wid.create_canvas_image(self.canvas,"src/img/Main/imgUser.png",0, 0)

        self.text_id_user = self.canvas.create_text(64,25, anchor="nw", text=self.username, fill="#FFFFFF", font=("Inter Medium", 12 * -1))
        self.text_id_date_time = self.canvas.create_text(475,313, anchor="nw", text="19:49 / Saturday /  01.11.2024", fill="#DFDFDF", font=("Inter", 24 * -1))
        self.rect=self.canvas.create_rectangle(218.0, 0, 230.0, 63, fill="#FFFFFF",outline="", tags="rect")
        

    def create_widgets(self):
        self.napravi_dugmad_po_ulozi()
    
        self.vreme()
    
    def napravi_dugmad_po_ulozi(self):
        self.dugmad_pozicije = {} 

        imena_dugmadi_po_ulozi = {
            "gost": ["btnProgrami", "btnTermini", "btnRezervacije", "btnRegistrujSe"],
            "admin": ["btnVrsteTreninga", "btnTreninzi", "btnProgrami", "btnClanovi", "btnTermini", "btnIzvestaji", "btnAdmin", "btnOdjaviSe"],
            "instruktor": ["btnRezervacije", "btnClanovi", "btnOdjaviSe"],
            "korisnik": ["btnProgrami", "btnTermini", "btnRezervacije", "btnOdjaviSe"]
        }

        dugmad = {
            "btnVrsteTreninga": lambda i: self.create_button("src/img/Main/btnVrsteTreninga.png", x=0, y=63*i, width=230, height=63, command=lambda: self.prebaci_win("vrste_treninga")),
            "btnTreninzi": lambda i: self.create_button("src/img/Main/btnTreninzi.png", x=0, y=63*i, width=230, height=63, command=lambda: self.prebaci_win("trening")),
            "btnIzvestaji": lambda i: self.create_button("src/img/Main/btnIzvestaji.png", x=0, y=63*i, width=230, height=63, command=lambda: self.prebaci_win("izvestaji")),
            "btnAdmin": lambda i: self.create_button("src/img/Main/btnAdmin.png", x=0, y=63*i, width=230, height=63, command=lambda: self.prebaci_win("admin")),
            "btnClanovi": lambda i: self.create_button("src/img/Main/btnClanovi.png", x=0, y=63*i, width=230, height=63, command=lambda: self.prebaci_win("clanovi")),
            "btnTermini": lambda i: self.create_button("src/img/Main/btnTermini.png", x=0, y=63*i, width=230, height=63, command=lambda: self.prebaci_win("termini")),
            "btnRezervacije": lambda i: self.create_button("src/img/Main/btnRezervacije.png", x=0, y=63*i, width=230, height=63, command=lambda: self.prebaci_win("rezervacije")),
            "btnProgrami": lambda i: self.create_button("src/img/Main/btnProgrami.png", x=0, y=63*i, width=230, height=63, command=lambda: self.prebaci_win("programi")),
            "btnRegistrujSe": lambda i: self.create_button("src/img/Main/btnRegistrujSe.png", x=35.0, y=559.0, width=160.0, height=35.0, command=lambda: self.registrujSe()),
            "btnOdjaviSe": lambda i: self.create_button("src/img/Main/btnOdjaviSe.png", x=35.0, y=559.0, width=160.0, height=35.0, command=lambda: self.vrati("login"))
        }

        i = 1
        for btn_ime in imena_dugmadi_po_ulozi.get(self.uloga, []):
            y_position = 63 * i if "RegistrujSe" not in btn_ime and "OdjaviSe" not in btn_ime else 559.0
            self.dugmad_pozicije[btn_ime] = y_position 
            dugmad[btn_ime](i) 
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
    
    def registrujSe(self):
        niz=["signup",self.username]
        self.vrati(niz)

    def unisti_trenutni_win(self):
        if self.trenutni_window is not None:
            self.trenutni_window.current_canvas.destroy()  
            self.trenutni_window = None

    def napravi_win_programi(self):
        self.trenutni_window = winProgrami.ProgramiWindow(self.window, self.unisti_trenutni_win,self.uloga)
        self.trenutni_window.start()
        
    def napravi_win_trening(self):
        self.trenutni_window = winTrening.TreningWindow(self.window, self.unisti_trenutni_win,self.uloga)
        self.trenutni_window.start()
        
    def napravi_win_clanovi(self):
        self.trenutni_window = winClanovi.ClanoviWindow(self.window, self.unisti_trenutni_win,self.uloga)
        self.trenutni_window.start()
        
    def napravi_win_admin(self):
        self.trenutni_window = winAdmin.AdminWindow(self.window, self.unisti_trenutni_win,self.uloga)
        self.trenutni_window.start()

    def napravi_win_vrste_treninga(self):
        self.trenutni_window= winVrsteTreninga.VrsteTreningaWindow(self.window,self.unisti_trenutni_win,self.uloga)
        self.trenutni_window.start()
    
    def napravi_win_termini(self):
        self.trenutni_window = winTermini.TerminiWindow(self.window, lambda: self.unisti_trenutni_win(), self.uloga)
        self.trenutni_window.start()
        
    def napravi_win_izvestaji(self):
        self.trenutni_window = winIzvestaji.IzvestajiWindow(self.window, self.unisti_trenutni_win, self.uloga)
        self.trenutni_window.start()

    def napravi_win_rezervacije(self):
        self.trenutni_window = winRezervacije.winRezervacije(self.window, self.unisti_trenutni_win, self.uloga,self.username)
        self.trenutni_window.start()

    def prebaci_win(self, win):
        self.unisti_trenutni_win()
        if win == "programi": self.napravi_win_programi()
        elif win == "trening": self.napravi_win_trening()
        elif win == "clanovi": self.napravi_win_clanovi()
        elif win == "admin": self.napravi_win_admin()
        elif win == "vrste_treninga": self.napravi_win_vrste_treninga()
        elif win == "termini": self.napravi_win_termini()
        elif win == "izvestaji": self.napravi_win_izvestaji()
        elif win == "rezervacije": self.napravi_win_rezervacije()