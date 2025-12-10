import streamlit as st
import pandas as pd
import sys

sys.path.append(r"D:\MDX\CW2_CST1510_M01087113_Week_7_12\Week 8")

from app.data.db import connect_database
from app.data.datasets import (
    insert_dataset,
    update_dataset,
    delete_dataset,
    get_all_datasets
)

st.set_page_config(page_title="Datasets Metadata", layout="wide")
st.title("📁 Datasets Metadata Dashboard")
st.write(f"Welcome, **{st.session_state.username}**")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = "Username"
 

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
df = get_all_datasets(conn)


if mode == "CRUD":
    st.subheader("Create New Dataset Record")
    with st.form("create_form"):
        dataset_name = st.text_input("Dataset Name")
        category = st.text_input("Category")
        source = st.text_input("Source")
        last_updated = st.text_input("Last Updated (YYYY-MM-DD)")
        record_count = st.number_input("Record Count", min_value=0)
        file_size = st.number_input("File Size (MB)", min_value=0.0)
        create_btn = st.form_submit_button("Insert")

        if create_btn:
            insert_dataset(conn, dataset_name, category, source, last_updated, record_count, file_size)
            st.success("Dataset inserted successfully!")

    st.subheader("Update Dataset Record")
    with st.form("update_form"):
        dataset_id = st.number_input("Dataset ID", min_value=1)
        dataset_name = st.text_input("New Dataset Name")
        category = st.text_input("New Category")
        source = st.text_input("New Source")
        last_updated = st.text_input("New Last Updated")
        record_count = st.number_input("New Record Count", min_value=0)
        file_size = st.number_input("New File Size", min_value=0.0)
        update_btn = st.form_submit_button("Update")

        if update_btn:
            update_dataset(conn, dataset_id, dataset_name, category, source,
                           last_updated, record_count, file_size)
            st.success("Dataset updated successfully!")

    st.subheader("Delete Dataset Record")
    with st.form("delete_form"):
        delete_id = st.number_input("Dataset ID to delete", min_value=1)
        delete_btn = st.form_submit_button("Delete")

        if delete_btn:
            delete_dataset(conn, delete_id)
            st.success("Dataset deleted successfully!")


if mode == "Analytics":
    st.subheader("Analytics")

    st.write("Record Count by Category")
    fig1 = df["category"].value_counts().plot(kind="bar").get_figure()
    st.pyplot(fig1)



if mode == "AI Chat":
    st.subheader("Ask AI about your datasets")

    from openai import OpenAI
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    system_prompt = "You are an AI assistant that explains dataset metadata and simple data science concepts."

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
