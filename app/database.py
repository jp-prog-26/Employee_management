import sqlite3
import os
from flask import g, current_app

# Nombre de la base de datos local de la app.
DATABASE_NAME = 'employees.db'

def get_db():
    """Retorna la conexion de BD del contexto actual de la request."""
    if 'db' not in g:
        # Se guarda la conexión en el contexto de Flask para reutilizarla durante la request.
        db_path = os.path.join(current_app.instance_path, DATABASE_NAME)
        os.makedirs(current_app.instance_path, exist_ok=True)
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
        g.db.execute('PRAGMA journal_mode=WAL')
    return g.db


def close_db(e=None):
    """Cierra la conexion al finalizar la request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db(app):
    """Crea las tablas si no existen, aplica migraciones y registra el teardown."""
    with app.app_context():
        db = get_db()

        # Crear tabla base (incluye las 4 columnas de nombre + full_name para compatibilidad)
        db.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                document        TEXT    NOT NULL UNIQUE,
                first_name      TEXT    NOT NULL DEFAULT '',
                second_name     TEXT             DEFAULT '',
                first_lastname  TEXT    NOT NULL DEFAULT '',
                second_lastname TEXT             DEFAULT '',
                full_name       TEXT             DEFAULT '',
                hire_date       TEXT    NOT NULL,
                end_date        TEXT,
                status          TEXT    NOT NULL DEFAULT 'ACTIVE'
            )
        ''')

        # Compatibilidad con versiones previas: si la tabla ya existe, se agregan columnas faltantes.
        migrations = [
            ('first_name',      "TEXT NOT NULL DEFAULT ''"),
            ('second_name',     "TEXT DEFAULT ''"),
            ('first_lastname',  "TEXT NOT NULL DEFAULT ''"),
            ('second_lastname', "TEXT DEFAULT ''"),
        ]
        for col, definition in migrations:
            try:
                db.execute(f'ALTER TABLE employees ADD COLUMN {col} {definition}')
            except Exception:
                pass  # La columna ya existe, se ignora el error

        db.commit()
    app.teardown_appcontext(close_db)
