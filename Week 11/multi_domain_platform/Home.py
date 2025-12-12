import streamlit as st
import sys

# Session States intitialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

if st.session_state.logged_in:
    st.success(f"✅ You are logged in as **{st.session_state.username}**.")
    if st.button("Go to Dashboard"):
        st.switch_page("pages/_Cybersecurity.py")
    
    st.stop()


# Page config + title
st.set_page_config(page_title="Login / Register", page_icon="🔑", layout="centered")
st.title("🔐 Welcome")


# Imports for services and models
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager


# Create services
db = DatabaseManager("database/platform.db")
auth = AuthManager(db)


# UI (Creates tabs for Login and Registration)
tab_login, tab_register = st.tabs(["Login", "Register"])


# Login tab functions
with tab_login:
    st.subheader("Login")

    username_input = st.text_input("Username", key="login_user")
    password_input = st.text_input("Password", type="password", key="login_pass")
    if st.button("Log in", type="primary"):
        
        user = auth.login_user(username_input, password_input)
        
        if user is None:
            st.error("Invalid username or password.")
        else:
            st.success("Login successful!")
            st.session_state.logged_in = True
            st.session_state.username = user.get_username()
            st.switch_page("pages/_Cybersecurity.py")


# Registration tab functions
with tab_register:
    st.subheader("Register")
    new_user = st.text_input("Choose Username", key="reg_user")
    new_pass = st.text_input("Choose Password", type="password", key="reg_pass")
    confirm_pass = st.text_input("Confirm Password", type="password", key="reg_confirm")

    if st.button("Register Account"):
        if new_pass != confirm_pass:
            st.error("Passwords do not match.")
        else:
            try:
                auth.register_user(new_user, new_pass, role="user")
                st.success("Account created successfully!")
                st.info("You can now log in from the Login tab.")
            except Exception as e:
                # username already exists
                if "UNIQUE constraint failed" in str(e):
                    st.error(f"The username '{new_user}' is already taken. Try another.")
                else:
                    st.error(f"An unexpected error occurred: {e}")