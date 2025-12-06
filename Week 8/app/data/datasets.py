import pandas as pd



def get_all_datasets(conn):
    try:
        df = pd.read_sql_query("SELECT * FROM datasets_metadata", conn)
        return df
    except Exception:
        return pd.DataFrame()

def insert_dataset(conn, dataset_name, description, records):
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO datasets_metadata (dataset_name, description, records)
        VALUES (?, ?, ?)
        """,
        (dataset_name, description, records)
    )
    conn.commit()
