import csv
from database.SupabaseManager import SupabaseManager

def populate_playlists():
    supabase_manager = SupabaseManager()
    with open("./utils/playlists.csv", "r") as f:
        reader = csv.reader(f)
        reader.__next__()
        for row in reader:
            print(f"Adding playlist {row[2]} {row[1]}")
            supabase_manager.add_playlist(row[2], row[1], row[0])

def populate_videos():
    supabase_manager = SupabaseManager()
    with open("./dataset/videos.csv", "r") as f:
        reader = csv.reader(f)
        reader.__next__()
        for row in reader:
            print(f"Adding video {row[0]} {row[1]}")
            try:
                supabase_manager.add_video(row[0], row[1], row[2], row[3], row[4], row[5])
            except Exception as e:
                print(f"Error adding video {row[0]} {row[1]}: {e}")
                continue

if __name__ == "__main__":
    # populate_playlists()
    populate_videos()