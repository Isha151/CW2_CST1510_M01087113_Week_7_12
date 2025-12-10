import pandas as pd

def get_all_datasets(conn):
    try:
        df = pd.read_sql_query("SELECT * FROM datasets_metadata", conn)
        return df
    except Exception:
        return pd.DataFrame()

def insert_dataset(conn, dataset_name, category, source, last_updated, record_count, file_size_mb):
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO datasets_metadata (dataset_name, category, source, last_updated, record_count, file_size_mb)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (dataset_name, category, source, last_updated, record_count, file_size_mb)
    )
    conn.commit()

def update_dataset(conn, dataset_id, dataset_name, category, source, last_updated, record_count, file_size_mb):
    cursor = conn.cursor()
    sql = """
        UPDATE datasets_metadata
        SET dataset_name = ?, category = ?, source = ?, last_updated = ?, 
            record_count = ?, file_size_mb = ?
        WHERE id = ?
    """
    cursor.execute(sql, (
        dataset_name, category, source, last_updated, record_count, file_size_mb, dataset_id
    ))
    conn.commit()
    return cursor.rowcount

def delete_dataset(conn, dataset_id):
    cursor = conn.cursor()
    sql = "DELETE FROM datasets_metadata WHERE id = ?"
    cursor.execute(sql, (dataset_id,))
    conn.commit()
    return cursor.rowcount
