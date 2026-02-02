CREATE TABLE Clanovi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ime TEXT NOT NULL,
    prezime TEXT NOT NULL,
    oib TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE,
);

CREATE TABLE Filmovi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    naslov TEXT NOT NULL,
    zanr TEXT NOT NULL,
    godina_izdanja INTEGER,
);

CREATE TABLE Posudbe (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cla_id INTEGER NOT NULL,
    flm_id INTEGER NOT NULL,
    datum_posudbe DATE NOT NULL,
    datum_vracanja DATE,
    FOREIGN KEY (cla_id) REFERENCES Clanovi(id),
    FOREIGN KEY (flm_id) REFERENCES Filmovi(id)
);