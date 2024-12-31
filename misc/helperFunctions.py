from imports import *
import hashlib
import ctypes
import os

SETUP_PATH="src/setup.txt"

def hashPassword(password):
   password_bytes = password.encode('utf-8')
   hash_object = hashlib.sha256(password_bytes)
   return hash_object.hexdigest()
 
def obavestenje(poruka,title="Greška",sirina=350,crveno=False):
   error_window = ctk.CTkToplevel(fg_color=boje.crna)
   error_window.title(title)
   error_window.geometry(f"{sirina}x150")
   error_window.resizable(False, False)
   centriraj_window(error_window)
   fg_color='red' if crveno else 'black'
   error_label = ctk.CTkLabel(error_window, text=poruka, fg_color=fg_color)
   error_label.pack(pady=20)

   close_button = ctk.CTkButton(error_window, text="Zatvori", command=error_window.destroy)
   close_button.pack(pady=10)

def pitaj(poruka,title="Greška",text1="Da",text2="Ne",crveno=True):
   error_window = ctk.CTkToplevel(fg_color=boje.crna)
   error_window.title(title)
   error_window.geometry("350x150")
   error_window.resizable(False, False)
   centriraj_window(error_window)
   fg_color='red' if crveno else 'black'

   error_label = ctk.CTkLabel(error_window, text=poruka, fg_color=fg_color)
   error_label.pack(pady=20)

   result = {"value": False}

   button_1 = ctk.CTkButton(error_window, text=text1,fg_color=boje.dugme_disabled, command=lambda: (result.update(value=True), error_window.destroy()),width=140)
   button_2 = ctk.CTkButton(error_window, text=text2, command=lambda: (result.update(value=False), error_window.destroy()),width=140)
   button_1.place(x=28,y=108)
   button_2.place(x=181,y=108)

   error_window.wait_window()
   return result["value"]
   
def setup_window(window,title,width_height,bg_color=boje.crna):
   ctk.set_appearance_mode("Dark")
   window.title(title)
   window.geometry(width_height)
   window.configure(bg = bg_color)
   window.resizable(False, False)
   centriraj_window(window)
   window.iconbitmap("src/img/logo/TFLogo.ico")
   if os.name == "nt":
      app_id = "mycompany.myapp.subapp"
      ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
        
def centriraj_window(window):
   window.update_idletasks()
   screen_width = window.winfo_screenwidth()
   screen_height = window.winfo_screenheight()
   window_width = window.winfo_width()
   window_height = window.winfo_height()
   x = (screen_width // 2) - (window_width//2)
   y = (screen_height // 2) - (window_height//2)
   window.geometry(f"{window_width}x{window_height}+{x}+{y}")
   window.focus()
   window.grab_set()

def napravi_toplevel(width=343,height=485,title=""):
   window = ctk.CTkToplevel(fg_color=boje.crna)
   window.title(title)
   window.geometry(str(width)+"x"+str(height))
   window.resizable(False,False)
   centriraj_window(window)
   return window

def ucitaj_iz_setup(text):
   if os.path.exists(SETUP_PATH):
      with open(SETUP_PATH,'r',encoding='utf-8') as file:
         for line in file.readlines():
            if line.strip() and line.strip().split(": ")[0]==text:
               return line.strip().split(": ")[1]
   else:
      obavestenje(f"Nije pronađen setup.txt na lokaciji: {os.getcwd().replace("\\","/")}/{SETUP_PATH}", sirina=1000)
      
def azuriraj_setup(kljuc, nova_vrednost):
   if os.path.exists(SETUP_PATH):
      with open(SETUP_PATH, 'r', encoding='utf-8') as file:
         lines = file.readlines()

      postoji = False
      updated_lines = []

      for line in lines:
         if line.strip() and line.strip().split(": ")[0] == kljuc:
            updated_lines.append(f"{kljuc}: {nova_vrednost}\n")
            postoji = True
         else:
            updated_lines.append(line)

      if not postoji:
         updated_lines.append(f"{kljuc}: {nova_vrednost}\n")

      with open(SETUP_PATH, 'w', encoding='utf-8') as file:
         file.writelines(updated_lines)
   else:
      obavestenje(f"Nije pronađen setup.txt na lokaciji: {os.getcwd().replace('\\', '/')}/{SETUP_PATH}", sirina=1000)
      
def ocisti_string(*args):
   return tuple(str(arg).strip() for arg in args)

def eng_dani_u_srp(dan):
   dani_map = {
      "Monday": "Ponedeljak",
      "Tuesday": "Utorak",
      "Wednesday": "Sreda",
      "Thursday": "Četvrtak",
      "Friday": "Petak",
      "Saturday": "Subota",
      "Sunday": "Nedelja"
   }
   return dani_map.get(dan, "Nepoznat dan")

def broj_u_dan(dan):
   dani_map = {
      0: "Ponedeljak",
      1: "Utorak",
      2: "Sreda",
      3: "Četvrtak",
      4: "Petak",
      5: "Subota",
      6: "Nedelja"
   }
   return dani_map.get(dan, "Nepoznat dan")

def dan_u_broj(dan):
   dani_map = {
      "Ponedeljak": 0,
      "Utorak": 1,
      "Sreda": 2,
      "Četvrtak": 3,
      "Petak": 4,
      "Subota": 5,
      "Nedelja": 6
   }
   return dani_map.get(dan, -1)

def dan_in_broj(dan):
   dani_map = {
      "Ponedeljak": 1,
      "Utorak": 2,
      "Sreda": 3,
      "Četvrtak": 4,
      "Petak": 5,
      "Subota": 6,
      "Nedelja": 7
   }
   for key, value in dani_map:
      if dan in key:
         return value
 
def sacuvaj_tabelu(podaci, imena_kolona, putanja):
   with open(putanja,'w',encoding='utf-8') as file:
      max=0
      for ime in imena_kolona:
         if len(ime)>max: max=len(ime)
      
      for podatak in podaci:
         for item in podatak:
            if len(str(item))>max: max=len(str(item))
            
      max+=2
      file.write("|")
      for ime in imena_kolona:
         file.write(ime.center(max)+"|")
      
      broj_linija=(max+1)*len(imena_kolona)+1
      
      file.write("\n"+"—"*broj_linija+"\n")
      
      for podatak in podaci:
         file.write("|")
         for item in podatak:
            file.write(str(item).center(max)+"|")
         file.write("\n")
         
      file.write("—"*broj_linija+"\n")
   
   obavestenje(f"Podaci su uspešno sačuvani u fajl: {putanja}",title="Uspešno čuvanje")
      
def dopisi_u_fajl(putanja, tekst):
   with open(putanja, 'a', encoding='utf-8') as file:
      file.write('\n'+ tekst + '\n')
      
def onemoguci_dugme(dugme):
   dugme.configure(command="disabled")
   dugme.configure(fg_color=boje.dugme_disabled)
   dugme.configure(hover_color=boje.dugme_disabled_hover)
   
def omoguci_dugme(dugme, komanda):
   dugme.configure(command=komanda)
   dugme.configure(fg_color=boje.dugme)
   dugme.configure(hover_color=boje.dugme_hover)