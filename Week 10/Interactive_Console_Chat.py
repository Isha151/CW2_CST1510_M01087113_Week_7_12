from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


print("ChatGPT Console Chat")
print("Type 'quit' to exit\n")

# Initialize messages list with system message
messages = [
    {"role": "system", "content": "You are a helpful assistant."}
]

print("ChatGPT with Memory. Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        print("Goodbye!")
        break
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": user_input}]
    )
    answer = response.choices[0].message.content
    print(f"AI: {answer}\n")
