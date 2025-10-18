import chromadb
import os
from dotenv import load_dotenv
load_dotenv()

class ChromaManager:
    def __init__(self):
        # self.client = chromadb.PersistentClient(path="./database/chroma_db")
        self.client = chromadb.CloudClient(
            api_key=os.getenv("CHROMA_API_KEY"),
            tenant=os.getenv("CHROMA_TENANT"),
            database="videos"
        )

    def create_collection(self, collection_name):
        self.collection = self.client.create_collection(collection_name)
        print(f"Created collection {self.collection.name}")

    def get_collection(self, collection_name):
        self.collection = self.client.get_collection(collection_name)

    def add_video_chunk(self, video_id, video_title, video_date, video_duration, playlist_id, playlist_name, source, chunk_index, chunk_transcript):
        print(f"Adding chunk {chunk_index} for video {video_id} on collection {self.collection.name}")
        self.collection.add(
            ids=[f"{video_id}_{chunk_index}"],
            documents=[chunk_transcript],
            metadatas={
                "video_id": video_id,
                "video_title": video_title,
                "video_date": video_date,
                "video_duration": video_duration,
                "playlist_id": playlist_id,
                "playlist_name": playlist_name,
                "source": source,
                "chunk_index": chunk_index
            }
        )

    def search_video_chunks(self, query, limit=10):
        return self.collection.query(
            query_texts=[query],
            n_results=limit
        )

    def clean_database(self, collection_name):
        self.client.delete_collection(collection_name)