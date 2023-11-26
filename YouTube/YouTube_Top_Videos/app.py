# app.py
from youtube_statistics import YouTubeStatistics
# Create an instance of YouTubeStatistics and retrieve YouTube data
youtube_stats = YouTubeStatistics()
df = youtube_stats.get_youtube_data()
# Copy data to clipboard
df.to_clipboard(index=False)
# Display the result or use it as needed
print(df)