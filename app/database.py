import sqlite3
from flask import current_app, g

SCHEMA = """
CREATE TABLE IF NOT EXISTS instructors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS styles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS studios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    instructor_id INTEGER NOT NULL,
    style_id INTEGER,
    studio_id INTEGER,
    duration INTEGER,
    FOREIGN KEY(instructor_id) REFERENCES instructors(id),
    FOREIGN KEY(style_id) REFERENCES styles(id),
    FOREIGN KEY(studio_id) REFERENCES studios(id)
);
"""

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

def init_app(app):
    app.teardown_appcontext(close_db)

def close_db(exception=None):
    database = g.pop("db", None)
    if database is not None:
        database.close()

def create_tables():
    get_db().executescript(SCHEMA)
    get_db().commit()
