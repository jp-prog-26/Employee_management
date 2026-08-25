import sqlite3
import os
from flask import g, current_app

DATABASE_NAME = 'employees.db'


def get_db():
    """Retorna la conexion de BD del contexto actual de la request."""
    if 'db' not in g:
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
    """Crea las tablas si no existen y registra el teardown."""
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                document  TEXT    NOT NULL UNIQUE,
                full_name TEXT    NOT NULL,
                hire_date TEXT    NOT NULL,
                end_date  TEXT,
                status    TEXT    NOT NULL DEFAULT 'ACTIVE'
            )
        ''')
        db.commit()
    app.teardown_appcontext(close_db)
