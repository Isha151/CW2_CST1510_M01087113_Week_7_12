import sqlite3
import os

def connect_database():
    # 1. Get the folder where THIS file is right now
    current_dir = os.path.dirname(__file__)

    # 2. Create the path to the database
    # ".." means "go up one folder". We do it twice to go back two levels.
    db_path = os.path.join(current_dir, "../../DATA/intelligence_platform.db")

    # 3. Connect and return the connection
    return sqlite3.connect(db_path)