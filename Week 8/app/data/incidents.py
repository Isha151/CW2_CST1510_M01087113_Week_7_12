import pandas as pd


def load_csv_to_table(conn, csv_path, table_name):
    """Load a CSV file into the database."""
    if not csv_path.exists():
        print(f"⚠️ File not found: {csv_path}")
        return 0
    
    try:
        df = pd.read_csv(csv_path)
        # Write to database
        df.to_sql(name=table_name, con=conn, if_exists='append', index=False)
        print(f"✅ Loaded {len(df)} rows into '{table_name}'")
        return len(df)
    except Exception as e:
        print(f"❌ Error loading {table_name}: {e}")
        return 0


def insert_incident(conn, date, incident_type, severity, status, description, reported_by=None):
    cursor = conn.cursor()
    sql = """
        INSERT INTO cyber_incidents 
        (date, incident_type, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor.execute(sql, (date, incident_type, severity, status, description, reported_by))
    conn.commit()
    return cursor.lastrowid

def get_all_incidents(conn):
    return pd.read_sql_query("SELECT * FROM cyber_incidents", conn)

def update_incident_status(conn, incident_id, new_status):
    cursor = conn.cursor()
    sql = "UPDATE cyber_incidents SET status = ? WHERE id = ?"
    cursor.execute(sql, (new_status, incident_id))
    conn.commit()
    return cursor.rowcount

def delete_incident(conn, incident_id):
    cursor = conn.cursor()
    sql = "DELETE FROM cyber_incidents WHERE id = ?"
    cursor.execute(sql, (incident_id,))
    conn.commit()
    return cursor.rowcount