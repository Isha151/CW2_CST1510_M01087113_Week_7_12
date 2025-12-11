from openai import OpenAI
import streamlit as st

class AIAssistant:
    """Simple chat assistant using OpenAI + Streamlit-style chat history."""

    def __init__(self, session_key: str, system_prompt: str = "You are a helpful assistant."):
        self.client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        self.system_prompt = system_prompt
        self.session_key = session_key  # ← UNIQUE PER PAGE

        # Initialize session state messages if not present
        if "ai_messages" not in st.session_state:
            st.session_state.ai_messages = [
                {"role": "system", "content": self.system_prompt}
            ]

    def send_message(self, user_input: str) -> str:
        """
        Adds the user message, sends to OpenAI,
        stores assistant response, and returns the assistant message.
        """

        # Add user message to history
        st.session_state.ai_messages.append({
            "role": "user",
            "content": user_input
        })

        # Send to OpenAI
        response = self.client.chat.completions.create(
            model="gpt-5-nano",
            messages=st.session_state.ai_messages
        )

        ai_message = response.choices[0].message.content

        # Save assistant reply
        st.session_state.ai_messages.append({
            "role": "assistant",
            "content": ai_message
        })

        return ai_message

    def clear_history(self):
        """Resets conversation while keeping system prompt."""
        st.session_state.ai_messages = [
            {"role": "system", "content": self.system_prompt}
        ]