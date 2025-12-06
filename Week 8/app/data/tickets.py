import sqlite3
import pandas as pd

def create_it_tickets_table(conn):
    cursor = conn.cursor()
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS it_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id TEXT UNIQUE,
        priority TEXT,
        status TEXT,
        category TEXT,
        subject TEXT NOT NULL,
        description TEXT,
        created_date TEXT,
        resolved_date TEXT,
        assigned_to TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    '''
    cursor.execute(create_table_sql)
    conn.commit()
    print('✅ it_tickets table created successfully!')

def get_all_incidents(conn):
    create_it_tickets_table(conn)  # ensure table exists
    return pd.read_sql_query("SELECT * FROM it_tickets", conn)

def insert_ticket(conn, subject, priority, status):
    """
    Insert a new ticket into the database.
    """
    create_it_tickets_table(conn)  # Ensure table exists
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO it_tickets (subject, priority, status) VALUES (?, ?, ?)",
        (subject, priority, status)
    )
    conn.commit()
