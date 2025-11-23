from app.data.db import connect_database

def get_user_by_username(conn, username):
    """
    Retrieve a user record from the database.
    Used by: login_user (in services)
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cursor.fetchone()

def insert_user(conn, username, password_hash, role='user'):
    """
    Insert a new user into the database.
    Used by: register_user (in services)
    """
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role)
    )
    conn.commit()