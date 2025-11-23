import pandas as pd
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "DATA"

from app.data.db import connect_database
from app.data.schema import (
    create_users_table, 
    create_cyber_incidents_table, 
    create_datasets_metadata_table, 
    create_it_tickets_table
)
from app.services.user_service import migrate_users_from_file
from app.data.incidents import load_csv_to_table

def setup_database_complete():
    print("-" * 60)
    print("STARTING DATABASE SETUP")
    print("-" * 60)
    
    conn = connect_database()
    
    conn.execute("DROP TABLE IF EXISTS users")
    conn.execute("DROP TABLE IF EXISTS cyber_incidents")
    conn.execute("DROP TABLE IF EXISTS datasets_metadata")
    conn.execute("DROP TABLE IF EXISTS it_tickets")
    
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)
    
    try:
        migrate_users_from_file(conn, filepath=DATA_DIR / "users.txt")
    except Exception as e:
        print(f"Migration error: {e}")
    
    try:
        df = pd.read_csv(DATA_DIR / "cyber_incidents.csv")
        
        df = df.rename(columns={
            "Date": "date", 
            "Type": "incident_type", 
            "Description": "description"
        })
        
        df["severity"] = "Medium"
        df["status"] = "Open"
        df["reported_by"] = "alice"
        
        valid_columns = ["date", "incident_type", "severity", "status", "description", "reported_by"]
        df_clean = df[valid_columns]
        
        df_clean.to_sql("cyber_incidents", conn, if_exists="append", index=False)
        print(f"Loaded {len(df_clean)} rows into cyber_incidents")
    except Exception as e:
        print(f"Error processing cyber_incidents: {e}")

    load_csv_to_table(conn, DATA_DIR / "datasets_metadata.csv", "datasets_metadata")
    load_csv_to_table(conn, DATA_DIR / "it_tickets.csv", "it_tickets")
    
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM it_tickets")
    print(f"IT Tickets Row Count: {cursor.fetchone()[0]}")
    
    conn.close()
    print("DATABASE SETUP COMPLETE")

if __name__ == "__main__":
    setup_database_complete()