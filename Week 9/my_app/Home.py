import streamlit as st
import sys
from pathlib import Path

# --- 1. PAGE CONFIG (Must be first) ---
st.set_page_config(page_title="Login / Register", page_icon="🔑", layout="centered")

# --- 2. PATH SETUP (The Bridge) ---
# Go up 3 levels: Home.py -> my_app -> Week 9 -> PROJECT_ROOT
week8_path = Path(__file__).resolve().parent.parent.parent / "Week 8"
sys.path.append(str(week8_path))

# --- 3. IMPORTS ---
try:
    from app.services.user_service import login_user, register_user
except ImportError:
    st.error(f"⚠️ Error: Could not find Week 8 code. Python looked in: {week8_path}")
    st.stop()

# --- 4. SESSION STATE SETUP ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# --- 5. MAIN UI ---
st.title("🔐 Welcome")

# If already logged in, offer to go to dashboard
if st.session_state.logged_in:
    st.success(f"✅ You are logged in as **{st.session_state.username}**.")
    if st.button("Go to Dashboard"):
        st.switch_page("pages/1_Dashboard.py")
    # Stop here so we don't show the login form again
    st.stop()

# Tabs
tab_login, tab_register = st.tabs(["Login", "Register"])

# LOGIN TAB
with tab_login:
    st.subheader("Login")
    login_user_input = st.text_input("Username", key="login_user")
    login_pass_input = st.text_input("Password", type="password", key="login_pass")

    if st.button("Log in", type="primary"):
        # Call the REAL Week 8 function
        success, msg = login_user(login_user_input, login_pass_input)
        
        if success:
            st.session_state.logged_in = True
            st.session_state.username = login_user_input
            st.success(msg)
            st.switch_page("pages/1_Dashboard.py")
        else:
            st.error(msg)

# REGISTER TAB
with tab_register:
    st.subheader("Register")
    reg_user = st.text_input("Choose Username", key="reg_user")
    reg_pass = st.text_input("Choose Password", type="password", key="reg_pass")
    reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")

    if st.button("Create Account"):
        if reg_pass != reg_confirm:
            st.error("Passwords do not match.")
        else:
            try:
                # Try to register
                success, msg = register_user(reg_user, reg_pass, "user")
                
                if success:
                    st.success(msg)
                    st.info("Go to the Login tab to sign in.")
                else:
                    st.error(msg)
            
            except Exception as e:
                # If the database complains (like Unique Constraint failed), catch it here
                if "UNIQUE constraint failed" in str(e):
                    st.error(f"The username '{reg_user}' is already taken. Please choose another.")
                else:
                    st.error(f"An error occurred: {e}")