import streamlit as st
from app.data.db import connect_database
from app.data.tickets import get_all_incidents as get_all_tickets, insert_ticket
import pandas as pd
import os, openai


conn = connect_database()  
df = get_all_tickets(conn)  

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.error("⛔ You must be logged in to view this page.")
    if st.button("Go to Login"):
        st.switch_page("Home.py")
    st.stop()

st.set_page_config(page_title="IT Support Tickets", layout="wide")

st.title("🛠️ IT Support Tickets Dashboard")



st.subheader("Ticket Stats")
c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Total Tickets", len(df))

with c2:
    open_count = df[df["status"] == "Open"].shape[0] if "status" in df else 0
    st.metric("Open Tickets", open_count)

with c3:
    closed_count = df[df["status"] == "Closed"].shape[0] if "status" in df else 0
    st.metric("Closed Tickets", closed_count)


st.subheader("Create New Ticket")

with st.expander("Add ticket"):
    with st.form("ticket_form"):
        title = st.text_input("Issue Title")
        priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        status = st.selectbox("Status", ["Open", "In Progress", "Closed"])

        submitted = st.form_submit_button("Submit Ticket")

        if submitted:
            insert_ticket(conn, title, priority, status)  # Inserts into it_tickets table
            st.success("Ticket submitted successfully!")
            st.experimental_rerun()


st.subheader("Ticket Records")
st.dataframe(df, use_container_width=True)


st.subheader("Chat with IT Ticket Assistant")

cols = df.columns.tolist() if not df.empty else []
default_system = (
    f"You are an IT support analysis assistant. "
    f"Your dataset columns include: {', '.join(cols)}. "
    f"Provide short, practical responses and suggest basic IT workflows when helpful."
)

system_prompt = st.text_area("System prompt", value=default_system, height=120)
user_q = st.text_input("Ask a question about the tickets")

if st.button("Ask"):
    api_key = (
        st.secrets.get("OPENAI_API_KEY", "")
        if "OPENAI_API_KEY" in st.secrets
        else os.environ.get("OPENAI_API_KEY", "")
    )

    if not api_key:
        st.error("OpenAI API key missing.")
    else:
        openai.api_key = api_key

        try:
            resp = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_q},
                ],
                max_tokens=300,
            )
            st.write(resp["choices"][0]["message"]["content"])
        except Exception as e:
            st.error(f"OpenAI API error: {e}")
