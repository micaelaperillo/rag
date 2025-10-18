import pandas as pd

# Load both CSV files
videos = pd.read_csv('./dataset/videos.csv')
playlists = pd.read_csv('./dataset/playlists.csv')

# Merge on playlist_id
merged = pd.merge(videos, playlists, on='playlist_id', how='left')

# Save to new dataset
merged.to_csv('./dataset/dataset.csv', index=False)

print("✅ Merged dataset saved as dataset.csv")
print(merged.head())