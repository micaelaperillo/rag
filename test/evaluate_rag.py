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
        "expected_video_ids": ["test_video_1"]
    },
    {
        "question": "I have some programming experience and I want to learn about object-oriented programming in Python. Can you explain what a class is?",
        "user_preferences": "25 years old, bachelor's degree in computer science, interested in software development, job: junior software developer",
        "expected_video_ids": ["test_video_2", "test_video_3", "test_video_6"]
    },
    {
        "question": "I'm an experienced developer and I'm interested in advanced Python concepts. I have heard about metaclasses and related concept?",
        "user_preferences": "35 years old, master's degree in computer science, interested in advanced Python and metaprogramming, job: senior software engineer",
        "expected_video_ids": ["test_video_3", "test_video_2"]
    },
    {
        "question": "How can I get started with web development in Python? I've heard of Django.",
        "user_preferences": "22 years old, university student, interested in web development, job: intern",
        "expected_video_ids": ["test_video_7", "test_video_10"]
    },
    {
        "question": "I need to analyze some data. Which Python libraries are best for that?",
        "user_preferences": "30 years old, data analyst, interested in data science libraries",
        "expected_video_ids": ["test_video_6"]
    },
    {
        "question": "Hi i want to learn about data science and pandas because i wanto to analyze data about the stock market. The problem is that i don't know which libraries are best for that. Please recommend me videos about that and how to use them. Also i want to learn how to test in python in general",
        "user_preferences": "30 years old, data analyst, interested in data science libraries",
        "expected_video_ids": ["test_video_6", "test_video_8"]
    },
    {
        "question": "I want to start learning to code, what's a good language? I've heard about Python and Java.",
        "user_preferences": "19 years old, college student, no programming experience.",
        "expected_video_ids": ["test_video_1", "test_video_11"]
    },
    {
        "question": "hey uhm i need to build a backend for my app, someone said spring boot is good? wuts that? is it java?",
        "user_preferences": "28 years old, frontend developer, some experience with APIs.",
        "expected_video_ids": ["test_video_15"]
    },
    {
        "question": "My code is slow when I process a lot of data. How can I make it faster? Maybe use multiple threads? I'm using Java.",
        "user_preferences": "32 years old, software engineer, working on data processing applications.",
        "expected_video_ids": ["test_video_14", "test_video_18"]
    },
    {
        "question": "I'm learning about oop. what's the difference between a class and an object in java?",
        "user_preferences": "21 years old, computer science student.",
        "expected_video_ids": ["test_video_12"]
    },
    {
        "question": "How do I handle lists of things in Java? like arrays but more flexible. also i need to store key-value pairs. show me some vids thx",
        "user_preferences": "24 years old, junior developer.",
        "expected_video_ids": ["test_video_13", "test_video_17"]
    }
]

def run_evaluation(query_rewriting=False, re_ranking=False):
    
    questions = []
    answers = []
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
        retrieved_contexts.append(contexts)
        
        accuracy = calculate_video_accuracy(str(llm_response), chroma_results, case["expected_video_ids"])
        video_accuracy_scores.append(accuracy)

    data_samples = {
        'question': questions,
        'answer': answers,
        'contexts': retrieved_contexts,
    }
    dataset = Dataset.from_dict(data_samples)

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
    
    metrics_df = df[['answer_relevancy', 'context_precision', 'video_accuracy']]
    
    return metrics_df.mean()


if __name__ == "__main__":
    
    results = []
    
    # 1. No flags
    print("Running evaluation with no flags...")
    metrics = run_evaluation(query_rewriting=False, re_ranking=False)
    results.append({"Query Rewriting": False, "Re-ranking": False, **metrics})
    
    # 2. Query Rewriting only
    print("Running evaluation with Query Rewriting...")
    metrics = run_evaluation(query_rewriting=True, re_ranking=False)
    results.append({"Query Rewriting": True, "Re-ranking": False, **metrics})
    
    # 3. Re-ranking only
    print("Running evaluation with Re-ranking...")
    metrics = run_evaluation(query_rewriting=False, re_ranking=True)
    results.append({"Query Rewriting": False, "Re-ranking": True, **metrics})
    
    # 4. Both flags
    print("Running evaluation with Query Rewriting and Re-ranking...")
    metrics = run_evaluation(query_rewriting=True, re_ranking=True)
    results.append({"Query Rewriting": True, "Re-ranking": True, **metrics})
    
    
    # Create and print the comparative table
    results_df = pd.DataFrame(results)
    print("\n--- Comparative Evaluation Results ---")
    print(results_df.to_string())
    print("--------------------------------------")
    
    results_df.to_csv("rag_evaluation_results_comparative.csv", index=False)
    print("Comparative results saved to rag_evaluation_results_comparative.csv")
