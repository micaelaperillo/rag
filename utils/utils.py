import csv
import os
import subprocess
from googleapiclient.discovery import build
from dotenv import load_dotenv
import re

load_dotenv()

API_KEY = os.getenv('YOUTUBE_API_KEY')
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

DATASET_DIR = 'dataset'
TRANSCRIPTS_DIR = os.path.join(DATASET_DIR, 'transcripts')
CSV_FILE = os.path.join(DATASET_DIR, 'videos.csv')
PLAYLISTS_CSV = 'utils/playlists.csv'

def load_playlists(file_path):
    playlists = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            playlists.append(row['playlist_id'])
    return playlists

from googleapiclient.discovery import build
from datetime import timedelta
import isodate

def get_videos_from_playlist(playlist_id):
    youtube = build("youtube", "v3", developerKey=API_KEY)
    videos = []
    next_page_token = None

    while True:
        playlist_request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        playlist_response = playlist_request.execute()

        video_ids = [item['snippet']['resourceId']['videoId'] for item in playlist_response['items']]
        if not video_ids:
            break

        videos_request = youtube.videos().list(
            part="contentDetails,snippet",
            id=",".join(video_ids)
        )
        videos_response = videos_request.execute()

        for item in videos_response['items']:
            snippet = item['snippet']
            content_details = item['contentDetails']

            duration_iso = content_details.get('duration', 'PT0S')
            duration = isodate.parse_duration(duration_iso)
            duration_str = str(duration)

            videos.append({
                'id': item['id'],
                'title': snippet.get('title', ''),
                'description': snippet.get('description', ''),
                'date': snippet.get('publishedAt', ''),
                'duration': duration_str,
                'playlist_id': playlist_id
            })

        next_page_token = playlist_response.get('nextPageToken')
        if not next_page_token:
            break

    return videos


def save_transcript(video_id, playlist_id):
    transcript_dir = os.path.join(TRANSCRIPTS_DIR, playlist_id)
    os.makedirs(transcript_dir, exist_ok=True)
    transcript_file = os.path.join(transcript_dir, f't_{video_id}.txt')

    cmd = [
        'yt-dlp',
        f'https://www.youtube.com/watch?v={video_id}',
        '--write-auto-sub',
        '--sub-lang', 'en',
        '--skip-download',
        '--output', os.path.join(transcript_dir, f't_{video_id}.%(ext)s'),
        '--sub-format', 'srt'  
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        srt_file = transcript_file.replace('.txt', '.en.srt')
        if os.path.exists(srt_file):
            text = srt_to_text(srt_file)
            with open(transcript_file, 'w', encoding='utf-8') as f:
                f.write(text)
            os.remove(srt_file)
            return transcript_file
        else:
            print(f"No subtitles downloaded for {video_id}")
            return ''
    except subprocess.CalledProcessError as e:
        print(f"Error downloading subtitles for {video_id}: {e}")
        return ''

def srt_to_text(srt_path):
    with open(srt_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    text_lines = []
    for line in lines:
        line = line.strip()
        if line == '' or line.isdigit() or '-->' in line:
            continue
        text_lines.append(line)

    return ' '.join(text_lines)

def main():
    os.makedirs(DATASET_DIR, exist_ok=True)
    playlists = load_playlists(PLAYLISTS_CSV)

    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['video_id', 'title', 'description', 'date', 'duration', 'playlist_id', 'transcript_file']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for playlist_id in playlists:
            print(f"Processing playlist {playlist_id}...")
            videos = get_videos_from_playlist(playlist_id)
            for video in videos:
                print(f"Processing video {video['id']} - {video['title']}")

                transcript_file = save_transcript(video['id'], playlist_id)

                writer.writerow({
                    'video_id': video['id'],
                    'title': video['title'],
                    'description': video['description'],
                    'date': video['date'],
                    'duration': video['duration'],
                    'playlist_id': playlist_id,
                    'transcript_file': transcript_file
                })

    print(f"\nAll playlists processed. CSV saved at {CSV_FILE}")

if __name__ == "__main__":
    main()
