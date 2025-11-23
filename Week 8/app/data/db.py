import sqlite3
from pathlib import Path

# --- FIX: USE ABSOLUTE PATHS ---
# This gets the folder where db.py is located (Week 8/app/data)
BASE_DIR = Path(__file__).resolve().parent

# This points exactly to Week 8/app/data/DATA/intelligence_platform.db
DB_PATH = BASE_DIR / "DATA" / "intelligence_platform.db"

def connect_database(db_path=None):
    """
    Connect to the SQLite database.
    If no path is provided, it uses the fixed DB_PATH.
    """
    if db_path is None:
        db_path = DB_PATH
        
    # Create the folder if it doesn't exist (just in case)
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    
    return sqlite3.connect(str(db_path))