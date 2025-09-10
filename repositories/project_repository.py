import sqlite3
from pathlib import Path
from typing import List, Dict

DB_PATH = Path(__file__).resolve().parents[1] / "database.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row          
    conn.execute("PRAGMA foreign_keys = ON;")  
    return conn

def add_project(name: str, created_in: str) -> int:
    conn = get_connection()
    try:
        cur = conn.execute(
            "INSERT INTO projects (name, created_in) VALUES (?, ?)",
            (name, created_in)
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()

def get_all_projects() -> List[Dict]:
    conn = get_connection()
    try:
        cur = conn.execute("SELECT id, name, created_in FROM projects ORDER BY id DESC")
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

def delete_project(project_id: int) -> bool:
    conn = get_connection()
    try:
        cur = conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()
