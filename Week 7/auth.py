import bcrypt
import os

USER_DATA_FILE = "users.txt"

def hash_password(password):
   
    # TODO: Encode the password to bytes (bcrypt requires byte strings)
    byte_data = password.encode('utf-8')
    
    # TODO: Generate a salt using bcrypt.gensalt()
    salt = bcrypt.gensalt()
    
    # TODO: Hash the password using bcrypt.hashpw()
    hashed_password_bytes = bcrypt.hashpw(byte_data, salt)
    
    # TODO: Decode the hash back to a string to store in a text file
    hashed_password_string = hashed_password_bytes.decode('utf-8')

    return hashed_password_string

def verify_password(password, hashed_password):
    
    # TODO: Encode both the plaintext password and the stored hash to byt
    plain_text_bytes = password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    
    # TODO: Use bcrypt.checkpw() to verify the password
    # This function extracts the salt from the hash and compares

    match = bcrypt.checkpw(plain_text_bytes, hashed_bytes)
    
    return match

def register_user(username, password):
   
    with open(USER_DATA_FILE, 'r') as f:
            for line in f:
                existing_username = line.strip().split(',')[0]
                if username == existing_username:
                    print(f"User '{username}' already exists.")
                    return False
                
    hashed_password = hash_password(password)

    with open(USER_DATA_FILE, 'a') as f:
        f.write(f"{username},{hashed_password}\n")
    
    print(f"User '{username}' successfully registered.")
    return True

def user_exists(username):
    # TODO: Handle the case where the file doesn't exist yet
    if not os.path.exists(USER_DATA_FILE):
        return False
  
    
    # TODO: Read the file and check each line for the username
    existing_username = username
    with open(USER_DATA_FILE, 'r') as f:
        for line in f:
                existing_username = line.strip().split(',')[0]
                if username == existing_username:
                    print(f"User '{username}' already exists.")
                    return True
  
    return False

def login_user(username, password):
    # TODO: Handle the case where no users are registered yet
    if not os.path.exists(USER_DATA_FILE):
         print("Login failed, no users registered yet!")
         return False
   
    
    # TODO: Search for the username in the file
    with open(USER_DATA_FILE, 'r') as f:
         for line in f:
              parts = line.strip().split(',',1)
              if len(parts)==2:
                   existing_username, hashed_password = parts
                   if username == existing_username:
                    found_user = True
                    stored_hash = hashed_password
                    break
 
    # TODO: If username matches, verify the password
    if found_user:
         if verify_password(password, hashed_password):
              print(f'Login successful for user{username}')
              return True
         
            # TODO: If we reach here, the username was not found

         else:
              print(f"Login failed: User '{username}' not found.")
              return False


def validate_username(username):
    MIN_LENGTH = 3
    MAX_LENGTH = 20

    if len(username) < 3:
         error_message = ("Username too short")
         return False, error_message
    if len(username) > 20:
         error_message = ("Username too long")
         return False, error_message
    else:
        pass


def validate_password(password):
    min_length = 10
    has_upper = False
    has_lower = False
    has_special = False
    has_number = False

    if not password:
         print("Password cannot be empty")
         return False
    
    if len(password) < min_length:
        return False, f"Password must be at least {min_length} characters long."

    for char in password:
         if char.isupper():
              has_upper = True
         if char.islower():
              has_lower = True
         if char.isdigit():
              has_number = True
         if not char.isalnum():
              has_special = True

    if not has_upper:
        return False, "Password must contain at least one uppercase letter."
    
    if not has_lower:
        return False, "Password must contain at least one lowercase letter."
    
    if not has_number:
        return False, "Password must contain at least one number."
        
    if not has_special:
        return False, "Password must contain at least one special character (e.g., !@#$%^&*)."
    
    
    
              
    pass
    
 
