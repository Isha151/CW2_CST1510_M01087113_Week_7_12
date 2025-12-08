import streamlit as st
import sys

st.set_page_config(page_title="Login / Register", page_icon="🔑", layout="centered")


sys.path.append(r"D:\MDX\CW2_CST1510_M01087113_Week_7_12\Week 8\app\services")


from app.services.user_service import login_user, register_user



if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""


st.title("🔐 Welcome")


if st.session_state.logged_in:
    st.success(f"✅ You are logged in as **{st.session_state.username}**.")
    if st.button("Go to Dashboard"):
        st.switch_page("pages/Cyber_Dashboard.py")
    
    st.stop()


tab_login, tab_register = st.tabs(["Login", "Register"])


with tab_login:
    st.subheader("Login")
    login_user_input = st.text_input("Username", key="login_user")
    login_pass_input = st.text_input("Password", type="password", key="login_pass")

    if st.button("Log in", type="primary"):
        
        success, msg = login_user(login_user_input, login_pass_input)
        
        if success:
            st.session_state.logged_in = True
            st.session_state.username = login_user_input
            st.success(msg)
            st.switch_page("pages/Cyber_Dashboard.py")
        else:
            st.error(msg)


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
                
                success, msg = register_user(reg_user, reg_pass, "user")
                
                if success:
                    st.success(msg)
                    st.info("Go to the Login tab to sign in.")
                else:
                    st.error(msg)
            
            except Exception as e:
                
                if "UNIQUE constraint failed" in str(e):
                    st.error(f"The username '{reg_user}' is already taken. Please choose another.")
                else:
                    st.error(f"An error occurred: {e}")