import json
import torch
from database.ChromaManager import ChromaManager
from llm.llm import OpenAILLM
from llm.prompt import get_prompt, get_query_rewriting_prompt
from sentence_transformers.cross_encoder import CrossEncoder

# HARDCODED_RESULTS = [
#     {
#         "video_id": "bX3jvD7XFPs",
#         "video_title": "Python Data Structures and Algorithms",
#         "video_date": "2024-02-01",
#         "video_duration": "15:20",
#         "playlist_id": "PLB2BE3D6CA77BB8F7",
#         "playlist_name": "Python Programming",
#         "source": "FreeCodeCamp",
#         "chunk_index": 10
#     }
# ]

class Recommender:
    def __init__(self):
        # Define the model. 'ms-marco-MiniLM-L-6-v2' is fast and effective
        model_name = 'cross-encoder/ms-marco-MiniLM-L-6-v2'
        
        self.device = "cpu"
        
        self.cross_encoder_model = CrossEncoder(model_name, device=self.device, max_length=512)

    def crossEncoderReRanking(self, query, results):
        """
        Re-ranks a list of retrieved documents using the Cross-Encoder model.

        Returns:
            list: A new list of result dictionaries, sorted by relevance
                  score in descending order.
        """
        # If no results, return an empty list
        if not results:
            return []
        
        parsed_results = []
        sentence_pairs = []

        try:
            # Case 1: Results are raw ChromaDB output
            if isinstance(results, dict) and 'documents' in results and 'metadatas' in results:
                doc_list = results['documents'][0]
                meta_list = results['metadatas'][0]
                
                if len(doc_list) != len(meta_list):
                    print("Warning: Mismatch in document and metadata count. Aborting re-ranking.")
                    return results # Return original results

                for i, doc_text in enumerate(doc_list):
                    parsed_results.append({
                        "document": doc_text,
                        "metadata": meta_list[i]
                    })
                    sentence_pairs.append([query, doc_text])

            # Case 2: Results are already a list of dictionaries
            elif isinstance(results, list) and len(results) > 0 and 'document' in results[0]:
                parsed_results = results
                sentence_pairs = [[query, result['document']] for result in results]
            
            else:
                return results

            if not sentence_pairs:
                return []

            scores = self.cross_encoder_model.predict(sentence_pairs, show_progress_bar=False)

            scored_results = list(zip(scores, parsed_results))

            scored_results.sort(key=lambda x: x[0], reverse=True)

            re_ranked_list = [result for score, result in scored_results]

            return re_ranked_list

        except Exception as e:
            print(f"Error during re-ranking: {e}. Returning original results.")
            return results


    def recommend(self, query, user_preferences):
        chroma_manager = ChromaManager()
        llm = OpenAILLM()
        chroma_manager.get_collection("videos")
        
        # 1. Query Rewriting
        rewritten_query = llm.generate_text(get_query_rewriting_prompt(query))
        # print("Rewritten query: ", rewritten_query)
        
        # 2. Retrieval
        retrieved_results = chroma_manager.search_video_chunks(rewritten_query, limit=15)
        # print(f"Chroma retrieved {len(retrieved_results.get('ids', [[]])[0]) if isinstance(retrieved_results, dict) else len(retrieved_results)} results.")

        # 3. Re-ranking
        re_ranked_results = self.crossEncoderReRanking(rewritten_query, retrieved_results)
        
        # print(f"retrieved results: {retrieved_results}")
        # print(f"re-ranked results: {re_ranked_results}")

        # 4. Pruning
        unique_video_results = []
        included_video_ids = set()
        for result in re_ranked_results:
            video_id = result.get('metadata', {}).get('video_id')
            if video_id and video_id not in included_video_ids:
                unique_video_results.append(result)
                included_video_ids.add(video_id)
        
        top_k = 5
        final_results_for_prompt = unique_video_results[:top_k]
        

        # 5. Generation
        answer = llm.generate_recommendations(get_prompt(query, final_results_for_prompt, user_preferences))
        
        # 6. Parsing
        if isinstance(answer, str):
            try:
                parsed_answer = json.loads(answer)
                return parsed_answer
            except json.JSONDecodeError:
                print(f"Error: LLM output was not valid JSON. Output: {answer}")
                return "Error parsing JSON from the LLM"
        return answer