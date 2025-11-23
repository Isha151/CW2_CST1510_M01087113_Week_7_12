import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DB_PATH = PROJECT_ROOT / "DATA" / "intelligence_platform.db"

def connect_database(db_path=None):
    if db_path is None:
        db_path = DB_PATH
    
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(str(db_path))