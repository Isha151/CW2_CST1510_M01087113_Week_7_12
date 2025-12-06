import streamlit as st
import sys
from pathlib import Path
from openai import OpenAI
import streamlit as st


st.set_page_config(page_title="Cyber Dashboard", page_icon="📊", layout="wide")


week8_path = Path(__file__).resolve().parent.parent.parent.parent / "Week 8"
sys.path.append(str(week8_path))


try:
    from app.data.db import connect_database
    from app.data.incidents import get_all_incidents, insert_incident
except ImportError:
    st.error("⚠️ Setup Error: Could not find Week 8 functions.")
    st.stop()


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.error("⛔ You must be logged in to view this page.")
    if st.button("Go to Login"):
        st.switch_page("Home.py")
    st.stop()


st.title("📊 Cyber Incidents Dashboard")
st.write(f"Welcome, **{st.session_state.username}**")


conn = connect_database() 


st.subheader("Recent Incidents")
try:
    df = get_all_incidents(conn)
    st.dataframe(df, use_container_width=True)
except Exception as e:
    st.error(f"Error reading data: {e}")


st.divider()
st.subheader("Report New Incident")

with st.form("new_incident_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        new_date = st.date_input("Date")
        new_title = st.text_input("Title/Description")
        new_type = st.selectbox("Type", ["Phishing", "Malware", "DDoS", "Ransomware"])
    
    with col2:
        new_severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
        new_status = st.selectbox("Status", ["Open", "In Progress", "Resolved"])
    
    submitted = st.form_submit_button("Submit Report")
    
    if submitted:
        insert_incident(
            conn, 
            str(new_date), 
            new_type, 
            new_severity, 
            new_status, 
            new_title, 
            st.session_state.username
        )
        st.success("✅ Incident reported successfully!")
        st.rerun()



if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.error("⛔ You must be logged in to view this page.")
    if st.button("Go to Login"):
        st.switch_page("Home.py")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# ═══════════════════════════════════════════════# STEP 1: Initialize session state for messages# ═══════════════════════════════════════════════if"messages"not in st.session_state:
st.session_state.messages = [
    {"role": "system", "content": "You are a helpful assistant."}
]

# ═══════════════════════════════════════════════# STEP 2: Display existing messages# ═══════════════════════════════════════════════for message in st.session_state.messages:
    # Skip system messages (don't show to user)if message["role"] != "system":
# with st.chat_message(message["role"]):
#     st.write(message["content"])

# ═══════════════════════════════════════════════# STEP 3: Handle user input# ═══════════════════════════════════════════════
user_input = st.chat_input("Type your message...")

if user_input:
    # Display user message immediatelywith st.chat_message("user"):
    st.write(user_input)
    
    # Add user message to session state
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    
    # ═══════════════════════════════════════════════# STEP 4: Get AI response# ═══════════════════════════════════════════════
response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=st.session_state.messages
    )
    
    # Extract AI message
ai_message = response.choices[0].message.content
    
    # Display AI responsewith st.chat_message("assistant"):
st.write(ai_message)
    
    # ═══════════════════════════════════════════════# STEP 5: Save AI response to session state# ═══════════════════════════════════════════════
st.session_state.messages.append(
        {"role": "assistant", "content": ai_message}
    )        


st.divider()
if st.button("Log Out"):
    st.session_state.logged_in = False
    st.switch_page("Home.py")