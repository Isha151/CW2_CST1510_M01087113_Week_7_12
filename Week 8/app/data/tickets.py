import sqlite3
import pandas as pd
import uuid

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

def get_all_tickets(conn):
    create_it_tickets_table(conn)  
    return pd.read_sql_query("SELECT * FROM it_tickets", conn)

def insert_ticket(conn, subject, priority, status, category, description):
    cursor = conn.cursor()
    sql = """
        INSERT INTO it_tickets (subject, priority, status, category, description)
        VALUES (?, ?, ?, ?, ?)
    """
    cursor.execute(sql, (subject, priority, status, category, description))
    conn.commit()
    return cursor.rowcount


def update_ticket(conn, ticket_id, new_status, new_priority):
    cursor = conn.cursor()
    sql = """
        UPDATE it_tickets
        SET status = ?, priority = ?
        WHERE id = ?
    """
    cursor.execute(sql, (new_status, new_priority, ticket_id))
    conn.commit()
    return cursor.rowcount


def delete_ticket(conn, ticket_id):
    cursor = conn.cursor()
    sql = "DELETE FROM it_tickets WHERE id = ?"
    cursor.execute(sql, (ticket_id,))
    conn.commit()
    return cursor.rowcount
