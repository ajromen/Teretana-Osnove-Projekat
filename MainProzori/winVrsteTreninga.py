from imports import *
import bp_vrste_treninga

class VrsteTreningaWindow(winTemplate):
    def __init__(self, window, main_window,uloga):
        super().__init__(window,main_window,uloga)

    def start(self):
        self.create_canvas()
        self.create_exit_button()
        self.create_search_button(self.pretrazi)
        
        velika=True
        if(self.uloga=="admin"):
            self.create_button("./src/img/Widget/btnDodaj.png",23,543,252,40,lambda: self.winVrste_dodaj()) # Dodaj Dugme
            self.create_button("./src/img/Widget/btnIzmeni.png",300,543,252,40,lambda: self.winVrste_izmeni()) # Izmeni Dugme
            self.create_button("./src/img/Widget/btnObrisi.png",577,543,252,40,self.obrisi) # Obrisi Dugme
            velika=False
        
        self.kriterijumiMap={
            "Šifra vrste treninga" : "id_vrste_treninga",
            "Naziv" : "naziv" 
        }
        self.kriterijumi=["Šifra vrste treninga", "Naziv"]
        self.create_cmbbxSearch(self.kriterijumi)
        self.create_entry_search(self.pretrazi)
        self.create_table(self.kriterijumi,velika)
        self.table.column("Naziv", width=720)
        

    def popuni_tabelu(self,tabela,kriterijum='id_vrste_treninga',pretraga=""):
        for red in tabela.get_children():
            tabela.delete(red)
                
        podaci=self.izlistaj(kriterijum,pretraga)
        i=0
        for podatak in podaci:
            if(podatak[2]==1): 
                if(self.uloga=="admin"): tabela.insert("", "end", values=podatak,tags="obrisano"+str(i%2))
            else: tabela.insert("", "end", values=podatak,tags=str(i%2))
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
        self.top_level=True
        self.trenutni_window=helperFunctions.napravi_toplevel(height=267,title="Dodaj vrstu treninga")
        
        self.create_label("Šifra vrste treninga:",23,35)
        self.create_label("Naziv:",23,86)
        self.entrySifra=self.create_entry(170,32,width=150,height=23,manual_fin_fon=(True,"Polje"))

        self.txtbxOpis = ctk.CTkTextbox(self.trenutni_window,width=294,height=80,corner_radius=4,fg_color="#080A17")# drugi pput
        self.txtbxOpis.place(x=26,y=112)
        self.txtbxOpis.insert("0.0", "")

        self.create_text_button("Dodaj",88,202,self.napravi,width=166)
        self.create_button("./src/img/Widget/btnOtkazi.png",136,239,72,17,self.trenutni_window.destroy)
        self.top_level=False
        
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
        
        slctd_data = self.table.item(slctd_item)
        id_vrste_treninga = slctd_data["values"][0]
        obrisan = self.table.item(slctd_item, "tags")
        
        totalno=False
        for tag in obrisan:
            if "obrisano" in tag:
                totalno=helperFunctions.pitaj("Ako obišete već obrisanu vrstu treninga, ona će biti trajno\n obrisana kao i sve što je vezano za nju.\n Da li ste sigurni da želite da nastavite?","Brisanje")
        
        if not totalno:
            if not helperFunctions.pitaj(title="Potvrda brisanja", poruka="Da li ste sigurni da želite da obiršete odabranu vrstu treninga?"):
                return

        bp_vrste_treninga.obrisi_vrste_treninga(id_vrste_treninga,totalno)
    
        self.popuni_tabelu(self.table)
        helperFunctions.obavestenje(title="Brisanje", poruka="Vrsta treninga je uspešno obrisana.")
            
    def winVrste_izmeni(self):
        self.top_level=True
        slctd_item = self.table.selection()
        if not slctd_item:
            helperFunctions.obavestenje(poruka="Niste odabrali nijednu vrstu treninga za izmenu.")
            return
        
        obrisan = self.table.item(slctd_item, "tags")

        for tag in obrisan:
            if "obrisano" in tag:
                helperFunctions.obavestenje("Ne možete izmeniti obrisan trening.",crveno=True)
                return

        self.trenutni_window = helperFunctions.napravi_toplevel(height=267, title="Izmeni vrstu treninga")

        slctd_data = self.table.item(slctd_item)
        slctd_id = slctd_data["values"][0]
        slctd_naziv = slctd_data["values"][1]

        self.create_label("Šifra vrste treninga:", 23, 35)
        self.create_label("Naziv:", 23, 86)
        self.entrySifra = self.create_entry(170, 32, width=150, height=23, manual_fin_fon=(True, "Polje"), placeholder=slctd_id, state="disabled")

        self.txtbxOpis = ctk.CTkTextbox(self.trenutni_window, width=294, height=80, corner_radius=4, fg_color="#080A17")
        self.txtbxOpis.place(x=26, y=112)
        self.txtbxOpis.insert("0.0", slctd_naziv)

        self.create_text_button("Sačuvaj", 88, 202, lambda: self.izmeni_vrstu_treninga(slctd_id), width=166)
        self.create_button("./src/img/Widget/btnOtkazi.png", 136, 239, 72, 17, self.trenutni_window.destroy)
        self.top_level=False

    def izmeni_vrstu_treninga(self, id_vrste_treninga):
        naziv = self.txtbxOpis.get("0.0", END).strip()

        if not naziv:
            helperFunctions.obavestenje("Naziv ne sme biti prazan.")
            return

        if bp_vrste_treninga.azuriraj_vrstu_treninga(id_vrste_treninga, naziv):
            return

        helperFunctions.obavestenje(title="Izmena vrste treninga", poruka="Uspešno izmenjena vrsta treninga.")
        self.popuni_tabelu(self.table)
        self.trenutni_window.destroy()