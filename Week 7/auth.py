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
    
    if user_exists(username):
        print(f"\nUser '{username}' already exists. Registration aborted.")
        return False

    hashed_password = hash_password(password)


    try:
        with open(USER_DATA_FILE, 'a') as f:
            f.write(f"{username},{hashed_password}\n")
        
        print(f"\nSUCCESS: User '{username}' successfully registered.")
        return True
    except IOError as e:
        print(f"Error writing to user data file: {e}")
        return False

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
        return True, ""


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
    
    return True, ""
    



def display_menu():
    """Displays the main menu options."""
    print("\n" + "="*50)
    print("  MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print("  Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)
def main():
    """Main program loop."""
    print("\nWelcome to the Week 7 Authentication System!")
    
    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()
        
        if choice == '1':
            # Registration flow
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()
            
            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
            
            password = input("Enter a password: ").strip()
            
            # Validate password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
            
            # Confirm password
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue
            
            # Register the user
            register_user(username, password)
        
        elif choice == '2':
            # Login flow
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            
            # Attempt login
            if login_user(username, password):
                print("\nYou are now logged in.")
                print("(In a real application, you would now access the website)")
                
                # Optional: Ask if they want to logout or exit
                input("\nPress Enter to return to main menu...")
        
        elif choice == '3':
            # Exit
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break
        
        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")
if __name__ == "__main__":
    main()

display_menu()
    
 
