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

def create_entry(canvas, x, y, on_focus_in=None, on_focus_out=None, placeholder='',width=303,height=20,belo=False,state="normal",corner_radius=5,back_color=boje.entry_main,auto_fin_fout=(False,"Polje"),justify="left",key_release=None):
    entry = ctk.CTkEntry(
        canvas,border_width=0,
        fg_color= back_color,
        text_color=boje.bela,
        width=width,height=height,
        corner_radius=corner_radius,
        justify=justify
    )
    entry.place(x=x, y=y,)
    entry.delete(0,END)
    entry.insert(0, placeholder)
    not belo and entry.configure(text_color=boje.text_siva)
    belo and entry.configure(text_color=boje.bela)
    entry.configure(state=state)
    if(auto_fin_fout[0]):
        prikazi='•' if auto_fin_fout[1]=="Lozinka" else ''
        entry.bind("<FocusIn>", lambda event: on_entry_click(entry,placeholder,show=prikazi))
        entry.bind("<FocusOut>", lambda event: on_entry_out(entry,placeholder))
    else:
        entry.bind("<FocusIn>", command=on_focus_in)
        entry.bind("<FocusOut>", command=on_focus_out)
        entry.bind("<Return>",command=on_focus_out)
        
    if key_release is not None:
        entry.bind("<KeyRelease>", key_release)
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

def napravi_sql_cmbbx(canvas,text,labelX,labelY,comboX,comboY,query,broj_kolona=1,specificni=False,font_size=15,variable=None,on_change=None):
    lblSifra = ctk.CTkLabel(canvas, text=text, font=("Inter",font_size * -1),anchor='nw')
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
        tekst = " ".join(str(sifra[i]) for i in range(broj_kolona))
        lista.append(tekst)
    cmbbx=create_comboBox(canvas, values=lista,x=comboX,y=comboY,variable=variable,on_change=on_change)
    return cmbbx

def create_comboBox(canvas,values,x,y,width=148,variable=None,on_change=None):
    combo= ctk.CTkComboBox(
        canvas,
        width=width,height=33,
        corner_radius=5,
        border_width=0,
        values=values,
        fg_color=boje.entry_main,
        dropdown_fg_color=boje.entry_main,
        button_color=boje.entry_svetlija,
        state="readonly",
        variable=variable)
    combo.place(x=x,y=y)
    combo.set(values[0])
    if variable and on_change:
        variable.trace_add("write",lambda *args:on_change_funk(variable,on_change))
    return combo

def on_change_funk(varOnChange,on_change):
    if not varOnChange.get():
        return
    on_change()

def create_entry_search(canvas,pretrazi):
    entrySearch = create_entry(canvas=canvas,x=28,y=59,placeholder="Pretraži",corner_radius=0,auto_fin_fout=(True,"Polje"))
    entrySearch.bind("<Return>", lambda event: pretrazi())
    entrySearch.bind("<KeyRelease>", lambda event: pretrazi())
    return entrySearch

def create_table(canvas,popuni_tabelu,kolone,x=31,y=112,width=787,height=401):
    style = ttk.Style()
    style.theme_use("default")
    
    style.configure("Treeview",
                    background=boje.tabela1,
                    foreground="white",
                    rowheight=25,
                    fieldbackground=boje.entry_main,
                    borderwidth=0)
    style.map('Treeview', background=[('selected', boje.tabela_selected)])
    
    style.configure("Treeview.Heading", background=boje.tabela_heading, foreground="white", relief="flat")
    style.map("Treeview.Heading", background=[('active', boje.tabela_heading_selected)])
        
    table = ttk.Treeview(canvas, columns=kolone, show="headings", height=18)
    #za aktivaciju(zelena)
    table.tag_configure("za_aktivaciju", background=boje.tabela_zeleno, foreground="white")
    #administrator (svetlo plava)
    table.tag_configure("admin", background=boje.tabela_admin, foreground="white")
    #obicno boja
    table.tag_configure("1", background=boje.tabela2, foreground="white")
    table.tag_configure("0", background=boje.tabela1, foreground="white")
    #obrisano boja
    table.tag_configure("obrisano1", background=boje.tabela_crveno_2, foreground="white")
    table.tag_configure("obrisano0", background=boje.tabela_crveno_1, foreground="white")

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
                    background=boje.entry_main,
                    foreground="white",
                    fieldbackground=boje.entry_main,
                    bordercolor=boje.dugme_disabled,
                    borderwidth=0,
                    arrowcolor="white")
    
    style.map('DateEntry', background=[('selected', boje.tabela_heading_selected)])
    
    date_picker = tkcalendar.DateEntry(
        canvas,
        width=15,
        background=boje.entry_main,
        foreground=boje.bela,
        borderwidth=0,
        headersbackground=boje.tabela_heading,
        headersforeground=boje.bela,
        selectbackground=boje.tabela_selected,
        selectforeground=boje.bela,
        normalbackground=boje.bela,
        normalforeground=boje.crna,
        weekendbackground=boje.bela,
        weekendforeground=boje.crna,
        othermonthbackground=boje.entry_tamnija,
        othermonthforeground=boje.text_siva,
        othermonthwebackground=boje.entry_tamnija,
        othermonthweforeground=boje.text_siva,
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