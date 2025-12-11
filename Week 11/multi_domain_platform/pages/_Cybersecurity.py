import streamlit as st
import pandas as pd



# Session States Initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = "Username"
    
# if not st.session_state.logged_in:
#     st.error("⛔ You must be logged in to view this page.")
#     if st.button("Go to Login"):
#         st.switch_page("Home.py")
#     st.stop()


# AI chat history for THIS page only
if "ai_messages_datasets" not in st.session_state:
    st.session_state["ai_messages_cyber"] = [
        {"role": "system", "content": "You explain datasets and statistics."}
    ]


# Page config + title
st.set_page_config(page_title="Datasets Metadata", layout="wide")
st.title("📊 Cyber Incidents Dashboard")
st.write(f"Welcome, **{st.session_state.username}**")


# Side bar logout button
with st.sidebar:

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.switch_page("Home.py")


# Imports for services and models
from services.database_manager import DatabaseManager
from services.incident_service import IncidentService
from models.security_incident import SecurityIncident
from services.ai_assistant import AIAssistant


# Create services
db = DatabaseManager("database/platform.db")
incident_service = IncidentService(db)
ai = AIAssistant(session_key="ai_messages_cyber",
                 system_prompt="You explain cybersecurity incidents.")


# UI control (Radio Buttons)
mode = st.radio(
    "Choose an option:",
    ["CRUD", "Analytics", "AI Chat"],
    horizontal=True
)


# Load all tickets once
incidents = incident_service.get_all()


# CRUD Functions mode
if mode == "CRUD":
    st.subheader("Create New Cyber Incident")
    with st.form("create_form"):
        date = st.text_input("Date (YYYY-MM-DD)")
        incident_type = st.text_input("Incident Type")
        severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
        status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"])
        description = st.text_area("Description")
        reported_by = st.text_input("Reported By (optional)")

        create_btn = st.form_submit_button("Insert")

        if create_btn:
            incident = SecurityIncident(
                incident_id=None,
                date=date,
                incident_type=incident_type,
                severity=severity,
                status=status,
                description=description,
                reported_by=reported_by
            )
            incident_service.create(incident)
            st.success("Incident inserted successfully!")

    st.subheader("Update Incident Status")

    with st.form("update_form"):
        incident_id = st.number_input("Incident ID", min_value=1)
        new_status = st.selectbox("New Status", ["Open", "In Progress", "Resolved", "Closed"])
        update_btn = st.form_submit_button("Update")

        if update_btn:
            incident_service.update_status(incident_id, new_status)
            st.success("Status updated!")


    st.subheader("Delete Cyber Incident")

    with st.form("delete_form"):
        delete_id = st.number_input("Incident ID to Delete", min_value=1)
        delete_btn = st.form_submit_button("Delete")

        if delete_btn:
            incident_service.delete(delete_id)
            st.success("Incident deleted.")



# Analytics Funtion mode
elif mode == "Analytics":
    st.subheader("Analytics")

    import matplotlib.pyplot as plt

    df = pd.DataFrame([{
        "id": i.id,
        "date": i.date,
        "incident_type": i.incident_type,
        "severity": i.severity,
        "status": i.status,
        "reported_by": i.reported_by
    } for i in incidents])


    st.write("Record Count by Category")
    fig1, ax1 = plt.subplots()
    df['incident_type'].value_counts().plot(kind='bar', ax=ax1)
    st.pyplot(fig1)



# AI Chat Funtion Mode
elif mode == "AI Chat":
    st.subheader("Chat with AI Assistant")

    # Show message history
    for msg in st.session_state["ai_messages_cyber"]:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    # Handle new messages
    user_input = st.chat_input("Ask about cyber incidents...")

    if user_input:
        with st.chat_message("user"):
            st.write(user_input)

        reply = ai.send_message(user_input)

        with st.chat_message("assistant"):
            st.write(reply)