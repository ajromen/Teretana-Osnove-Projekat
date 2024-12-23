from imports import *
import hashlib
import ctypes
import os
from fpdf import FPDF

SETUP_PATH="src/setup.txt"

def hashPassword(password):
   password_bytes = password.encode('utf-8')
   hash_object = hashlib.sha256(password_bytes)
   return hash_object.hexdigest()

def obavestenje(poruka,title="Greška",sirina=350):
   error_window = ctk.CTkToplevel(fg_color='#000000')
   error_window.title(title)
   error_window.geometry(f"{sirina}x150")
   error_window.resizable(False, False)
   centerWindow(error_window)

   error_label = ctk.CTkLabel(error_window, text=poruka, fg_color="red")
   error_label.pack(pady=20)

   close_button = ctk.CTkButton(error_window, text="Zatvori", command=error_window.destroy)
   close_button.pack(pady=10)

def pitaj(poruka,title="Greška",text1="Da",text2="Ne"):
   error_window = ctk.CTkToplevel(fg_color='#000000')
   error_window.title(title)
   error_window.geometry("350x150")
   error_window.resizable(False, False)
   centerWindow(error_window)

   error_label = ctk.CTkLabel(error_window, text=poruka, fg_color="red")
   error_label.pack(pady=20)

   result = {"value": False}

   button_1 = ctk.CTkButton(error_window, text=text1,fg_color="#252525", command=lambda: (result.update(value=True), error_window.destroy()),width=140)
   button_2 = ctk.CTkButton(error_window, text=text2, command=lambda: (result.update(value=False), error_window.destroy()),width=140)
   button_1.place(x=28,y=108)
   button_2.place(x=181,y=108)

   error_window.wait_window()

   return result["value"]
   
def setup_window(window,title,width_height,bg_color="#000000"):
   ctk.set_appearance_mode("Dark")
   window.title(title)
   window.geometry(width_height)
   window.configure(bg = bg_color)
   window.resizable(False, False)
   centerWindow(window)
   window.iconbitmap("src/img/Logo/TFLogo.ico")
   if os.name == "nt":
      app_id = "mycompany.myapp.subapp"
      ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
        
def centerWindow(window):
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
   window = ctk.CTkToplevel(fg_color='#000000')
   window.title(title)
   window.geometry(str(width)+"x"+str(height))
   window.resizable(False,False)
   centerWindow(window)
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

def sacuvaj_tabelu(podaci,imena_kolona,putanja):
   def sacuvaj_tabelu(podaci, imena_kolona, putanja):
      class PDF(FPDF):
         def header(self):
            self.set_font('Arial', 'B', 12)
            for col_name in imena_kolona:
               self.cell(40, 10, col_name, 1)
            self.ln()

         def table_row(self, row):
            self.set_font('Arial', '', 12)
            for item in row:
               self.cell(40, 10, str(item), 1)
            self.ln()

      pdf = PDF()
      pdf.add_page()

      for row in podaci:
         pdf.table_row(row)

      pdf.output(putanja)

   # Example usage:
   # podaci = [["John", "Doe", 28], ["Jane", "Doe", 25]]
   # imena_kolona = ["First Name", "Last Name", "Age"]
   # putanja = "output.pdf"
   # sacuvaj_tabelu(podaci, imena_kolona, putanja)