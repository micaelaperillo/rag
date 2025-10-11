import chromadb

class ChromaManager:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./database/chroma_db")

    def create_collection(self, collection_name):
        self.collection = self.client.create_collection(collection_name)
        print(f"Created collection {self.collection.name}")

    def get_collection(self, collection_name):
        self.collection = self.client.get_collection(collection_name)

    def add_video_chunk(self, video_id, chunk_index, chunk_transcript):
        print(f"Adding chunk {chunk_index} for video {video_id} on collection {self.collection.name}")
        self.collection.add(
            ids=[f"{video_id}_{chunk_index}"],
            documents=[chunk_transcript],
            metadatas={
                "video_id": video_id,
                "chunk_index": chunk_index
            }
        )

    def search_video_chunks(self, query, limit=10):
        return self.collection.query(
            query_texts=[query],
            n_results=limit
        )

    def clean_database(self):
        self.client.delete_collection("videos")