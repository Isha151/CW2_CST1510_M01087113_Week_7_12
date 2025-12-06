from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# ═══════════════════════════════════════════════# STEP 1: Initialize session state for messages# ═══════════════════════════════════════════════if"messages"not in st.session_state:
st.session_state.messages = [
    {"role": "system", "content": "You are a helpful assistant."}
]

# ═══════════════════════════════════════════════# STEP 2: Display existing messages# ═══════════════════════════════════════════════for message in st.session_state.messages:
    # Skip system messages (don't show to user)if message["role"] != "system":
# with st.chat_message(message["role"]):
#     st.write(message["content"])

# ═══════════════════════════════════════════════# STEP 3: Handle user input# ═══════════════════════════════════════════════
user_input = st.chat_input("Type your message...")

if user_input:
    # Display user message immediatelywith st.chat_message("user"):
    st.write(user_input)
    
    # Add user message to session state
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    
    # ═══════════════════════════════════════════════# STEP 4: Get AI response# ═══════════════════════════════════════════════
response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=st.session_state.messages
    )
    
    # Extract AI message
ai_message = response.choices[0].message.content
    
    # Display AI responsewith st.chat_message("assistant"):
st.write(ai_message)
    
    # ═══════════════════════════════════════════════# STEP 5: Save AI response to session state# ═══════════════════════════════════════════════
st.session_state.messages.append(
        {"role": "assistant", "content": ai_message}
    )