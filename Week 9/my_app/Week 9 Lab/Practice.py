import streamlit as st
import pandas as pd

st.set_page_config(page_title='My App', layout='centered')

name = st.text_input("Name")
if st.button("Submit"):
    if name:
        st.success(f'Hello, {name}!')
    else:
        st.warning("Enter name")


with st.sidebar:
    st.header("Controls")
    option = st.selectbox("Choose", ["A", "B", "C"])

col1, col2 = st.columns(2)

with col1:
    st.subheader("left")

with col2:
    st.subheader("Right")


with st.expander("see details"):
    st.write("Hidden content")
    