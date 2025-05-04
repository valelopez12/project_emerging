# generate_answers.py

import requests
import json

# List of questions you'd like to ask the RAG system
questions = [
    "What is the capital of France?",
    "Who created the Python language?",
    "Who wrote Don Quixote?",
    "What is retrieval-augmented generation?",
    "What is the use of FastAPI in RAG systems?"
]

# RAG API URL
BASE_URL = "http://localhost:8000"

# Output file
OUTPUT_FILE = "answers.json"

def generate_answer(question):
    response = requests.post(
        f"{BASE_URL}/generate",
        json={"new_message": {"role": "user", "content": question}}
    )
    if response.ok:
        return response.json().get("generated_text", "")
    else:
        print(f"Error generating answer for: {question}")
        print(response.text)
        return ""

def main():
    results = []

    for question in questions:
        print(f"Asking: {question}")
        answer = generate_answer(question)
        print(f"Answer: {answer}\n")
        results.append({"question": question, "answer": answer})

    # Save results to JSON
    with open(OUTPUT_FILE, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n Answers saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
