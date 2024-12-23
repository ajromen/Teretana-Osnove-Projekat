from baza_podataka import BazaPodataka
from imports import *
from tkinter import ttk
import tkcalendar

def create_button(canvas,image_path, x, y, width=None, height=None, command=None):
    image = PhotoImage(file=image_path)
    if width is None:
        width = image.width()
    if height is None:  
        height = image.height()
    button = Button(canvas, image=image, borderwidth=0, highlightthickness=0, command=command, relief="flat")
    button.image = image  
    button.place(x=x, y=y, width=width, height=height)
    return button

def create_entry(canvas, x, y, on_focus_in=None, on_focus_out=None, placeholder='',width=303,height=20,belo=False,state="normal",corner_radius=5,back_color="#080A17",manual_fin_fon=(False,"Polje"),justify="left"):
    entry = ctk.CTkEntry(
        canvas,border_width=0,
        fg_color= back_color,
        text_color="#FFFFFF",
        width=width,height=height,
        corner_radius=corner_radius,
        justify=justify
    )
    entry.place(x=x, y=y,)
    entry.delete(0,END)
    entry.insert(0, placeholder)
    not belo and entry.configure(text_color="gray")
    belo and entry.configure(text_color="white")
    entry.configure(state=state)
    if(manual_fin_fon[0]):
        prikazi='•' if manual_fin_fon[1]=="Lozinka" else ''
        entry.bind("<FocusIn>", lambda event: on_entry_click(entry,placeholder,show=prikazi))
        entry.bind("<FocusOut>", lambda event: on_entry_out(entry,placeholder))
    else:
        entry.bind("<FocusIn>", command=on_focus_in)
        entry.bind("<FocusOut>", command=on_focus_out)
        entry.bind("<Return>",command=on_focus_out)
    return entry

def on_entry_click(entry, placeholder, color_active="white",show=''):
    if entry.get() == placeholder:
        entry.delete(0, "end")
        entry.configure(text_color=color_active)
        if placeholder == "Lozinka":
            entry.configure(show=show)

def on_entry_out(entry, placeholder, color_inactive="gray",show=''):
    if entry.get() == "":
        entry.insert(0, placeholder)
        entry.configure(text_color=color_inactive)
        if placeholder == "Lozinka":
            entry.configure(show=show)

def napravi_sql_cmbbx(canvas,text,labelX,labelY,comboX,comboY,query,broj_kolona=1,specificni=False):
    lblSifra = ctk.CTkLabel(canvas, text=text, font=("Inter",15 * -1),anchor='nw')
    lblSifra.place(x=labelX,y=labelY)
    listaSifre=[]
    try:
        cursor=BazaPodataka.get_cursor()
        cursor.execute(query)
        listaSifre=cursor.fetchall()
    except Exception:
        helperFunctions.obavestenje(str(Exception))
        
    lista=[] if specificni else ["SVE"]
    for sifra in listaSifre:
        tekst = " ".join(str(sifra[i]) for i in range(broj_kolona))  # No extra trailing space
        lista.append(tekst)
    cmbbx=create_comboBox(canvas, values=lista,x=comboX,y=comboY)
    return cmbbx

def create_comboBox(canvas,values,x,y,width=148,variable=None):
    combo= ctk.CTkComboBox(
        canvas,
        width=width,height=33,
        corner_radius=5,
        border_width=0,
        values=values,
        fg_color="#080A17",
        dropdown_fg_color="#080A17",
        button_color="#0D1026",
        state="readonly",
        variable=variable)
    combo.place(x=x,y=y)
    combo.set(values[0])
    return combo

def create_entry_search(canvas,pretrazi):
    entrySearch = create_entry(canvas=canvas,x=28,y=59,placeholder="Pretraži",corner_radius=0,manual_fin_fon=(True,"Polje"))
    entrySearch.bind("<Return>", lambda event: pretrazi())
    entrySearch.bind("<KeyRelease>", lambda event: pretrazi())
    return entrySearch

