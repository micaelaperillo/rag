import os
import supabase
from dotenv import load_dotenv

load_dotenv()

class SupabaseManager:
    def __init__(self):
        self.client = supabase.create_client(
            supabase_url=os.getenv("SUPABASE_URL"),
            supabase_key=os.getenv("SUPABASE_API_KEY")
        )

    def reset_tables(self):
        self.client.table("videos").delete().execute()
        self.client.table("playlists").delete().execute()

    def add_video(self, video_id, title, description, date, duration, playlist_id):
        self.client.table("videos").insert({"video_id": video_id, "title": title, "description": description, "date": date, "duration": duration, "playlist_id": playlist_id}).execute()

    def get_video(self, video_id):
        return self.client.table("videos").select("*").eq("video_id", video_id).execute()

    def get_all_videos(self):
        return self.client.table("videos").select("*").execute()

    def get_videos_by_playlist_id(self, playlist_id):
        return self.client.table("videos").select("*").eq("playlist_id", playlist_id).execute()

    def add_playlist(self, playlist_id, subject, source):
        self.client.table("playlists").insert({"playlist_id": playlist_id, "subject": subject, "source": source}).execute()

    def get_playlist(self, playlist_id):
        return self.client.table("playlists").select("*").eq("playlist_id", playlist_id).execute()

    def get_all_playlists(self):
        return self.client.table("playlists").select("*").execute()