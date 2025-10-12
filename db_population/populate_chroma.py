import os
import csv

from database.ChromaManager import ChromaManager
from db_population.utils.ChunkingUtils import ChunkingHelper

def populate_db():
    chroma_manager = ChromaManager()
    chroma_manager.create_collection("videos")

    chunking_helper = ChunkingHelper()
    
    # video_id,title,description,date,duration,playlist_id,transcript_file,source,subject
    with open("./dataset/combined_dataset.csv", "r") as f:
        reader = csv.reader(f)
        reader.__next__()
        for row in reader:
            video_id = row[0]
            video_title = row[1]
            video_date = row[3]
            video_duration = row[4]
            playlist_id = row[5]
            transcript_file = row[6]
            source = row[7]
            playlist_name = row[8]

            transcript = open(transcript_file, "r").read()
            chunks = chunking_helper.get_video_transcript_chunks(transcript)
            for chunk in chunks:
                print(f"Adding chunk {chunks.index(chunk)} for video {video_id}")
                chroma_manager.add_video_chunk(video_id, video_title, video_date, video_duration, playlist_id, playlist_name, source, chunks.index(chunk), chunk)

if __name__ == "__main__":
    populate_db()