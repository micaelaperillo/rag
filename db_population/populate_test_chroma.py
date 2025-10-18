import csv
from database.ChromaManager import ChromaManager
from db_population.utils.ChunkingUtils import ChunkingHelper

def populate_test_db():
    chroma_manager = ChromaManager()
    collection_name = "test_videos"
    
    try:
        chroma_manager.get_collection(collection_name)
        print(f"Collection '{collection_name}' already exists. Cleaning it.")
        chroma_manager.clean_database(collection_name)
        chroma_manager.create_collection(collection_name)
    except Exception:
        print(f"Collection '{collection_name}' does not exist. Creating it.")
        chroma_manager.create_collection(collection_name)

    chunking_helper = ChunkingHelper()
    
    with open("./test_dataset/test_dataset.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        
        for row in reader:
            try:
                video_id = row[0]
                video_title = row[1]
                video_date = row[3]
                video_duration = row[4]
                playlist_id = row[5]
                transcript_file = row[6]
                source = row[7]
                playlist_name = "Test Playlist" 

                with open(transcript_file, "r") as tf:
                    transcript = tf.read()

                chunks = chunking_helper.get_video_transcript_chunks(transcript)
                for i, chunk in enumerate(chunks):
                    try:
                        print(f"Adding chunk {i} for video {video_id}")
                        chroma_manager.add_video_chunk(
                            video_id, 
                            video_title, 
                            video_date, 
                            video_duration, 
                            playlist_id, 
                            playlist_name, 
                            source, 
                            i, 
                            chunk
                        )
                    except Exception as e:
                        print(f"Error adding chunk {i} for video {video_id}: {str(e)}")
                        continue
                        
            except Exception as e:
                print(f"Error processing video {row[0] if len(row) > 0 else 'unknown'}: {str(e)}")
                continue

if __name__ == "__main__":
    populate_test_db()
    print("Test database population complete.")
