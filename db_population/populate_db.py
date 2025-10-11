import os
import glob

from database.ChromaManager import ChromaManager
from db_population.utils.ChunkingUtils import ChunkingHelper

def populate_db():
    chroma_manager = ChromaManager()
    chroma_manager.create_collection("videos")

    chunking_helper = ChunkingHelper()

    project_root = os.path.dirname(os.path.dirname(__file__))
    dataset_path = os.path.join(project_root, "dataset", "transcripts", "*", "t_*.txt")
    
    for transcript_file in glob.glob(dataset_path):

        with open(transcript_file, "r") as f:
            transcript = f.read()
            video_id = transcript_file.split("/")[-1].split("t_")[1].split(".txt")[0]

            chunks = chunking_helper.get_video_transcript_chunks(transcript)
            for chunk in chunks:
                chroma_manager.add_video_chunk(video_id, chunks.index(chunk), chunk)

if __name__ == "__main__":
    populate_db()