import json
import os
import openai
import ast
from datasets import Dataset
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from ragas import evaluate
from dotenv import load_dotenv, find_dotenv
import pandas as pd
from core.recommender import Recommender
import argparse

load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")

recommender = Recommender(collection_name="test_videos")

def calculate_video_accuracy(llm_response_str: str, chroma_results: dict, expected_ids: list) -> float:
    """
    Calculates video accuracy by extracting recommended video titles from the LLM's
    natural language response and mapping them back to video_ids from the chroma results.
    """
    if not chroma_results.get('metadatas') or not chroma_results['metadatas'][0]:
        return 0.0

    title_to_id_map = {
        meta['video_title']: meta['video_id']
        for meta in chroma_results['metadatas'][0]
    }
    
    recommended_ids = set()
    for title, video_id in title_to_id_map.items():
        if title in llm_response_str:
            recommended_ids.add(video_id)

    expected_ids_set = set(expected_ids)
    
    if not expected_ids_set:
        return 1.0 if not recommended_ids else 0.0
    
    matching_ids = recommended_ids.intersection(expected_ids_set)
    accuracy = len(matching_ids) / len(expected_ids_set)
    
    return accuracy

test_cases = [
    {
        "question": "I'm a complete beginner in programming. What is Python and what is it used for?",
        "user_preferences": "18 years old, high school education level, interested in learning programming, job: student",
        "ground_truth": "Python is a high-level, interpreted programming language known for its readability and beginner-friendly syntax. It is a general-purpose language used in web development, data science, machine learning, scripting, and automation.",
        "expected_video_ids": ["test_video_1"]
    },
    {
        "question": "I have some programming experience and I want to learn about object-oriented programming in Python. Can you explain what a class is?",
        "user_preferences": "25 years old, bachelor's degree in computer science, interested in software development, job: junior software developer",
        "ground_truth": "A class in Python is a blueprint for creating objects. An object is an instance of a class, and it can contain data (attributes) and code (methods). The __init__ method is a special method, the constructor, used to initialize the object's attributes.",
        "expected_video_ids": ["test_video_2", "test_video_3", "test_video_6"]
    },
    {
        "question": "I'm an experienced developer and I'm interested in advanced Python concepts. I have heard about metaclasses and related concept?",
        "user_preferences": "35 years old, master's degree in computer science, interested in advanced Python and metaprogramming, job: senior software engineer",
        "ground_truth": "A metaclass is the class of a class. It defines how a class is created. The default metaclass in Python is `type`. You can create your own metaclasses to modify classes at creation time, for tasks like registering classes or enforcing coding standards.",
        "expected_video_ids": ["test_video_3", "test_video_2"]
    },
    {
        "question": "How can I get started with web development in Python? I've heard of Django.",
        "user_preferences": "22 years old, university student, interested in web development, job: intern",
        "ground_truth": "To start with Django, you first need to install it using pip (`pip install Django`). Then, you can create a new project with `django-admin startproject myproject`. A Django project is made of apps, and the core components of an app are models (for database structure), views (for handling requests), and templates (for rendering HTML).",
        "expected_video_ids": ["test_video_7", "test_video_10"]
    },
    {
        "question": "I need to analyze some data. Which Python libraries are best for that?",
        "user_preferences": "30 years old, data analyst, interested in data science libraries",
        "ground_truth": "For data analysis in Python, the most essential libraries are NumPy and Pandas. NumPy is used for numerical operations and provides the efficient `ndarray` object. Pandas is built on NumPy and is used for working with structured, tabular data through its `DataFrame` object.",
        "expected_video_ids": ["test_video_6"]
    },
    {
        "question": "Hi i want to learn about data science and pandas because i wanto to analyze data about the stock market. The problem is that i don't know which libraries are best for that. Please recommend me videos about that and how to use them. Also i want to learn how to test in python in general",
        "user_preferences": "30 years old, data analyst, interested in data science libraries",
        "ground_truth": "For data analysis in Python, the most essential libraries are NumPy and Pandas. NumPy is used for numerical operations and provides the efficient `ndarray` object. Pandas is built on NumPy and is used for working with structured, tabular data through its `DataFrame` object. For testing, Pytest is the most popular testing framework so you should use it.",
        "expected_video_ids": ["test_video_6", "test_video_8"]
    }
]

def run_evaluation(query_rewriting=False, re_ranking=False):
    
    questions = []
    answers = []
    ground_truths = []
    retrieved_contexts = []
    video_accuracy_scores = []

    for case in test_cases:
        print(f"Running test case: {case['question']}")
        
        response = recommender.recommend_testing(case["question"], case["user_preferences"], query_rewriting, re_ranking)
        
        llm_response = response["llm_response"]
        chroma_results = response["chroma_results"]
        contexts = chroma_results['documents'][0] if chroma_results.get('documents') else []
        
        questions.append(case["question"])
        answers.append(str(llm_response))
        ground_truths.append(case["ground_truth"])
        retrieved_contexts.append(contexts)
        
        accuracy = calculate_video_accuracy(str(llm_response), chroma_results, case["expected_video_ids"])
        video_accuracy_scores.append(accuracy)

    data_samples = {
        'question': questions,
        'answer': answers,
        'ground_truth': ground_truths,
        'contexts': retrieved_contexts,
    }
    dataset = Dataset.from_dict(data_samples)

    print(video_accuracy_scores)
    score = evaluate(
        dataset, 
        metrics=[
            answer_relevancy,
            context_precision,
            context_recall 
        ],
        raise_exceptions=False
    )
    
    df = score.to_pandas()
    df['video_accuracy'] = video_accuracy_scores
    
    # Print a clean summary of the metrics
    print("\n--- Evaluation Metrics Summary ---")
    print('(query rewriting: ', query_rewriting, ', re-ranking: ', re_ranking, ')')
    metrics_df = df[['answer_relevancy', 'context_precision', 'context_recall', 'video_accuracy']]
    print(metrics_df)
    print("------------------------------------")
    print(metrics_df.mean())
    print("------------------------------------")
    
    df.to_csv("rag_evaluation_results.csv", index=False)
    print("Evaluation complete. Results saved to rag_evaluation_results.csv")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Run RAG evaluation')
    parser.add_argument('--query-rewriting', action='store_true', help='Enable query rewriting')
    parser.add_argument('--re-ranking', action='store_true', help='Enable re-ranking')
    args = parser.parse_args()
    run_evaluation(query_rewriting=args.query_rewriting, re_ranking=args.re_ranking)
