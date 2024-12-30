from datetime import timedelta
import bp_programi
from imports import *
import bp_trening

class TreningWindow(winTemplate):
    def __init__(self, window, escfunk=None, uloga=None,username=None, u_prozoru=False):
        super().__init__(window, escfunk, uloga, u_prozoru, username)
        self.dani_dict = {
            "Pon": False,
            "Uto": False,
            "Sre": False,
            "Čet": False,
            "Pet": False,
            "Sub": False,
            "Ned": False,
        }

    def start(self):
        self.create_canvas()  
        
        self.create_exit_button()
        self.create_search_button(self.pretrazi)
        self.create_entry_search(self.pretrazi)
        
        velika=True
        if self.uloga == "admin":
            self.create_button("./src/img/widget/btnDodaj.png", 23, 543, 252, 40, lambda: self.winTrening_Dodaj())
            self.create_button("./src/img/widget/btnIzmeni.png", 300, 543, 252, 40, lambda: self.winTrening_Izmeni())
            self.create_button("./src/img/widget/btnObrisi.png", 577, 543, 252, 40, self.obrisi_trening)
            velika=False
        
        self.kriterijumi=["Šifra", "Sala", "Vreme početka", "Vreme kraja", "Dani nedelje", "Program"]
        self.kriterijumiMap={
            "Šifra" : "id_treninga",
            "Sala" : "naziv_sale",
            "Vreme početka" : "vreme_pocetka",
            "Vreme kraja" : "vreme_kraja",
            "Dani nedelje" : "dani",
            "Program" : "naziv_programa"
        }
        
        self.create_cmbbxSearch(self.kriterijumi)
        self.create_table(self.kriterijumi, velika=velika)

    def popuni_tabelu(self,tabela,kriterijum='id_treninga',pretraga=""):
        for red in tabela.get_children(): tabela.delete(red)
                
        podaci=self.izlistaj(kriterijum,pretraga)
        
        i=0
        for podatak in podaci:
            podatak=list(podatak)
            sifra_sale=podatak[6]
            sifra_programa=podatak[7]
            podatak[1]=str(sifra_sale)+" "+podatak[1]
            podatak[5]=str(sifra_programa)+" "+podatak[5]
            if(podatak[8]==1): 
                if(self.uloga=="admin"): tabela.insert("", "end", values=podatak,tags="obrisano"+str(i%2))
            else: tabela.insert("", "end", values=podatak,tags=str(i%2))
            i+=1

    def pretrazi(self):
        pretraga = self.entrySearch.get().strip().lower()
        kriterijum = self.kriterijumiMap.get(self.cmbbxSearch.get())
        

        for red in self.table.get_children():
            self.table.delete(red)
            
        if pretraga =="" or pretraga=="pretraži":
            pretraga=""
        
        self.popuni_tabelu(self.table,pretraga=pretraga,kriterijum=kriterijum)
        

    def izlistaj(self,kriterijum='id_treninga',pretraga=""):              
        return bp_trening.izlistaj_trening(pretraga,kriterijum)
    
    def obrisi_trening(self):
        slctd_item = self.table.selection()
        if not slctd_item:
            helperFunctions.obavestenje(poruka="Niste odabrali nijedan trening za brisanje.")
            return
        
        slctd_data = self.table.item(slctd_item)
        trening_id = slctd_data["values"][0]  
        obrisan = self.table.item(slctd_item, "tags")

        totalno=False
        for tag in obrisan:
            if "obrisano" in tag:
                totalno=helperFunctions.pitaj("Ako obišete već obrisan trening, on će biti trajno\n obrisan kao i sve što je vezano za njega.\n Da li ste sigurni da želite da nastavite?","Brisanje")

        if not totalno:
            if not helperFunctions.pitaj(title="Potvrda brisanja", poruka="Da li ste sigurni da želite da obiršete odabrani trening?"):
                return
  
        bp_trening.obrisi_trening(trening_id,totalno)

        self.popuni_tabelu(self.table)
        helperFunctions.obavestenje(title="Brisanje", poruka="Trening je uspešno obrisan.")
            
                
    def winTrening_Izmeni(self):
        self.top_level=True
        slctd_item = self.table.selection()
        if not slctd_item:
            helperFunctions.obavestenje(poruka="Niste odabrali nijedan trening za izmenu.",crveno=True)
            return
        
        obrisan = self.table.item(slctd_item, "tags")

        for tag in obrisan:
            if "obrisano" in tag:
                helperFunctions.obavestenje("Ne možete izmeniti obrisan trening.",crveno=True)
                return
        
        self.trenutni_window=helperFunctions.napravi_toplevel(height=390,title="Izmeni trening")
        
        slctd_data = self.table.item(slctd_item)
        slctd_id = slctd_data["values"][0]
        slctd_sala=slctd_data["values"][1]
        slctd_vreme_pocetka=slctd_data["values"][2]
        slctd_vreme_kraja=slctd_data["values"][3]
        slctd_dani=slctd_data["values"][4]
        slctd_program=slctd_data["values"][5]
        
        self.switch_dani(slctd_dani)
        
        # sifra
        self.entrySifra = self.create_entry(141, 30, width=179, height=23, belo=True, placeholder=slctd_id, state="disabled")
        self.cmbbxSala=self.napravi_sql_cmbbx("Sale:",59,75,170,69,"SELECT id_sale, naziv FROM Sala WHERE obrisana IS NOT TRUE",2,True) #Kombo box za naziv
        self.cmbbxProgram=self.napravi_sql_cmbbx("Program:",44,207,170,199,"SELECT id_programa,naziv FROM Program WHERE obrisan IS NOT TRUE",2,True) #Kombo box za naziv
        self.selektuj_vrednost_comboBox(self.cmbbxSala,slctd_sala)
        self.selektuj_vrednost_comboBox(self.cmbbxProgram,slctd_program)
        
        self.zajednicke_Dodaj_Izmeni(slctd_vreme_pocetka,slctd_vreme_kraja,mode=1)
        self.top_level=False

    def winTrening_Dodaj(self):
        self.top_level=True
        self.trenutni_window=helperFunctions.napravi_toplevel(height=390,title="Dodaj trening")
        
        self.cmbbxSala=self.napravi_sql_cmbbx("Sale:",59,75,170,69,"SELECT id_sale, naziv FROM Sala WHERE obrisana IS NOT TRUE",2,True) #Kombo box za naziv
        self.cmbbxProgram=self.napravi_sql_cmbbx("Program:",44,207,170,199,"SELECT id_programa,naziv FROM Program WHERE obrisan IS NOT TRUE",2,True) #Kombo box za naziv
        
        self.entrySifra=self.create_entry(141, 30, width=179, height=23, placeholder="Unesite šifru",auto_fin_fout=(True,"Polje"))
        
        self.zajednicke_Dodaj_Izmeni(mode=0)
        self.top_level=False
        
    def zajednicke_Dodaj_Izmeni(self,vreme_pocetka="00:00",vreme_kraja="00:00",mode=0,dani=""): # 0 za dodaj 1 za izmeni
        self.top_level=True
        self.create_label("Šifra",58,31)
        
        #labele za vreme
        self.create_label("Vreme početka",20,122)
        self.create_label("h   :",204,121)
        self.create_label("min",288,121)
        
        self.create_label("Vreme kraja",33,162)
        self.create_label("h   :",204,161)
        self.create_label("min",288,161)
        
        self.create_label("Dani:",23,243)        
        
        vreme_pocetka=(vreme_pocetka.strip()).split(":")
        pocetak_sati=vreme_pocetka[0]
        pocetak_minuti=vreme_pocetka[1]
        
        vreme_kraja=(vreme_kraja.strip()).split(":")
        kraj_sati=vreme_kraja[0]
        kraj_minuti=vreme_kraja[1]
        
        self.entryPocetakSati=self.create_entry(156,119,width=42,height=23,belo=True,placeholder=pocetak_sati,key_release=lambda *args: self.sredi_sate("pocetak"))
        self.entryPocetakMinuti=self.create_entry(241,119,width=42,height=23,belo=True,placeholder=pocetak_minuti,key_release=lambda *args: self.sredi_sate("pocetak"))
        self.entryKrajSati=self.create_entry(156,160,width=42,height=23,belo=True,placeholder=kraj_sati,key_release=lambda *args: self.sredi_sate("kraj"))
        self.entryKrajMinuti=self.create_entry(242,160,width=42,height=23,belo=True,placeholder=kraj_minuti,key_release=lambda *args: self.sredi_sate("kraj"))
        
        #Kreiranje dugmadi za dane
        self.btnPon=self.button_dani("Pon",self.trenutni_window,16,272)
        self.btnUto=self.button_dani("Uto",self.trenutni_window,61,272)
        self.btnSre=self.button_dani("Sre",self.trenutni_window,106,272)
        self.btnCet=self.button_dani("Čet",self.trenutni_window,151,272)
        self.btnPet=self.button_dani("Pet",self.trenutni_window,196,272)
        self.btnSub=self.button_dani("Sub",self.trenutni_window,241,272)
        self.btnNed=self.button_dani("Ned",self.trenutni_window,286,272)
        
        btnSacuvaj = ctk.CTkButton(self.trenutni_window, text="Sačuvaj", command=lambda: self.dodaj_izmeni(mode=mode))
        btnSacuvaj.place(x=102,y=325)
        #dugme za otkazivanje
        self.create_button("./src/img/widget/btnOtkazi.png",x=136,y=362,width=72,height=17,command=self.trenutni_window.destroy)
        self.top_level=False
        
        
    def sredi_sate(self,vreme: str)-> None:
        id_programa=self.cmbbxProgram.get()
        id_programa,=helperFunctions.ocisti_string(id_programa.split(' ')[0])
        trajanje=bp_programi.get_trajanje(id_programa)
        vreme_pocetka,vreme_kraja=self.proveri_entry_vreme()
        
        if vreme=="pocetak" and vreme_pocetka!=None:
            vreme_pocetka = datetime.datetime.strptime(vreme_pocetka, "%H:%M")
            vreme_kraja = vreme_pocetka + timedelta(minutes=trajanje)
            self.entryKrajSati.delete(0, ctk.END)  
            self.entryKrajSati.insert(0, vreme_kraja.strftime("%H"))
            self.entryKrajMinuti.delete(0, ctk.END)  
            self.entryKrajMinuti.insert(0, vreme_kraja.strftime("%M"))
            
        elif vreme=="kraj"and vreme_kraja!=None:
            vreme_kraja = datetime.datetime.strptime(vreme_kraja, "%H:%M")
            vreme_pocetka = vreme_kraja - timedelta(minutes=trajanje)
            self.entryPocetakSati.delete(0, ctk.END)  
            self.entryPocetakSati.insert(0, vreme_pocetka.strftime("%H"))
            self.entryPocetakMinuti.delete(0, ctk.END)  
            self.entryPocetakMinuti.insert(0, vreme_pocetka.strftime("%M"))
        
    def proveri_entry_vreme(self):
        #provera unosa za vreme
        vreme_pocetak_sat=self.entryPocetakSati.get().zfill(2)
        vreme_pocetak_minuti=self.entryPocetakMinuti.get().zfill(2)
        vreme_kraj_sat=self.entryKrajSati.get().zfill(2)
        vreme_kraj_minuti=self.entryKrajMinuti.get().zfill(2)
        ret_val=(None,None)
        
        if(not vreme_pocetak_sat.isdigit()):
            helperFunctions.obavestenje("Polje vreme pocetak-sati sme sadržati samo cifre.", crveno=True)
            self.restartuj_vreme(self.entryPocetakSati)
            return ret_val
        if(not vreme_pocetak_minuti.isdigit()):
            self.restartuj_vreme(self.entryPocetakMinuti)
            helperFunctions.obavestenje("Polje vreme pocetak-minuti sme sadržati samo cifre.", crveno=True)
            return ret_val
        if(not vreme_kraj_sat.isdigit()):
            self.restartuj_vreme(self.entryKrajSati)
            helperFunctions.obavestenje("Polje vreme kraj-sati sme sadržati samo cifre.", crveno=True)
            return ret_val
        if(not vreme_kraj_minuti.isdigit()):
            self.restartuj_vreme(self.entryKrajMinuti)
            helperFunctions.obavestenje("Polje vreme kraj-minuti sme sadržati samo cifre.", crveno=True)
            return ret_val
        
        #proveravanje da li je uneti broj u opsegu
        if(int(vreme_pocetak_sat)>23):
            self.restartuj_vreme(self.entryPocetakSati)
            helperFunctions.obavestenje("Polje vreme početkak-sati mora biti u opsegu od 0-24.", crveno=True)
            return ret_val
        if(int(vreme_pocetak_minuti)>59):
            self.restartuj_vreme(self.entryPocetakMinuti)
            helperFunctions.obavestenje("Polje vreme početak-minuti mora biti u opsegu od 0-60.", crveno=True)
            return ret_val
        if(int(vreme_kraj_sat)>23):
            self.restartuj_vreme(self.entryKrajSati)
            helperFunctions.obavestenje("Polje vreme kraj-sati mora biti u opsegu od 0-24.", crveno=True)
            return ret_val
        if(int(vreme_kraj_minuti)>59):
            self.restartuj_vreme(self.entryKrajMinuti)
            helperFunctions.obavestenje("Polje vreme kraj-minuti mora biti u opsegu od 0-60.", crveno=True)
            return ret_val
        
        vreme_pocetka=str(vreme_pocetak_sat)+":"+str(vreme_pocetak_minuti)
        vreme_kraja=str(vreme_kraj_sat)+":"+str(vreme_kraj_minuti)
        
        return vreme_pocetka,vreme_kraja
    
    def restartuj_vreme(self,entry,text="00"):
        entry.delete(0,ctk.END)
        entry.insert(0,text)
        
    def dodaj_izmeni(self,mode=0):
        if(mode==1): 
            if(not helperFunctions.pitaj(title="Izmeni program",poruka="Da li ste sigurni da želite da izmenite program?")):return
        id=self.entrySifra.get()
        id_sale=self.cmbbxSala.get()
        #vreme
        
        dani=self.switch_dani_toStr()
        
        id_programa=self.cmbbxProgram.get()
        
        if(id=="" or (not id.isdigit())):
            helperFunctions.obavestenje("Šifra ne sme biti prazna ili sadržati slova.")
            return
        if(id[0]=="0"):
            helperFunctions.obavestenje("Šifra ne sme počinjati sa 0.")
            return
        if(len(id)!=4):
            helperFunctions.obavestenje("Šifra mora imati tačno 4 cifre.")
            return
        if(id_sale==""):
            helperFunctions.obavestenje("Polje sala ne sme biti prazano.")
            return
        if(id_programa==""):
            helperFunctions.obavestenje("Polje program ne sme biti prazano.")
            return
        id_sale=id_sale.split(" ")[0]
        id_programa=id_programa.split(" ")[0]
        
        
        vreme_pocetka,vreme_kraja= self.proveri_entry_vreme()
        if vreme_pocetka==None: return
        
        if(mode):
            if(bp_trening.azuriraj_trening(id, id_sale, vreme_pocetka, vreme_kraja, dani, id_programa)): return
            helperFunctions.obavestenje(title="Izmena programa", poruka="Uspešno izmenjen program.")
        else:
            if(bp_trening.dodaj_trening(id, id_sale, vreme_pocetka, vreme_kraja, dani, id_programa)): return
            helperFunctions.obavestenje(title="Dodaj program", poruka="Uspešno dodat program.")
        
        self.popuni_tabelu(self.table)

        self.entryPocetakSati=None
        self.entryPocetakMinuti=None
        self.entryKrajSati=None
        self.entryKrajMinuti=None
        
        self.trenutni_window.destroy()
        self.trenutni_window=None
            
        
    def button_dani(self,dan,window,x,y):
        aktiviran=self.dani_dict.get(dan,False)
        button = ctk.CTkButton(window, text=dan, corner_radius=5,font=("Inter",12), width=41, height=26)
        if aktiviran: button.configure(fg_color=boje.dugme)
        else: button.configure(fg_color=boje.entry_main)
        button.place(x=x, y=y)
        button.configure(command=lambda: self.switch_dugme(dan, button))
        return button
    
    def switch_dani(self,dani_str):
        self.dani_dict = {
            "Pon": False,
            "Uto": False,
            "Sre": False,
            "Čet": False,
            "Pet": False,
            "Sub": False,
            "Ned": False,
        }
        if(dani_str==""): return
        dani_list=dani_str.split(",")
        for dan in dani_list:
            self.dani_dict[dan]=True
            
    def switch_dani_toStr(self):
        string=""
        for dan in self.dani_dict.items():
            if(dan[1]):string+=dan[0]+","
        string = string[:-1] if string.endswith(",") else string
        return string
        
    def switch_dugme(self,dan,dugme):
        self.dani_dict[dan] = not self.dani_dict[dan]
        if dugme.cget("fg_color")==boje.dugme:
            dugme.configure(fg_color=boje.entry_main)
        else:
            dugme.configure(fg_color=boje.dugme)