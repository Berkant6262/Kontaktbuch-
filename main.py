import sqlite3


def connect_db():
    conn = sqlite3.connect("kontakte.db")  # Erstellt die Datei kontakte.db, wenn nicht da
    cursor = conn.cursor()
    # Tabelle Kontakte mit id, name, telefon, email
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kontakte (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            telefon TEXT,
            email TEXT
        )
    """)
    conn.commit()
    return conn




if __name__ == "__main__":
    connect_db()