import baza_podataka
import bp_vrste_treninga
from imports import *

class VrsteTreningaWindow:
    def __init__(self, window, main_window):
        self.window = window
        self.main_window=main_window
        self.current_canvas = None

    def start(self):
        self.current_canvas = Canvas(self.window, bg="#010204", height=618, width=860, bd=0, highlightthickness=0, relief="ridge")
        self.current_canvas.place(x=230, y=0)        
        
        wid.create_button(self.current_canvas,"./src/img/Widget/btnExit.png",812,9,33,33,lambda: self.main_window.unisti_trenutni_win())# EXit dugme
        wid.create_button(self.current_canvas,"./src/img/Widget/btnSearch.png",358,53,33,33,self.pretrazi) # Search dugme
        wid.create_button(self.current_canvas,"./src/img/Widget/btnDodaj.png",23,543,252,40,lambda: self.winVrste_dodaj()) # Dodaj Dugme
        wid.create_button(self.current_canvas,"./src/img/Widget/btnIzmeni.png",300,543,252,40,lambda: print("izmeni")) # Izmeni Dugme
        wid.create_button(self.current_canvas,"./src/img/Widget/btnObrisi.png",577,543,252,40,self.obrisi) # Obrisi Dugme
        
        self.imgsearchPozadiga = wid.create_canvas_image(self.current_canvas,"./src/img/Widget/searchPozadina.png",23,53)
        self.tabelaPozadina = wid.create_canvas_image(self.current_canvas,"./src/img/Widget/tabelaPozadina.png",23,102)
        
        self.kriterijumiMap={
            "Šifra vrste treninga" : "id_vrste_treninga",
            "Naziv" : "naziv" 
        }
        self.kriterijumi=["Šifra vrste treninga", "Naziv"]
        self.entrySearch=wid.create_entry_search(self.current_canvas,self.pretrazi)
        
        self.current_canvas.create_text(610,65, anchor="nw", text="Pretraži po:", fill="#FFFFFF", font=("Inter", 12 * -1))
        self.cmbbxSearch=wid.create_comboBox(self.current_canvas,self.kriterijumi,x=681,y=53)
        
        self.table=wid.create_table(self.current_canvas,self.popuni_tabelu,tuple(self.kriterijumi))
        self.table.column("Naziv", width=720)
        

    def popuni_tabelu(self,tabela,kriterijum='id_vrste_treninga',pretraga=""):
        for red in tabela.get_children():
            tabela.delete(red)
                
        podaci=self.izlistaj(kriterijum,pretraga)
        i=0
        for podatak in podaci:
            tabela.insert("", "end", values=podatak,tags=str(i%2))
            i+=1

    def pretrazi(self):
        pretraga = self.entrySearch.get().strip().lower()
        kriterijum = self.kriterijumiMap.get(self.cmbbxSearch.get())
        if(not kriterijum):
            helperFunctions.obavestenje("Prvo izaberite kriterijum pretrage.")
            return

        for red in self.table.get_children():
            self.table.delete(red)
            
        pretraga=pretraga.lower()
            
        if pretraga =="" or pretraga=="pretraži":
            pretraga=""

        self.popuni_tabelu(self.table,pretraga=pretraga,kriterijum=kriterijum)

    def izlistaj(self,kriterijum='id_vrste_treninga',pretraga=""):              
        return bp_vrste_treninga.izlistaj_vrste_treninga(pretraga,kriterijum)
    
    def winVrste_dodaj(self):
        self.trenutni_window=helperFunctions.napravi_toplevel(height=267,title="Dodaj vrstu treninga")
        
        wid.create_label(self.trenutni_window,"Šifra vrste treninga:",23,35)
        wid.create_label(self.trenutni_window,"Naziv:",23,86)
        self.entrySifra=wid.create_entry(self.trenutni_window,170,32,width=164,height=23,manual_fin_fon=(True,"Polje"))

        self.txtbxOpis = ctk.CTkTextbox(self.trenutni_window,width=294,height=80,corner_radius=4,fg_color="#080A17")
        self.txtbxOpis.place(x=26,y=112)
        self.txtbxOpis.insert("0.0", "")

        btnSacuvaj = ctk.CTkButton(self.trenutni_window,width=166,height=27,text_color="#FFFFFF", text="Dodaj",font=("Inter", 15),command=self.napravi)
        btnSacuvaj.place(x=88,y=202)
        wid.create_button(self.trenutni_window,"./src/img/Widget/btnOtkazi.png",x=136,y=239,width=72,height=17,command=self.trenutni_window.destroy)

        
    def napravi(self):
        sifra=self.entrySifra.get().strip()
        naziv=self.txtbxOpis.get("0.0", END)

        if(not sifra.isdigit()):
            helperFunctions.obavestenje("Šifra vrste treninga mora biti broj")
            return 
        
        if(bp_vrste_treninga.dodaj_vrstu_treninga(sifra,naziv)):return
        helperFunctions.obavestenje(title="Dodaj program", poruka="Uspešno dodat program.")
        self.txtbxOpis=None
        
        self.popuni_tabelu(self.table)
        self.trenutni_window.destroy()
        
    def obrisi(self):
        slctd_item = self.table.selection()
        if not slctd_item:
            helperFunctions.obavestenje(poruka="Niste odabrali nijednu vrstu treninga.")
            return
        
        pitaj = helperFunctions.pitaj(title="Potvrda brisanja", poruka="Da li ste sigurni da želite da obiršete odabranu vrstu treninga?")
        if not pitaj:
            return

        slctd_data = self.table.item(slctd_item)
        id_vrste_treninga = slctd_data["values"][0]

        komanda = "DELETE FROM Vrste_treninga WHERE id_vrste_treninga = ?"
        baza_podataka.cursor.execute(komanda, (id_vrste_treninga,))
        baza_podataka.connection.commit()

        self.table.delete(slctd_item)
        helperFunctions.obavestenje(title="Brisanje", poruka="Vrsta treninga je uspešno obrisana.")
            
        