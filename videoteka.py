import sqlite3

conn = sqlite3.connect('videoteka.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Clanovi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ime TEXT NOT NULL,
    prezime TEXT NOT NULL,
    oib TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE);''')

conn.commit()
conn.close()


conn = sqlite3.connect('videoteka.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS Filmovi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    naslov TEXT NOT NULL,
    zanr TEXT NOT NULL,
    godina_izdanja INTEGER);''')

conn.commit()
conn.close()

conn = sqlite3.connect('videoteka.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS Posudbe (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cla_id INTEGER NOT NULL,
    flm_id INTEGER NOT NULL,
    datum_posudbe DATE NOT NULL,
    datum_vracanja DATE,
    FOREIGN KEY (cla_id) REFERENCES Clanovi(id),
    FOREIGN KEY (flm_id) REFERENCES Filmovi(id));''')

conn.commit()
conn.close()

# UI

def dodaj_clana():
    ime = input("Unesite ime clana: ")
    prezime = input("Unesite prezime clana: ")
    oib = input("Unesite OIB clana: ")
    email = input("Unesite email clana (opcionalno): ")

    conn = sqlite3.connect('videoteka.db')
    cur = conn.cursor()

    cur.execute('''INSERT INTO Clanovi (ime, prezime, oib, email) VALUES (?, ?, ?, ?);''', (ime, prezime, oib, email))
    conn.commit()
    conn.close()
    print("Clan dodat u bazu podataka.")

def prikazi_clanove():
    print("\n--- CLANOVI ---")
    conn = sqlite3.connect('videoteka.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM Clanovi;")
    rezultati = cur.fetchall()

    print("ID | Ime | Prezime | OIB | Email")
    print("----------------------------------")
    for red in rezultati:
        print(f"{red[0]} | {red[1]} | {red[2]} | {red[3]} | {red[4]}")
    print("----------------------------------\n")

    conn.close()

def izbrisi_clana():
    prikazi_clanove()
    delete_id = input("Unesite ID clana koji zelite izbrisati: ")

    conn = sqlite3.connect('videoteka.db')
    cur = conn.cursor()

    cur.execute("DELETE FROM Clanovi WHERE id = ?;", (delete_id,))
    conn.commit()
    conn.close()
    print("Clan izbrisan iz baze podataka.")

def dodaj_film():
    naslov = input("Unesite naslov filma: ")
    zanr = input("Unesite zanr filma: ")
    godina_izdanja = int(input("Unesite godinu izdanja filma: "))

    conn = sqlite3.connect('videoteka.db')
    cur = conn.cursor()

    cur.execute('''INSERT INTO Filmovi (naslov, zanr, godina_izdanja) VALUES (?, ?, ?);''', (naslov, zanr, godina_izdanja))
    conn.commit()
    conn.close()
    print("Film dodat u bazu podataka.")

def prikazi_filmove():
    print("\n--- FILMOVI ---")
    conn = sqlite3.connect('videoteka.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM Filmovi;")
    rezultati = cur.fetchall()

    print("ID | Naslov | Zanr | Godina Izdanja")
    print("-------------------------------------")
    for red in rezultati:
        print(f"{red[0]} | {red[1]} | {red[2]} | {red[3]}")
    print("-------------------------------------\n")

    conn.close()

def izbrisi_film():
    prikazi_filmove()
    delete_id = input("Unesite ID filma koji zelite izbrisati: ")

    conn = sqlite3.connect('videoteka.db')
    cur = conn.cursor()

    cur.execute("DELETE FROM Filmovi WHERE id = ?;", (delete_id,))
    conn.commit()
    conn.close()
    print("Film izbrisan iz baze podataka.")

def posudi_film():
    prikazi_clanove()
    cla_id = input("Unesite ID clana koji posuduje film: ")
    conn = sqlite3.connect('videoteka.db')
    cur = conn.cursor()
    if not cur.execute("SELECT id FROM Clanovi WHERE id = ?;", (cla_id,)).fetchone():
        print("Clan s tim ID-om ne postoji. Pokušajte ponovo.")
        conn.close()
        posudi_film()
        return
        
    prikazi_filmove()
    flm_id = input("Unesite ID filma koji se posudjuje: ")
    if not cur.execute("SELECT id FROM Filmovi WHERE id = ?;", (flm_id,)).fetchone():
        print("Film s tim ID-om ne postoji. Pokušajte ponovo.")
        conn.close()
        posudi_film()
        return
    
    elif cur.execute("SELECT id FROM Posudbe WHERE flm_id = ? AND datum_vracanja IS NULL;", (flm_id,)).fetchone():
        print("Film je trenutno posuđen i nije vraćen. Pokušajte ponovo.")
        conn.close()
        posudi_film()
        return
    
    else:
        pass

    datum_posudbe = input("Unesite datum posudbe (YYYY-MM-DD): ")

    conn = sqlite3.connect('videoteka.db')
    cur = conn.cursor()

    cur.execute('''INSERT INTO Posudbe (cla_id, flm_id, datum_posudbe) VALUES (?, ?, ?);''', (cla_id, flm_id, datum_posudbe))
    conn.commit()
    conn.close()
    print("Film posudjen clanu.")

def prikazi_posudbe():
    print("\n--- POSUDBE ---")
    conn = sqlite3.connect('videoteka.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM Posudbe;")
    rezultati = cur.fetchall()  

    print("ID | ID Clana | ID Filma | Datum Posudbe | Datum Vracanja")
    print("--------------------------------------------------------")
    for red in rezultati:
        print(f"{red[0]} | {red[1]} | {red[2]} | {red[3]} | {red[4] if red[4] else 'Nije vracen'}")
    print("--------------------------------------------------------\n")

    conn.close()

def prikazi_posudjene_filmove():

    print("\n--- POSUĐENI FILMOVI ---")

    conn = sqlite3.connect('videoteka.db')
    cur = conn.cursor()

    cur.execute('''SELECT Posudbe.id, Clanovi.ime || ' ' || Clanovi.prezime AS clan, Filmovi.naslov, Posudbe.datum_posudbe
                   FROM Posudbe
                   JOIN Clanovi ON Posudbe.cla_id = Clanovi.id
                   JOIN Filmovi ON Posudbe.flm_id = Filmovi.id
                   WHERE Posudbe.datum_vracanja IS NULL;''')
    rezultati = cur.fetchall()

    print("ID | Clan | Naslov   | Datum Posudbe")
    print("---------------------------------------")
    for red in rezultati:
        print(f"{red[0]} | {red[1]} | {red[2]} | {red[3]}")
    print("---------------------------------------\n")

    conn.close()


def vrati_film():
    prikazi_posudjene_filmove()
    posudba_id = input("Unesite ID posudbe za film koji se vraca: ")

    conn = sqlite3.connect('videoteka.db')
    cur = conn.cursor()

    if not cur.execute("SELECT id FROM Posudbe WHERE id = ? AND datum_vracanja IS NULL;", (posudba_id,)).fetchone():
        print("Posudba s tim ID-om ne postoji ili je film već vraćen. Pokušajte ponovo.")
        conn.close()
        vrati_film()
        return
    
    else:
        pass

    datum_vracanja = input("Unesite datum vracanja (YYYY-MM-DD): ")

    cur.execute("UPDATE Posudbe SET datum_vracanja = ? WHERE id = ?;", (datum_vracanja, posudba_id))
    conn.commit()
    conn.close()
    print("Film vracen i posudba azurirana.")






while True:
    print("1. Dodaj clana")
    print("2. Prikazi clanove")
    print("3. Izbrisi clana")
    print("4. Dodaj film")
    print("5. Prikazi filmove")
    print("6. Izbrisi film")
    print("7. Posudi film")
    print("8. Prikazi posudbe")
    print("9. Vrati film")
    print("10. Izlaz")

    izbor = input("Izaberite opciju: ")

    if izbor == '1':
        dodaj_clana()
    elif izbor == '2':
        prikazi_clanove()
    elif izbor == '3':
        izbrisi_clana()
    elif izbor == '4':
        dodaj_film()
    elif izbor == '5':
        prikazi_filmove()
    elif izbor == '6':
        izbrisi_film()
    elif izbor == '7':
        posudi_film()
    elif izbor == '8':
        prikazi_posudbe()
    elif izbor == '9':
        vrati_film()
    elif izbor == '10':
        print("Izlaz iz programa.")
        break
    else:
        print("Neispravan unos, pokusajte ponovo.")