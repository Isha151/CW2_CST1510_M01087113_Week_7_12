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
    st.session_state["ai_messages_datasets"] = [
        {"role": "system", "content": "You explain datasets and statistics."}
    ]


# Page config + title
st.set_page_config(page_title="Datasets Metadata", layout="wide")
st.title("📁 Datasets Metadata Dashboard")
st.write(f"Welcome, **{st.session_state.username}**")


# Side bar logout button
with st.sidebar:

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.switch_page("Home.py")


# Imports for services and models  
from services.database_manager import DatabaseManager
from services.dataset_service import DatasetService
from models.dataset import Dataset
from services.ai_assistant import AIAssistant


# Create services
db = DatabaseManager("database/platform.db")
dataset_service = DatasetService(db)
ai = AIAssistant(session_key="ai_messages_datasets",
                 system_prompt="You explain datasets and statistics.")


# UI control (Radio Buttons)
mode = st.radio(
    "Choose an option:",
    ["CRUD", "Analytics", "AI Chat"],
    horizontal=True
)


# Load all tickets once
datasets = dataset_service.get_all()


# CRUD Functions mode
if mode == "CRUD":
    st.subheader("Create New Dataset Record")
    with st.form("create_form"):
        name = st.text_input("Dataset Name")
        category = st.text_input("Category")
        source = st.text_input("Source")
        last_updated = st.text_input("Last Updated (YYYY-MM-DD)")
        record_count = st.number_input("Record Count", min_value=0)
        file_size = st.number_input("File Size (MB)", min_value=0.0)

        submit = st.form_submit_button("Insert")

        if submit:
            dataset = Dataset(
                dataset_id=None,
                dataset_name=name,
                category=category,
                source=source,
                last_updated=last_updated,
                record_count=record_count,
                file_size_mb=file_size
            )
            dataset_service.create(dataset)
            st.success("Dataset inserted successfully!")

    st.subheader("Update Dataset Record")

    with st.form("update_form"):
        dataset_id = st.number_input("Dataset ID to Update", min_value=1)
        name = st.text_input("New Dataset Name")
        category = st.text_input("New Category")
        source = st.text_input("New Source")
        last_updated = st.text_input("New Last Updated")
        record_count = st.number_input("New Record Count", min_value=0)
        file_size = st.number_input("New File Size", min_value=0.0)

        update_btn = st.form_submit_button("Update")

        if update_btn:
            updated_dataset = Dataset(
                dataset_id=dataset_id,
                dataset_name=name,
                category=category,
                source=source,
                last_updated=last_updated,
                record_count=record_count,
                file_size_mb=file_size
            )
            dataset_service.update(updated_dataset)
            st.success("Dataset updated successfully!")


    st.subheader("Delete Dataset Record")
    with st.form("delete_form"):
        delete_id = st.number_input("Dataset ID to delete", min_value=1)
        delete_btn = st.form_submit_button("Delete")

        if delete_btn:
            dataset_service.delete(delete_id)
            st.success("Dataset deleted successfully!")


# Analytics Funtion mode
elif mode == "Analytics":
    st.subheader("Analytics")

    df = pd.DataFrame([d.to_dict() for d in datasets])

    st.write("Record Count by Category")
    fig1 = df["category"].value_counts().plot(kind="bar").get_figure()
    st.pyplot(fig1)


# AI Chat Funtion Mode
elif mode == "AI Chat":
    st.subheader("Chat with AI Assistant")

    # Show message history
    for msg in st.session_state["ai_messages_datasets"]:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    # Handle new messages
    user_input = st.chat_input("Ask about Datasets...")

    if user_input:
        with st.chat_message("user"):
            st.write(user_input)

        reply = ai.send_message(user_input)

        with st.chat_message("assistant"):
            st.write(reply)