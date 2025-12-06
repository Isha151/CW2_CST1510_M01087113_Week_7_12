from openai import OpenAI
import streamlit as st


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


messages = [
    {"role": "system", "content": "You are a helpful Python assistant."},
    {"role": "user", "content": "Write an explanation of API for beginners."}
]

# Call OpenAI API
response = client.chat.completions.create(
    model = "gpt-4.1-mini",
    messages = messages
)

# Print the response
# Print(response.choices[0].message["content"])
print(response.choices[0].message.content)