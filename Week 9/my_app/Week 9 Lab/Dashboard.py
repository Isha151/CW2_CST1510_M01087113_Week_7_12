import streamlit as st
import pandas as pd

st.set_page_config(layout='wide')
st.title("Sales Dashboard")

# Sidebar filters
with st.sidebar:
    year = st.selectbox("year", [2023, 2024, 2025])
    min_revenue = st.slider("Min revenue", 0, 100000, 20000)

df = pd.DataFrame(
    {
        "year": [2023, 2023, 2023, 2024, 2024, 2024, 2025, 2025],
        "region": ["North", "South", "East", "North", "South", "East", "North", "South"],
        "revenue": [30000, 50000, 20000, 45000, 60000, 35000, 55000, 80000]
    }
)

# Apply filters to data
filtered = df[(df["year"] ==year) & (df["revenue"] >= min_revenue)]

#layout witj columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("revenue by Region")
    st.bar_chart(filtered)

with col2:
    st.subheader("Revenue Distribution")
    st.bar_chart(filtered)

# Expandable data table
with st.expander("See filtered data"):
    st.dataframe(filtered)