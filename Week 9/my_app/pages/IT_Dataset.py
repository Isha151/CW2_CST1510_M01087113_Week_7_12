import streamlit as st
import os, openai
import sys

sys.path.append(r"D:\MDX\CW2_CST1510_M01087113_Week_7_12\Week 8")


from app.data.db import connect_database
from app.data.tickets import insert_ticket, update_ticket, delete_ticket, get_all_tickets

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = "Username"


st.set_page_config(page_title="Datasets Metadata", layout="wide")
st.title("🛠️ IT Support Tickets Dashboard")
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
df = get_all_tickets(conn)  


if mode == "CRUD":


    st.subheader("Create New Ticket")
    with st.form("create_ticket"):
        subject = st.text_input("Subject")
        priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
        status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"])
        category = st.text_input("Category")
        description = st.text_area("Description")

        create_btn = st.form_submit_button("Create Ticket")
        if create_btn:
            insert_ticket(conn, subject, priority, status, category, description)
            st.success("Ticket created successfully!")



    st.subheader("Update Ticket Status / Priority")
    with st.form("update_ticket"):
        ticket_id = st.number_input("Ticket ID to update", min_value=1)
        new_status = st.selectbox("New Status", ["Open", "In Progress", "Resolved", "Closed"])
        new_priority = st.selectbox("New Priority", ["Low", "Medium", "High", "Critical"])

        update_btn = st.form_submit_button("Update Ticket")
        if update_btn:
            update_ticket(conn, ticket_id, new_status, new_priority)
            st.success("Ticket updated successfully!")



    st.subheader("Delete Ticket")
    with st.form("delete_ticket"):
        delete_id = st.number_input("Ticket ID to delete", min_value=1)

        delete_btn = st.form_submit_button("Delete Ticket")
        if delete_btn:
            delete_ticket(conn, delete_id)
            st.success("Ticket deleted successfully!")

if mode == "Analytics":

    st.subheader("Ticket Stats")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Total Tickets", len(df))

    with c2:
        open_count = df[df["status"] == "Open"].shape[0]
        st.metric("Open Tickets", open_count)

    with c3:
        closed_count = df[df["status"] == "Closed"].shape[0]
        st.metric("Closed Tickets", closed_count)


    st.subheader("Ticket Records")
    st.dataframe(df, use_container_width=True)



    import matplotlib.pyplot as plt

    st.subheader("Record Count by Category")
    fig1, ax1 = plt.subplots()
    df["category"].value_counts().plot(kind="bar", ax=ax1)
    st.pyplot(fig1)








if mode == "AI Chat":
    st.subheader("Ask AI")

    from openai import OpenAI
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


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
