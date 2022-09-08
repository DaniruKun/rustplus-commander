"""SQLite adapter allowing to persist devices."""
import sqlite3
from typing import Any, Tuple

con = sqlite3.connect("devices.db")
cur = con.cursor()

def init_switches_table() -> sqlite3.Cursor:
  print('Initializing entity table(s)')
  cur.execute("CREATE TABLE IF NOT EXISTS switches(name text NOT NULL, entity_id text NOT NULL, owner CHAR)")
  print('Creating indexes')
  cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_switches_name ON switches (name)")

def register_entity(name: str, eid: str, owner: str) -> sqlite3.Cursor:
  print(f"Saving entity: {name} - {eid}")
  cur.execute("INSERT INTO switches VALUES(?, ?, ?)", (name, eid, owner))
  con.commit()
  
def get_entity_by_name(name: str) -> Any:
  cur.execute(
    "SELECT name, entity_id, owner FROM switches WHERE name = ?", (name,)
    ).fetchone()
