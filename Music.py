# test link: https://www.youtube.com/watch?v=zLrOS5oz6IQ
# streaming playlist: https://www.youtube.com/playlist?list=PLRvGeqCR1PHVpTBpuVQhd2oixW4FXi56z

from pytube import YouTube
from googleapiclient.discovery import build
import googleapiclient 

"""Api Connection"""
api_version = "v3"
api_service_name = "youtube"

youtube_connection = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

request = youtube_connection.playlistItems().list(
   part = "contentDetails",
   maxResults = "50",
   playlistId = "PLRvGeqCR1PHVpTBpuVQhd2oixW4FXi56z"
)
response = request.execute() # response from the request

"""Retrieves video ID"""
def retrieve():
    id = []
    for item in response['items']:
        id.append(response)
        video_id = item['contentDetails']['videoId']
        saving(video_id)
        
        print(video_id)

############################################
# USING FFMPEG INSTEAD?

def saving(video_id):
    Save_To = "/Users/elija/Desktop/Projects/Music/Music/MP3"
    link = f"https://www.youtube.com/watch?v={video_id}"

    yt = YouTube(link)
    yt = YouTube(link, use_oauth=True, allow_oauth_cache=True)

    mp3 = yt.streams.filter(file_extension="mp3").all()

    try:
        mp3.download(output_path=Save_To)
    except:
        print("error")

retrieve()