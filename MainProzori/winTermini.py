from imports import *
import bp_termini

class TerminiWindow:
    def __init__(self, window, main_window, uloga):
        self.window = window
        self.main_window = main_window
        self.current_canvas = None
        self.uloga = uloga

    def start(self):
        self.current_canvas = Canvas(self.window, bg="#010204", height=618, width=860, bd=0, highlightthickness=0, relief="ridge")
        self.current_canvas.place(x=230, y=0)

        wid.create_button(self.current_canvas, "./src/img/Widget/btnExit.png", 812, 9, 33, 33, lambda: self.main_window.unisti_trenutni_win())  # Exit button
        wid.create_button(self.current_canvas, "./src/img/Widget/btnSearch.png", 358, 53, 33, 33, self.pretrazi)  # Search button
        wid.create_button(self.current_canvas, "./src/img/Widget/btnDodaj.png", 23, 543, 252, 40, lambda: self.winTermini_Dodaj())  # Add button
        wid.create_button(self.current_canvas, "./src/img/Widget/btnIzmeni.png", 300, 543, 252, 40, lambda: self.winTermini_Izmeni())  # Edit button
        wid.create_button(self.current_canvas, "./src/img/Widget/btnObrisi.png", 577, 543, 252, 40, self.obrisi_termin)  # Delete button

        self.imgsearchPozadiga = wid.create_canvas_image(self.current_canvas, "./src/img/Widget/searchPozadina.png", 23, 53)
        self.tabelaPozadina = wid.create_canvas_image(self.current_canvas, "./src/img/Widget/tabelaPozadina.png", 23, 102)

        self.kriterijumi = ["Šifra", "Datum održavanja", "Trening", "Obrisan"]
        self.entrySearch = wid.create_entry_search(self.current_canvas, self.pretrazi)

        self.current_canvas.create_text(610, 65, anchor="nw", text="Pretraži po:", fill="#FFFFFF", font=("Inter", 12 * -1))
        self.cmbbxSearch = wid.create_comboBox(self.current_canvas, self.kriterijumi, x=681, y=53)

        self.table = wid.create_table(self.current_canvas, self.popuni_tabelu, tuple(self.kriterijumi))

    def popuni_tabelu(self, tabela, kriterijum='id_termina', pretraga=""):
        for red in tabela.get_children():
            tabela.delete(red)

        podaci = self.izlistaj(kriterijum, pretraga)
        i = 0
        for podatak in podaci:
            if podatak[3] == 1:
                if self.uloga == "admin":
                    tabela.insert("", "end", values=podatak, tags="obrisano" + str(i % 2))
            else:
                tabela.insert("", "end", values=podatak, tags=str(i % 2))
            i += 1

    def pretrazi(self):
        pretraga = self.entrySearch.get().strip().lower()
        kriterijum = self.kriterijumiMap.get(self.cmbbxSearch.get())
        if not kriterijum:
            helperFunctions.obavestenje("Prvo izaberite kriterijum pretrage.")
            return

        for red in self.table.get_children():
            self.table.delete(red)

        if pretraga == "" or pretraga == "pretraži":
            pretraga = ""

        self.popuni_tabelu(self.table, pretraga=pretraga, kriterijum=kriterijum)

    def izlistaj(self, kriterijum='id_termina', pretraga=""):
        return bp_termini.izlistaj_termini(pretraga, kriterijum)

    def obrisi_termin(self):
        slctd_item = self.table.selection()
        if not slctd_item:
            helperFunctions.obavestenje(poruka="Niste odabrali nijedan termin za brisanje.")
            return

        pitaj = helperFunctions.pitaj(title="Potvrda brisanja", poruka="Da li ste sigurni da želite da obiršete odabrani termin?")
        if not pitaj:
            return

        slctd_data = self.table.item(slctd_item)
        termin_id = slctd_data["values"][0]

        bp_termini.obrisi_termin(termin_id)

        self.table.delete(slctd_item)
        helperFunctions.obavestenje(title="Brisanje", poruka="Termin je uspešno obrisan.")

    def winTermini_Dodaj(self):
        self.trenutni_window = helperFunctions.napravi_toplevel(height=390, title="Dodaj termin")
        # Add widgets for adding a new termin
        # ...

    def winTermini_Izmeni(self):
        slctd_item = self.table.selection()
        if not slctd_item:
            helperFunctions.obavestenje(poruka="Niste odabrali nijedan termin za izmenu.")
            return

        self.trenutni_window = helperFunctions.napravi_toplevel(height=390, title="Izmeni termin")
        # Add widgets for editing a selected termin
