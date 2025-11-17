import streamlit as st
import pandas as pd
st.title("1. Basic Page Elements")
st.write("`st.write` is very flexible – you can pass strings, numbers, dataframes, etc.")
st.caption("This is a caption!")
st.text("Plain fixed-width text for code-like things.")
st.markdown("You can use **Markdown** here, including *italic* and `code`.")

st.image(
    "https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png",
    caption="Streamlit logo",)