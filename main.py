import sqlite3
import os

#Terminal clearen, bei Python gibt es keinen direkten Befehel
def clear_screen():
    if os.name == 'nt': #Falls das Betriebssystem Windows ist
        os.system('cls')
    else:
        os.system('clear') # Linux oder Mac

#Erstellen der Datenbank 
def connect_db():
    _db = sqlite3.connect("kontakte.db")  # Erstellt die Datei kontakte.db, wenn nicht da
    _cursor = _db.cursor()
    # Tabelle Kontakte mit id, name, telefon, email
    _cursor.execute("""
        CREATE TABLE IF NOT EXISTS kontakte (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            telefon TEXT,
            email TEXT
        )
    """)
    _db.commit()
    return _db

#Fuegt Kontakte (Einträge in die Tabelle)
def kontakt_hinzufügen(db,name,telefon,email):
    _cursor = db.cursor()
    _cursor.execute("""
                INSERT INTO kontakte (name,telefon, email)
                VALUES (?,?,?)
                """,
                (name,telefon,email) 
                )

    db.commit()
    print("Kontakt wurde hinzugefügt")

#Zeigt die Kontakte an die mein bereits in der Datenbank hat 
def kontakte_anzeigen(_db):
    _cursor = _db.cursor()
    _cursor.execute("SELECT * FROM kontakte")
    alle = _cursor.fetchall()
    for kontakt in alle:
        print(kontakt)


if __name__ == "__main__":
    _db = connect_db()

    while True:
        print("Kontakt hinzufügen(1)\nProgramm schliessen(0)\nKontakte anzeigen(2)\n")
        try:
            _choiche = int(input("Was moechten sie tun (Zahl eingeben): "))
        except ValueError:
            print("Bitte eine gültige Zahl eingeben.")
            continue  # Schleife von vorne starten

        if _choiche == 0:
            print("Ciao")
            break
        elif _choiche == 1:
            clear_screen()
            _name = input("name: ")
            _tel = input("tel: ")
            _email = input("email: ")
            kontakt_hinzufügen(_db, _name, _tel, _email)
        elif _choiche == 2:
            kontakte_anzeigen(_db)
