import os
import csv

from database.ChromaManager import ChromaManager
from db_population.utils.ChunkingUtils import ChunkingHelper

def populate_db(start_line=0):
    chroma_manager = ChromaManager()
    chroma_manager.create_collection("videos")

    chunking_helper = ChunkingHelper()
    
    # video_id,title,description,date,duration,playlist_id,transcript_file,source,subject
    with open("./dataset/combined_dataset.csv", "r") as f:
        reader = csv.reader(f)
        
        # Skip header only if starting from line 0
        if start_line == 0:
            reader.__next__()
        
        # Skip lines until we reach the desired starting line
        for i in range(0, start_line):
            try:
                reader.__next__()
            except StopIteration:
                print(f"Warning: Starting line {start_line} is beyond the end of the file")
                return
        
        for row in reader:
            try:
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
                    try:
                        print(f"Adding chunk {chunks.index(chunk)} for video {video_id}")
                        chroma_manager.add_video_chunk(video_id, video_title, video_date, video_duration, playlist_id, playlist_name, source, chunks.index(chunk), chunk)
                    except Exception as e:
                        print(f"Error adding chunk {chunks.index(chunk)} for video {video_id}: {str(e)}")
                        continue
                        
            except Exception as e:
                print(f"Error processing video {row[0] if len(row) > 0 else 'unknown'}: {str(e)}")
                continue

if __name__ == "__main__":
    import sys
    
    # Default to line 0 if no argument provided
    start_line = 0
    if len(sys.argv) > 1:
        try:
            start_line = int(sys.argv[1])
            if start_line < 0:
                print("Error: Starting line must be 0 or greater")
                sys.exit(1)
        except ValueError:
            print("Error: Starting line must be a valid integer")
            sys.exit(1)
    
    print(f"Starting population from line {start_line}")
    populate_db(start_line)