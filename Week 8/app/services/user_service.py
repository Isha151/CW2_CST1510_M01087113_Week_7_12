import bcrypt
from pathlib import Path
from app.data.users import insert_user, get_user_by_username
from app.data.db import connect_database

def register_user(username, password, role='user'):
    conn = connect_database()
    try:
        if get_user_by_username(conn, username):
            return False, f"Username '{username}' already exists."

        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
        
        insert_user(conn, username, hashed, role)
        return True, f"User '{username}' registered successfully."
    except Exception as e:
        return False, f"Registration failed: {e}"
    finally:
        conn.close()

def login_user(username, password):
    conn = connect_database()
    try:
        user = get_user_by_username(conn, username)
        
        if not user:
            return False, "User not found."
        
        stored_hash = user[2]
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
            return True, f"Login successful!"
        return False, "Incorrect password."
    finally:
        conn.close()

def migrate_users_from_file(conn, filepath=None):
    if filepath is None:
        filepath = Path(__file__).resolve().parent.parent.parent / "DATA" / "users.txt"

    if not filepath.exists():
        print(f"File not found: {filepath}")
        return

    print(f"Reading users from: {filepath}")
    
    migrated_count = 0
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.lower().startswith('username'):
                    continue
                
                parts = line.split(',')
                if len(parts) >= 2:
                    username = parts[0]
                    password_hash = parts[1]
                    role = parts[2] if len(parts) > 2 else 'user'
                    
                    try:
                        insert_user(conn, username, password_hash, role)
                        migrated_count += 1
                    except Exception:
                        pass
    except Exception as e:
        print(f"Error reading file: {e}")
                    
    print(f"Migrated {migrated_count} users.")