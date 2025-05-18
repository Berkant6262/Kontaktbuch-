from datenbank_funktion import * 
import tkinter as tk 
from tkinter import messagebox, simpledialog

# Datenbankverbindung
db = connect_db()

# Hauptfenster erstellen
root = tk.Tk()
root.title("Kontaktverwaltung")

# Funktionen für Buttons
def kontakt_hinzufuegen_gui():
    name = simpledialog.askstring("Name", "Gib den Namen ein:")
    telefon = simpledialog.askstring("Telefon", "Gib die Telefonnummer ein:")
    email = simpledialog.askstring("E-Mail", "Gib die E-Mail ein:")
    if name:
        kontakt_hinzufuegen(db, name, telefon, email)

def kontakte_anzeigen_gui():
    kontakte = kontakte_suchen(db, "")  # alle
    if not kontakte:
        messagebox.showinfo("Kontakte", "Keine Kontakte gefunden.")
        return
    anzeigen = "\n".join([f"ID: {k[0]}, Name: {k[1]}, Telefon: {k[2]}, Email: {k[3]}" for k in kontakte])
    messagebox.showinfo("Alle Kontakte", anzeigen)

def kontakte_loeschen_gui():
    name = simpledialog.askstring("Löschen", "Name des Kontakts:")
    if not name:
        return
    treffer = kontakte_suchen(db, name)
    if not treffer:
        messagebox.showinfo("Löschen", "Kein Kontakt gefunden.")
        return
    auswahl = "\n".join([f"{k[0]}: {k[1]} ({k[2]}, {k[3]})" for k in treffer])
    id_str = simpledialog.askstring("Löschen", f"Gefunden:\n{auswahl}\nGib die ID zum Löschen ein:")
    if not id_str or not id_str.isdigit():
        return
    cursor = db.cursor()
    cursor.execute("DELETE FROM kontakte WHERE id = ?", (int(id_str),))
    db.commit()
    messagebox.showinfo("Löschen", "Kontakt gelöscht.")

def kontakte_bearbeiten_gui():
    name = simpledialog.askstring("Bearbeiten", "Name des Kontakts:")
    if not name:
        return
    treffer = kontakte_suchen(db, name)
    if not treffer:
        messagebox.showinfo("Bearbeiten", "Kein Kontakt gefunden.")
        return
    auswahl = "\n".join([f"{k[0]}: {k[1]} ({k[2]}, {k[3]})" for k in treffer])
    id_str = simpledialog.askstring("Bearbeiten", f"Gefunden:\n{auswahl}\nGib die ID zum Bearbeiten ein:")
    if not id_str or not id_str.isdigit():
        return
    id_bearbeiten = int(id_str)
    cursor = db.cursor()
    cursor.execute("SELECT name, telefon, email FROM kontakte WHERE id = ?", (id_bearbeiten,))
    kontakt = cursor.fetchone()
    if not kontakt:
        messagebox.showinfo("Bearbeiten", "Kontakt nicht gefunden.")
        return

    neuer_name = simpledialog.askstring("Bearbeiten", f"Name [{kontakt[0]}]:") or kontakt[0]
    neuer_telefon = simpledialog.askstring("Bearbeiten", f"Telefon [{kontakt[1]}]:") or kontakt[1]
    neuer_email = simpledialog.askstring("Bearbeiten", f"E-Mail [{kontakt[2]}]:") or kontakt[2]

    cursor.execute("""
        UPDATE kontakte SET name = ?, telefon = ?, email = ? WHERE id = ?
    """, (neuer_name, neuer_telefon, neuer_email, id_bearbeiten))
    db.commit()
    messagebox.showinfo("Bearbeiten", "Kontakt aktualisiert.")

# GUI Buttons
tk.Button(root, text="Kontakt hinzufügen", command=kontakt_hinzufuegen_gui, width=30).pack(pady=5)
tk.Button(root, text="Kontakte anzeigen", command=kontakte_anzeigen_gui, width=30).pack(pady=5)
tk.Button(root, text="Kontakt löschen", command=kontakte_loeschen_gui, width=30).pack(pady=5)
tk.Button(root, text="Kontakt bearbeiten", command=kontakte_bearbeiten_gui, width=30).pack(pady=5)
tk.Button(root, text="Beenden", command=root.quit, width=30).pack(pady=20)

# Fenster starten
root.mainloop()
