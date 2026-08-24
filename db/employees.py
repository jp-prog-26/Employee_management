import sqlite3

conexion = sqlite3.connect("employees.db")

conexion.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_document TEXT NOT NULL UNIQUE,
        fullName TEXT NOT NULL,
        date_hired TEXT NOT NULL,
        date_terminated TEXT,
        status TEXT NOT NULL DEFAULT 'ACTIVE'
    )
""")

conexion.commit()
conexion.close()