def create_table(canvas,popuni_tabelu,kolone,x=31,y=112,width=787,height=401):
    style = ttk.Style()
    style.theme_use("default")
    
    style.configure("Treeview",
                    background="#121633",
                    foreground="white",
                    rowheight=25,
                    fieldbackground="#080A17",
                    bordercolor="#343638",
                    borderwidth=0)
    style.map('Treeview', background=[('selected', '#3e4cb3')])
    
    style.configure("Treeview.Heading", background="#2d3680", foreground="white", relief="flat")
    style.map("Treeview.Heading", background=[('active', '#3484F0')])
        
    table = ttk.Treeview(canvas, columns=kolone, show="headings", height=18)
    #za aktivaciju(zelena)
    table.tag_configure("za_aktivaciju", background="#19682D", foreground="white")
    #administrator (svetlo plava)
    table.tag_configure("admin", background="#272D5C", foreground="white")
    #obicno boja
    table.tag_configure("1", background="#10142D", foreground="white")
    table.tag_configure("0", background="#121633", foreground="white")
    #obrisano boja
    table.tag_configure("obrisano1", background="#5A1616", foreground="white")
    table.tag_configure("obrisano0", background="#681919", foreground="white")

    for kolona in kolone:
        table.heading(kolona, text=kolona.capitalize())
        table.column(kolona, anchor="center", width=80)

    popuni_tabelu(table)
    
    if len(table.get_children())!=0:
        #menjanje sirina kolona
        max_sirina = 200 
        for kolona in table["columns"]:
            max_sirina_kolone = len(table.heading(kolona, "text"))+2
            
            for item in table.get_children():
                deo_text = str(table.item(item, "values")[table["columns"].index(kolona)])
                finalna_sirina = max(max_sirina_kolone, len(deo_text))
            
            table.column(kolona, width=min(finalna_sirina * 8 , max_sirina))

    table.place(x=x, y=y, width=width, height=height)
    return table

def selektuj_vrednost_comboBox(komboBox, kriterijum):
    vrednosti = komboBox.cget('values')
    for vrednost in vrednosti:
        if kriterijum.strip() in vrednost.strip():
            komboBox.set(vrednost)
            return
    
def create_label(window,text,x,y,font_size=15):
    labela = ctk.CTkLabel(window, text=text, font=("Inter",font_size * -1),anchor='nw')
    labela.place(x=x,y=y)
    return labela

def create_canvas_image(canvas,image_path,x,y):
    image=PhotoImage(file=image_path)
    canvas.create_image(x, y, image=image,anchor='nw')
    return image

def create_date_picker(canvas, x, y, variable):
    style = ttk.Style()
    style.theme_use("default")
    
    style.configure("DateEntry",
                    background="#080A17",
                    foreground="white",
                    fieldbackground="#080A17",
                    bordercolor="#343638",
                    borderwidth=0,
                    arrowcolor="white")
    
    style.map('DateEntry', background=[('selected', '#3e4cb3')])
    
    date_picker = tkcalendar.DateEntry(
        canvas,
        width=15,
        background='#080A17',
        foreground='#FFFFFF',
        borderwidth=0,
        headersbackground='#2d3680',
        headersforeground='#FFFFFF',
        selectbackground='#3e4cb3',
        selectforeground='#FFFFFF',
        normalbackground='#FFFFFF',
        normalforeground='#000000',
        weekendbackground='#FFFFFF',
        weekendforeground='#000000',
        othermonthbackground='#04050B',
        othermonthforeground='#A19E9E',
        othermonthwebackground='#04050B',
        othermonthweforeground='#A19E9E',
        showweeknumbers=False,
        style="DateEntry",
        date_pattern="yyyy-mm-dd",
        locale="sr_RS"
    )
    date_picker.place(x=x, y=y)
    return date_picker

# ne radi posle nagradjivanja jer odmah postaje premium
# popraviti tako sto ostavis da nije nagradjen js al mu je promenjn datum i ako se naidje na nekome kome je datum danas 
# da mu se dodeli koji treba da dobije