import bcrypt
import os

USER_DATA_FILE = "users.txt"

def hash_password(plain_text_password):
   
    # TODO: Encode the password to bytes (bcrypt requires byte strings)
    byte_data = plain_text_password.encode('utf-8')
    
    # TODO: Generate a salt using bcrypt.gensalt()
    salt = bcrypt.gensalt()
    
    # TODO: Hash the password using bcrypt.hashpw()
    hashed_password_bytes = bcrypt.hashpw(byte_data, salt)
    
    # TODO: Decode the hash back to a string to store in a text file
    hashed_password_string = hashed_password_bytes.decode('utf-8')

    return hashed_password_string

def verify_password(plain_text_password, hashed_password):
    
    # TODO: Encode both the plaintext password and the stored hash to byt
    plain_text_bytes = plain_text_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    
    # TODO: Use bcrypt.checkpw() to verify the password
    # This function extracts the salt from the hash and compares

    match = bcrypt.checkpw(plain_text_bytes, hashed_bytes)
    

    return match



def register_user(username, password):
   
    # TODO: Check if the username already exists
    if username in 'user.txt':
        print("User already exsists")
        return
    
    # TODO: Hash the password
    hash_password = password.encode('utf-8')
    
    # TODO: Append the new user to the file
    # Format: username,hashed_password
    with open('users.txt', 'w'):
        users.txt.append(username, password)
   
    return True