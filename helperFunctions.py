import hashlib
import customtkinter as ctk

def hashPassword(password):
   password_bytes = password.encode('utf-8')
   hash_object = hashlib.sha256(password_bytes)
   return hash_object.hexdigest()

def pisi_eror(poruka):
        error_window = ctk.CTkToplevel()
        error_window.title("Greška")

        error_window.update_idletasks()
        screen_width = error_window.winfo_screenwidth()
        screen_height = error_window.winfo_screenheight()
        window_width = 350
        window_height = 150
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        error_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        error_window.focus()
        error_window.grab_set()

        error_label = ctk.CTkLabel(error_window, text=poruka, fg_color="red")
        error_label.pack(pady=20)

        close_button = ctk.CTkButton(error_window, text="Zatvori", command=error_window.destroy)
        close_button.pack(pady=10)
        
def centerWindow(window):
   window.update_idletasks()
   screen_width = window.winfo_screenwidth()
   screen_height = window.winfo_screenheight()
   window_width = window.winfo_width()
   window_height = window.winfo_height()
   x = (screen_width // 2) - (window_width)*2
   y = (screen_height // 2) - (window_height)*1.2
   window.geometry(f"{window_width}x{window_height}+{x}+{y}")
   window.focus()
   window.grab_set()