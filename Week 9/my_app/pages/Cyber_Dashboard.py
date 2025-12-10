import streamlit as st
import sys
from openai import OpenAI

sys.path.append(r"D:\MDX\CW2_CST1510_M01087113_Week_7_12\Week 8")

from app.data.db import connect_database
from app.data.incidents import insert_incident, update_incident_status, delete_incident, get_all_incidents

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = "Username"
    

st.set_page_config(page_title="Datasets Metadata", layout="wide")
st.title("📊 Cyber Incidents Dashboard")
st.write(f"Welcome, **{st.session_state.username}**")

# if not st.session_state.logged_in:
#     st.error("⛔ You must be logged in to view this page.")
#     if st.button("Go to Login"):
#         st.switch_page("Home.py")
#     st.stop()



mode = st.radio(
    "Choose an option:",
    ["CRUD", "Analytics", "AI Chat"],
    horizontal=True
)

conn = connect_database()
df = get_all_incidents(conn)



if mode == "CRUD":
    st.subheader("Create New Cyber Incident")
    with st.form("create_form"):
        date = st.text_input("Date (YYYY-MM-DD)")
        incident_type = st.text_input("Incident Type")
        severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
        status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"])
        description = st.text_area("Description")

        create_btn = st.form_submit_button("Insert")
        if create_btn:
            insert_incident(conn, date, incident_type, severity, status, description)
            st.success("Incident inserted successfully!")


    st.subheader("Update Incident Status")
    with st.form("update_form"):
        incident_id = st.number_input("Incident ID to Update", min_value=1)
        new_status = st.selectbox("New Status", ["Open", "In Progress", "Resolved", "Closed"])

        update_btn = st.form_submit_button("Update")
        if update_btn:
            update_incident_status(conn, incident_id, new_status)
            st.success("Incident updated successfully!")


    st.subheader("Delete Cyber Incident")
    with st.form("delete_form"):
        delete_id = st.number_input("Incident ID to Delete", min_value=1)

        delete_btn = st.form_submit_button("Delete")
        if delete_btn:
            delete_incident(conn, delete_id)
            st.success("Incident deleted successfully!")



if mode == "Analytics":
    st.subheader("Analytics")

    import pandas as pd
    import matplotlib.pyplot as plt


    conn = connect_database()
    df = get_all_incidents(conn)


    st.write("Record Count by Category")
    fig1, ax1 = plt.subplots()
    df['incident_type'].value_counts().plot(kind='bar', ax=ax1)
    st.pyplot(fig1)




if mode == "AI Chat":
    st.subheader("Ask AI")

    from openai import OpenAI
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    # Hidden system prompt (DON'T SHOW to user)
    system_prompt = "You are an AI assistant that gives explanations ONLY about Cyber Security incidents."

    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_input = st.chat_input("Ask something...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages
        )

        answer = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": answer})

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
