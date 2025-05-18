import sqlite3
import os

# Bildschirm löschen (Windows/Linux/Mac)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Verbindung zur SQLite-Datenbank herstellen
def connect_db():
    db = sqlite3.connect("kontakte.db")
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kontakte (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            telefon TEXT,
            email TEXT
        )
    """)
    db.commit()
    return db

# Kontakt zur Datenbank hinzufügen
def kontakt_hinzufuegen(db, name, telefon, email):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO kontakte (name, telefon, email) VALUES (?, ?, ?)",
        (name, telefon, email)
    )
    db.commit()
    print("\nKontakt wurde hinzugefügt.\n")

# Alle Kontakte anzeigen
def kontakte_anzeigen(db):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM kontakte")
    kontakte = cursor.fetchall()

    if not kontakte:
        print("\nKeine Kontakte gefunden.\n")
    else:
        print("\nKontakte:")
        for k in kontakte:
            print(f"ID: {k[0]}, Name: {k[1]}, Telefon: {k[2]}, Email: {k[3]}")
        print()

# Kontakte nach Name suchen
def kontakte_suchen(db, suchname):
    cursor = db.cursor()
    cursor.execute(
        "SELECT id, name, telefon, email FROM kontakte WHERE name LIKE ?",
        ('%' + suchname + '%',)
    )
    return cursor.fetchall()

# Kontakt löschen
def kontakte_loeschen(db):
    name = input("Name des Kontakts zum Löschen eingeben: ")
    treffer = kontakte_suchen(db, name)

    if not treffer:
        print("\nKein Kontakt gefunden.\n")
        return

    print("\nGefundene Kontakte:")
    for k in treffer:
        print(f"ID: {k[0]}, Name: {k[1]}, Telefon: {k[2]}, Email: {k[3]}")
    
    try:
        id_loeschen = int(input("\nID des zu löschenden Kontakts eingeben: "))
    except ValueError:
        print("Ungültige Eingabe.")
        return

    cursor = db.cursor()
    cursor.execute("DELETE FROM kontakte WHERE id = ?", (id_loeschen,))
    db.commit()
    print("Kontakt wurde gelöscht.\n")

def kontakte_bearbeiten(db):
    name = input("Name des Kontakts zum Bearbeiten eingeben: ")
    treffer = kontakte_suchen(db, name)

    if not treffer:
        print("\nKein Kontakt gefunden.\n")
        return

    print("\nGefundene Kontakte:")
    for k in treffer:
        print(f"ID: {k[0]}, Name: {k[1]}, Telefon: {k[2]}, Email: {k[3]}")

    try:
        id_bearbeiten = int(input("\nID des zu bearbeitenden Kontakts eingeben: "))
    except ValueError:
        print("Ungültige Eingabe.")
        return

    cursor = db.cursor()
    cursor.execute("SELECT name, telefon, email FROM kontakte WHERE id = ?", (id_bearbeiten,))
    kontakt = cursor.fetchone()

    if not kontakt:
        print("Kontakt mit dieser ID wurde nicht gefunden.")
        return

    print("\nNeuen Wert eingeben (leer lassen zum Beibehalten):")
    neuer_name = input(f"Name [{kontakt[0]}]: ") or kontakt[0]
    neuer_telefon = input(f"Telefon [{kontakt[1]}]: ") or kontakt[1]
    neuer_email = input(f"E-Mail [{kontakt[2]}]: ") or kontakt[2]

    cursor.execute("""
        UPDATE kontakte
        SET name = ?, telefon = ?, email = ?
        WHERE id = ?
    """, (neuer_name, neuer_telefon, neuer_email, id_bearbeiten))

    db.commit()
    print("Kontakt wurde aktualisiert.\n")


# Hauptprogramm
if __name__ == "__main__":
    db = connect_db()

    while True:
        print("Kontaktverwaltung")
        print("----------------------------")
        print("1 - Kontakt hinzufügen")
        print("2 - Kontakte anzeigen")
        print("3 - Kontakt löschen")
        print("4 - Kontakt bearbeiten ")
        print("0 - Programm beenden")
        print("----------------------------")

        try:
            auswahl = int(input("Was möchtest du tun? "))
        except ValueError:
            print("Bitte eine gültige Zahl eingeben.\n")
            continue

        clear_screen()

        if auswahl == 0:
            print("Programm beendet.")
            break
        elif auswahl == 1:
            name = input("Name: ")
            telefon = input("Telefon: ")
            email = input("E-Mail: ")
            kontakt_hinzufuegen(db, name, telefon, email)
        elif auswahl == 2:
            kontakte_anzeigen(db)
        elif auswahl == 3:
            kontakte_loeschen(db)
        elif auswahl == 4:
            kontakte_bearbeiten(db)
        else:
            print("Ungültige Auswahl.\n")
