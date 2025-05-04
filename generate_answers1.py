# generate_answers.py

import requests

BASE_URL = "http://localhost:8000"

def generate_answer(question):
    try:
        response = requests.post(
            f"{BASE_URL}/generate",
            json={"new_message": {"role": "user", "content": question}}
        )
        if response.ok:
            return response.json().get("generated_text", "No response.")
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Exception: {e}"

def chat():
    print("RAG Chatbot is running. Type your question below.")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting chatbot.")
            break

        response = generate_answer(user_input)
        print(f"Bot: {response}\n")

if __name__ == "__main__":
    chat()
