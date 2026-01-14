import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk

def inicijalizacija_imenika():
    konekcija = sqlite3.connect('Imenik.db')
    kursor = konekcija.cursor()

    sql_naredba = '''
    CREATE TABLE IF NOT EXISTS Imenik (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ime TEXT NOT NULL,
        prezime TEXT NOT NULL,
        broj_telefona TEXT NOT NULL
    );
    '''
    kursor.execute(sql_naredba)
    konekcija.commit()
    konekcija.close()

inicijalizacija_imenika()

def dodaj_kontakt():
    unos_ime = simpledialog.askstring("Dodaj Kontakt", "Unesite ime:")
    unos_prezime = simpledialog.askstring("Dodaj Kontakt", "Unesite prezime:")
    unos_broj_telefona = simpledialog.askstring("Dodaj Kontakt", "Unesite broj telefona:")

    if unos_ime and unos_prezime and unos_broj_telefona:
        konekcija = sqlite3.connect('Imenik.db')
        kursor = konekcija.cursor()

        sql_naredba = '''
        INSERT INTO Imenik (ime, prezime, broj_telefona)
        VALUES (?, ?, ?);
        '''
        podaci = (unos_ime, unos_prezime, unos_broj_telefona)

        kursor.execute(sql_naredba, podaci)
        konekcija.commit()
        konekcija.close()
        messagebox.showinfo("Uspjeh", "Kontakt je uspješno dodan.")
    else:
        messagebox.showwarning("Greška", "Sva polja moraju biti popunjena.")

def prikazi_kontakte():
    konekcija = sqlite3.connect('Imenik.db')
    kursor = konekcija.cursor()

    kursor.execute("SELECT * FROM Imenik;")
    rezultati = kursor.fetchall()
    konekcija.close()

    prikaz_window = tk.Toplevel()
    prikaz_window.title("Kontakti")

    tree = ttk.Treeview(prikaz_window, columns=("ID", "Ime", "Prezime", "Broj Telefona"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Ime", text="Ime")
    tree.heading("Prezime", text="Prezime")
    tree.heading("Broj Telefona", text="Broj Telefona")

    for red in rezultati:
        tree.insert("", tk.END, values=red)
    tree.pack(fill=tk.BOTH, expand=True)
    prikaz_window.mainloop()

def izbrisi_kontakt():
    delete_id = simpledialog.askstring("Izbriši Kontakt", "Unesite ID kontakta koji želite izbrisati:")

    if delete_id:
        konekcija = sqlite3.connect('Imenik.db')
        kursor = konekcija.cursor()

        sql_naredba = '''
        DELETE FROM Imenik WHERE id = ?;
        '''
        podaci = (delete_id,)

        kursor.execute(sql_naredba, podaci)
        konekcija.commit()
        konekcija.close()
        messagebox.showinfo("Uspjeh", "Kontakt je uspješno izbrisan.")
    else:
        messagebox.showwarning("Greška", "Morate unijeti ID kontakta.")

root = tk.Tk()
root.title("Imenik")
root.geometry("300x200")
btn_dodaj = tk.Button(root, text="Dodaj Kontakt", command=dodaj_kontakt)
btn_dodaj.pack(pady=10)
btn_prikazi = tk.Button(root, text="Prikazi Kontakte", command=prikazi_kontakte)
btn_prikazi.pack(pady=10)   
btn_izbrisi = tk.Button(root, text="Izbriši Kontakt", command=izbrisi_kontakt)
btn_izbrisi.pack(pady=10)
btn_izlaz = tk.Button(root, text="Izlaz", command=root.quit)
btn_izlaz.pack(pady=10)
root.mainloop()
