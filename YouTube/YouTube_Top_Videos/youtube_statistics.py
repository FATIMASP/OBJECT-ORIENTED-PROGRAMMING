import config
from googleapiclient.discovery import build
import pandas as pd

class YouTubeStatistics:
    def __init__(self):
        self.api_key = config.api_key
        self.search_query = config.search_query
        self.max_results = config.max_results
        self.top = config.top
        self.final_cols = config.final_cols
        self.int_cols = config.int_cols
        self.sorting_cols = config.sorting_cols
        self.sorting_order = config.sorting_order

    def get_youtube_data(self):
        youtube = build('youtube', 'v3', developerKey=self.api_key)

        # Search for videos based on the query
        search_response = youtube.search().list(
            q=self.search_query,
            type='video',
            part='id,snippet',
            maxResults=self.max_results
        ).execute()

        video_data = []

        # Iterate through the search results
        for search_result in search_response.get('items', []):
            video_id = search_result['id']['videoId']
            video_statistics = youtube.videos().list(
                part='snippet,statistics',
                id=video_id
            ).execute()

            video_snippet = video_statistics['items'][0]['snippet']
            video_stats = video_statistics['items'][0]['statistics']

            # Fetch additional channel information
            channel_id = video_snippet['channelId']
            channel_stats = self.get_channel_statistics(youtube, channel_id)

            video_info = {
                'Video Title': video_snippet['title'],
                'Views': int(video_stats['viewCount']),
                'Likes': int(video_stats.get('likeCount', 0)),
                'Video Link': f'https://www.youtube.com/watch?v={video_id}',
                'Channel Title': video_snippet['channelTitle'],
                'Channel Link': f'https://www.youtube.com/channel/{channel_id}',
                'Subscribers': channel_stats.get('subscriberCount', 0),
                'Channel Views': channel_stats.get('viewCount', 0),
                'Total Videos': channel_stats.get('videoCount', 0)
            }

            video_data.append(video_info)

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(video_data)

        # Convert specified integer columns to int type with handling large values
        df[self.int_cols] = df[self.int_cols].apply(pd.to_numeric, errors='coerce', downcast='integer')

        # Sort the DataFrame based on specified columns and order
        df.sort_values(by=self.sorting_cols, ascending=self.sorting_order, inplace=True)

        # Reset index starting from 1 and add a new column 'SNo'
        df = df.reset_index(drop=True)
        df.index += 1
        df = df.reset_index().rename(columns={"index": "SNo"})

        # Filter top rows into a new DataFrame df2
        df2 = df.head(self.top)
        df2 = df2[self.final_cols]

        return df2

    def get_channel_statistics(self, youtube, channel_id):
        channel_statistics = youtube.channels().list(
            part='statistics',
            id=channel_id
        ).execute()

        if 'items' in channel_statistics:
            return channel_statistics['items'][0]['statistics']
        else:
            return {}

    def display_info(self):
        print(f"api_key: {self.api_key}, query: {self.search_query}")

# Example usage
if __name__ == "__main__":
    obj = YouTubeStatistics()
    obj.display_info()

    youtube_data_df = obj.get_youtube_data()

