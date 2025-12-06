import streamlit as st
from app.data.db import connect_database
from app.data.datasets import get_all_datasets, insert_dataset
import pandas as pd
import os, openai



# --- Access Control ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.error("You must be logged in to view this page.")
    st.stop()

st.set_page_config(page_title="Datasets Metadata", layout="wide")

st.title("📁 Datasets Metadata Dashboard")

conn = connect_database()
df = get_all_datasets(conn)

# --- Upload CSV ---
st.subheader("Upload Metadata CSV")

uploaded = st.file_uploader("Upload datasets_metadata.csv", type=["csv"])

if uploaded:
    csv_df = pd.read_csv(uploaded)
    st.dataframe(csv_df, use_container_width=True)

    if st.button("Import CSV to Database"):
        for _, row in csv_df.iterrows():
            insert_dataset(
                conn,
                row.get("dataset_name", ""),
                row.get("description", ""),
                row.get("records", 0),
            )
        st.success("CSV imported to database.")
        st.experimental_rerun()

# --- Display existing data ---
st.subheader("Metadata Records")

df = get_all_datasets(conn)
st.dataframe(df, use_container_width=True)

# --- Chatbot ---
st.subheader("Chat with Metadata Assistant")

cols = df.columns.tolist() if not df.empty else []
default_system = (
    f"You are a data governance assistant. "
    f"You help summarize dataset metadata. "
    f"Available fields: {', '.join(cols)}."
)

system_prompt = st.text_area("System prompt", value=default_system, height=120)
user_q = st.text_input("Ask me anything about the metadata")

if st.button("Ask"):
    api_key = (
        st.secrets.get("OPENAI_API_KEY", "")
        if "OPENAI_API_KEY" in st.secrets
        else os.environ.get("OPENAI_API_KEY", "")
    )

    if not api_key:
        st.error("API key missing!")
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
