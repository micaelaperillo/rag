from database.ChromaManager import ChromaManager
from llm.llm import OpenAILLM
from llm.prompt import get_prompt

HARDCODED_RESULTS = [
    {
        "video_id": "vid_001",
        "video_title": "Introduction to Machine Learning Fundamentals",
        "video_date": "2024-01-15",
        "video_duration": "12:34",
        "playlist_id": "ml_basics",
        "playlist_name": "Machine Learning Basics",
        "source": "transcript",
        "chunk_index": 0
    },
    {
        "video_id": "vid_002",
        "video_title": "Deep Learning with Neural Networks",
        "video_date": "2024-01-22",
        "video_duration": "18:45",
        "playlist_id": "ml_basics",
        "playlist_name": "Machine Learning Basics",
        "source": "transcript",
        "chunk_index": 1
    },
    {
        "video_id": "vid_003",
        "video_title": "Python Data Structures and Algorithms",
        "video_date": "2024-02-01",
        "video_duration": "15:20",
        "playlist_id": "python_fundamentals",
        "playlist_name": "Python Programming",
        "source": "transcript",
        "chunk_index": 0
    },
    {
        "video_id": "vid_004",
        "video_title": "Linear Algebra for Data Science",
        "video_date": "2024-02-08",
        "video_duration": "22:15",
        "playlist_id": "math_foundations",
        "playlist_name": "Mathematical Foundations",
        "source": "transcript",
        "chunk_index": 2
    },
    {
        "video_id": "vid_005",
        "video_title": "Natural Language Processing Basics",
        "video_date": "2024-02-15",
        "video_duration": "16:30",
        "playlist_id": "nlp_intro",
        "playlist_name": "NLP Introduction",
        "source": "transcript",
        "chunk_index": 0
    },
    {
        "video_id": "vid_006",
        "video_title": "Computer Vision and Image Recognition",
        "video_date": "2024-02-22",
        "video_duration": "19:45",
        "playlist_id": "cv_basics",
        "playlist_name": "Computer Vision",
        "source": "transcript",
        "chunk_index": 1
    },
    {
        "video_id": "vid_007",
        "video_title": "Statistics and Probability Theory",
        "video_date": "2024-03-01",
        "video_duration": "14:25",
        "playlist_id": "math_foundations",
        "playlist_name": "Mathematical Foundations",
        "source": "transcript",
        "chunk_index": 0
    },
    {
        "video_id": "vid_008",
        "video_title": "TensorFlow and PyTorch Comparison",
        "video_date": "2024-03-08",
        "video_duration": "21:10",
        "playlist_id": "ml_frameworks",
        "playlist_name": "ML Frameworks",
        "source": "transcript",
        "chunk_index": 0
    },
    {
        "video_id": "vid_009",
        "video_title": "Data Preprocessing and Feature Engineering",
        "video_date": "2024-03-15",
        "video_duration": "17:55",
        "playlist_id": "data_science",
        "playlist_name": "Data Science Pipeline",
        "source": "transcript",
        "chunk_index": 1
    },
    {
        "video_id": "vid_010",
        "video_title": "Model Evaluation and Cross-Validation",
        "video_date": "2024-03-22",
        "video_duration": "13:40",
        "playlist_id": "data_science",
        "playlist_name": "Data Science Pipeline",
        "source": "transcript",
        "chunk_index": 2
    }
]


class Recommender:
    def __init__(self):
        pass

    def recommend(self, query, user_preferences):
        chroma_manager = ChromaManager()
        chroma_manager.get_collection("videos")
        # results = chroma_manager.search_video_chunks(query, limit=10)
        llm = OpenAILLM()
        answer = llm.generate_recommendations(get_prompt(query, HARDCODED_RESULTS, user_preferences))
        return answer