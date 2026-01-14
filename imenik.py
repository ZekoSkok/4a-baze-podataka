
import sqlite3

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
    unos_ime = input("Unesite ime: ")
    unos_prezime = input("Unesite prezime: ")
    unos_broj_telefona = input("Unesite broj telefona: ")

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

def prikazi_kontakte():
    print("\n--- KONTAKTI ---")
    konekcija = sqlite3.connect('Imenik.db')
    kursor = konekcija.cursor()

    kursor.execute("SELECT * FROM Imenik;")
    rezultati = kursor.fetchall()

    print("ID  | Ime | Prezime | Broj Telefona")
    print("---------------------")
    for red in rezultati:
        print(f"{red[0]} | {red[1]} | {red[2]} | {red[3]}")
    print("---------------------\n")

    konekcija.close()

def izbrisi_kontakt():
    prikazi_kontakte()
    delete_id = input("Unesite ID kontakta koji zelite izbrisati: ")

    konekcija = sqlite3.connect('Imenik.db')
    kursor = konekcija.cursor()

    sql_naredba = '''
    DELETE FROM Imenik WHERE id = ?;
    '''
    podaci = (delete_id,)

    kursor.execute(sql_naredba, podaci)
    konekcija.commit()
    konekcija.close()

while True:
    print("1. Dodaj kontakt")
    print("2. Prikazi kontakte")
    print("3. Izbrisi kontakt")
    print("4. Izlaz")

    izbor = input("Izaberite opciju (1-4): ")

    if izbor == '1':
        dodaj_kontakt()
    elif izbor == '2':
        prikazi_kontakte()
    elif izbor == '3':
        izbrisi_kontakt()
    elif izbor == '4':
        print("Izlaz iz programa.")
        break
    else:
        print("Nepostojeca opcija, pokusajte ponovo.")