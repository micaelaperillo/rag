from database.ChromaManager import ChromaManager
from llm.llm import OpenAILLM
from llm.prompt import get_prompt, get_query_rewriting_prompt

HARDCODED_RESULTS = [
    {
        "video_id": "bX3jvD7XFPs",
        "video_title": "Python Data Structures and Algorithms",
        "video_date": "2024-02-01",
        "video_duration": "15:20",
        "playlist_id": "PLB2BE3D6CA77BB8F7",
        "playlist_name": "Python Programming",
        "source": "FreeCodeCamp",
        "chunk_index": 10
    }
]


class Recommender:
    def __init__(self, collection_name="videos"):
        self.collection_name = collection_name

    def recommend(self, query, user_preferences):
        chroma_manager = ChromaManager()
        llm = OpenAILLM()
        chroma_manager.get_collection(self.collection_name)
        rewritten_query = llm.generate_text(get_query_rewriting_prompt(query))
        # print("Rewritten query: ", rewritten_query)
        results = chroma_manager.search_video_chunks(rewritten_query, limit=5)
        # print("Chroma results: ", results)
        
        answer = llm.generate_recommendations(get_prompt(query, results, user_preferences))
        
        import json
        if isinstance(answer, str):
            try:
                parsed_answer = json.loads(answer)
                return parsed_answer
            except json.JSONDecodeError:
                return "Error parsing JSON from the LLM"
        return answer

    def recommend_testing(self, query, user_preferences, query_rewriting=False):
        chroma_manager = ChromaManager()
        llm = OpenAILLM()
        chroma_manager.get_collection(self.collection_name)
        if query_rewriting:
            rewritten_query = llm.generate_text(get_query_rewriting_prompt(query))
        else:
            rewritten_query = query
        results = chroma_manager.search_video_chunks(rewritten_query, limit=5)
        
        answer = llm.generate_text(get_prompt(query, results, user_preferences))
        return {"llm_response": answer, "chroma_results": results}