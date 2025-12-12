import streamlit as st
import uuid
import pandas as pd


# Session States intitialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = "Username"

if not st.session_state.logged_in:
    st.error("You must be logged in to view this page.")
    if st.button("Go to Login"):
        st.switch_page("Home.py")
    st.stop()


# AI chat history for THIS page only
if "ai_messages_tickets" not in st.session_state:
    st.session_state["ai_messages_tickets"] = [
        {"role": "system", "content": "You explain datasets and statistics."}
    ]


# Page config + title
st.set_page_config(page_title="Datasets Metadata", layout="wide")
st.title("🛠️ IT Support Tickets Dashboard")
st.write(f"Welcome, **{st.session_state.username}**")


# Side bar logout button
with st.sidebar:

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.switch_page("Home.py")


# Imports for services and models
from services.database_manager import DatabaseManager
from services.ticket_service import TicketService
from models.it_ticket import ITTicket
from services.ai_assistant import AIAssistant


# Create services
db = DatabaseManager("database/platform.db")
ticket_service = TicketService(db)
ai = AIAssistant(session_key="ai_messages_tickets",
                 system_prompt="You help with IT ticket analysis.")



# UI control (Radio Buttons)
mode = st.radio(
    "Choose an option:",
    ["CRUD", "Analytics", "AI Chat"],
    horizontal=True
)


# Load all tickets once
tickets = ticket_service.get_all()


# CRUD Functions mode
if mode == "CRUD":


    st.subheader("Create New Ticket")
    with st.form("create_ticket"):
        subject = st.text_input("Subject")
        priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
        status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"])
        category = st.text_input("Category")
        description = st.text_area("Description")

        submit = st.form_submit_button("Create Ticket")

        if submit:
            # Create unique ticket ID
            ticket_id = str(uuid.uuid4())[:8]

            ticket = ITTicket(
                db_id=None,
                ticket_id=ticket_id,
                subject=subject,
                priority=priority,
                status=status,
                category=category,
                description=description
            )

            ticket_service.create(ticket)
            st.success(f"Ticket created! ID: {ticket_id}")


    st.subheader("Update Ticket Status / Priority")

    with st.form("update_ticket"):
        ticket_db_id = st.number_input("Database Ticket ID", min_value=1)
        new_priority = st.selectbox("New Priority", ["Low", "Medium", "High", "Critical"])
        new_status = st.selectbox("New Status", ["Open", "In Progress", "Resolved", "Closed"])
        new_category = st.text_input("New Category")
        new_subject = st.text_input("New Subject")
        new_description = st.text_area("New Description")
        assigned_to = st.text_input("Assigned To (Optional)")
        resolved_date = st.text_input("Resolved Date (YYYY-MM-DD) (Optional)")

        update_btn = st.form_submit_button("Update Ticket")

        if update_btn:
            ticket = ITTicket(
                db_id=ticket_db_id,
                ticket_id="dummy",  # NOT updated — DB keeps original
                subject=new_subject,
                priority=new_priority,
                status=new_status,
                category=new_category,
                description=new_description,
                assigned_to=assigned_to,
                resolved_date=resolved_date
            )

            ticket_service.update(ticket)
            st.success("Ticket updated!")


    st.subheader("Delete Ticket")


    with st.form("delete_ticket"):
        delete_id = st.number_input("Database Ticket ID to Delete", min_value=1)
        delete_btn = st.form_submit_button("Delete Ticket")

        if delete_btn:
            ticket_service.delete(delete_id)
            st.success("Ticket deleted successfully.")


# Analytics Funtion mode
elif mode == "Analytics":

    st.subheader("IT Ticket Analytics")

    # Convert tickets to DataFrame
    df = pd.DataFrame([{
        "priority": t.priority,
        "status": t.status,
        "category": t.category
    } for t in tickets])


    # Key Metrics info
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Tickets", len(df))
    col2.metric("Open Tickets", (df["status"] == "Open").sum())
    col3.metric("Closed Tickets", (df["status"] == "Closed").sum())

    st.divider()


    # Tickets by Priority chart
    st.subheader("Tickets by Priority")
    priority_counts = df["priority"].value_counts()
    st.bar_chart(priority_counts)


    # Tickets by Status chart
    st.subheader("Tickets by Status")
    status_counts = df["status"].value_counts()
    st.bar_chart(status_counts)

 
    # Tickets by Category chart
    st.subheader("Tickets by Category")
    category_counts = df["category"].value_counts()
    st.bar_chart(category_counts)

    # Raw Data 
    st.subheader("Ticket Records")
    st.dataframe(df, use_container_width=True)



# AI Chat Funtion Mode
elif mode == "AI Chat":
    st.subheader("Chat with AI Assistant")

    # Show message history
    for msg in st.session_state["ai_messages_tickets"]:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    # Handle new messages
    user_input = st.chat_input("Ask about IT Tickets...")

    if user_input:
        with st.chat_message("user"):
            st.write(user_input)

        reply = ai.send_message(user_input)

        with st.chat_message("assistant"):
            st.write(reply)