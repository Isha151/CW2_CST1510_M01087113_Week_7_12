import os
import pandas as pd
import sqlite3

# --- Absolute paths ---
csv_file = r"D:\MDX\CW2_CST1510_M01087113_Week_7_12\Week 8\DATA\datasets_metadata.csv"
db_file = r"D:\MDX\CW2_CST1510_M01087113_Week_7_12\Week 8\DATA\intelligence_platform.db"

# --- Check CSV exists ---
if not os.path.exists(csv_file):
    raise FileNotFoundError(f"CSV file not found at {csv_file}")

# --- Read CSV ---
df_csv = pd.read_csv(csv_file)

# --- Connect to the existing DB ---
conn = sqlite3.connect(db_file, timeout=30)
cursor = conn.cursor()

# --- Create the table if it doesn't exist ---
create_table_sql = """
CREATE TABLE IF NOT EXISTS datasets_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dataset_name TEXT NOT NULL,
    category TEXT,
    source TEXT,
    last_updated TEXT,
    record_count INTEGER,
    file_size_mb REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""
cursor.execute(create_table_sql)
conn.commit()
print("✅ datasets_metadata table ensured in existing DB!")

# --- Insert each row from CSV ---
for _, row in df_csv.iterrows():
    dataset_name = row.get("dataset_name")
    category = row.get("category")
    source = row.get("source")
    last_updated = row.get("last_updated")
    record_count = row.get("record_count")
    file_size_mb = row.get("file_size_mb")

    if dataset_name:  # Skip rows without dataset_name
        cursor.execute(
            """
            INSERT INTO datasets_metadata
            (dataset_name, category, source, last_updated, record_count, file_size_mb)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (dataset_name, category, source, last_updated, record_count, file_size_mb)
        )
        conn.commit()  # commit after each row to avoid DB locks

conn.close()
print("✅ CSV data migrated successfully into datasets_metadata table!")
