import streamlit as st

st.title("This is my widget interface!")

st.header("Buttons and text input")
name = st.text_input("What is your name? ")
if st.button("Say hello"):
    if name:
        st.success(f"Hello {name}")
    else:
        st.warning("Please enter your name fist!")

st.divider()

st.header("Numeric inputs: ")
age = st.number_input("Enter your age", min_value=0, max_value=120, value=25)
st.write("You entered: ", age)

st.header("Images")
st.write("You can show images from a URL or local file.")
st.image(
    "https://petapixel.com/assets/uploads/2024/01/High-resolution-image-of-sun-1536x806.jpg",
    caption="Sun",)

st.divider()

st.slider("Pick a value", min_value=0, max_value=100, value=50, step=10, key="slider_example")

