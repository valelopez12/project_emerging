from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from ragas.evaluation import evaluate
from datasets import Dataset
import requests

# Sample evaluation set: questions with expected answers
evaluation_data = [
    {
        "question": "What is the capital of France?",
        "ground_truth": "Paris"
    },
    {
        "question": "Who created the Python language?",
        "ground_truth": "Guido van Rossum"
    },
    {
        "question": "Who wrote Don Quixote?",
        "ground_truth": "Miguel de Cervantes"
    }
]

def fetch_answer(question: str) -> str:
    response = requests.post(
        "http://localhost:8000/generate",
        json={"new_message": {"role": "user", "content": question}}
    )
    if response.ok:
        return response.json().get("generated_text", "")
    return ""

def fetch_context(question: str) -> str:
    # If your API provides retrieved context, add it here.
    # For now, return None or a dummy.
    return "Context not available."

def prepare_dataset():
    questions = []
    answers = []
    contexts = []
    ground_truths = []

    for item in evaluation_data:
        q = item["question"]
        print(f"Asking: {q}")
        a = fetch_answer(q)
        ctx = fetch_context(q) 
        questions.append(q)
        answers.append(a)
        contexts.append([ctx]) 
        ground_truths.append(item["ground_truth"])

    data = {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths
    }

    return Dataset.from_dict(data)

if __name__ == "__main__":
    rag_dataset = prepare_dataset()

    print("\nEvaluating...\n")
    results = evaluate(
        rag_dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
        ]
    )

    print("\n Evaluation Results:")
    print(results.to_pandas())
