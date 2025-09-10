import sqlite3
from pathlib import Path
from typing import List, Dict, Optional

DB_PATH = Path(__file__).resolve().parents[1] / "database.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def add_element(project_id: int, structural_type: str, structural_data_json: str,
                results_json: Optional[str], created_in: str) -> int:
    conn = get_connection()
    try:
        cur = conn.execute(
            """INSERT INTO structural_elements
               (project_id, structural_type, structural_data, results, created_in)
               VALUES (?, ?, ?, ?, ?)""",
            (project_id, structural_type, structural_data_json, results_json, created_in)
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()

def get_elements_by_project(project_id: int) -> List[Dict]:
    conn = get_connection()
    try:
        cur = conn.execute(
            """SELECT id, project_id, structural_type, structural_data, results, created_in
               FROM structural_elements
               WHERE project_id = ?
               ORDER BY id DESC""",
            (project_id,)
        )
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

def delete_element(element_id: int) -> bool:
    conn = get_connection()
    try:
        cur = conn.execute("DELETE FROM structural_elements WHERE id = ?", (element_id,))
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()
