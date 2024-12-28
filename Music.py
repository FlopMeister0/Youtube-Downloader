# test link: https://www.youtube.com/watch?v=zLrOS5oz6IQ
# streaming playlist: https://www.youtube.com/playlist?list=PLRvGeqCR1PHVpTBpuVQhd2oixW4FXi56z

from pytubefix import YouTube
from pytubefix.exceptions import VideoUnavailable
import os
from googleapiclient.discovery import build
import googleapiclient 

"""Api Connection"""
api_version = "v3"
api_service_name = "youtube"
api_key = "AIzaSyC4LwYBzN1iIAP_Y2lnQfJMtIXTY0CUT2g"

youtube_connection = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

request = youtube_connection.playlistItems().list(
   part = "contentDetails",
   maxResults = "50",
   playlistId = "PLRvGeqCR1PHVpTBpuVQhd2oixW4FXi56z"
)
response = request.execute() # response from the request

"""Retrieves video ID"""
def retrieve():
    for item in response['items']:
        video_id = item['contentDetails']['videoId']
        saving(video_id)
        
        print(video_id)

########################################
def saving(video_id):
    Save_To = "MP3"
    link = f"https://www.youtube.com/watch?v={video_id}"

    # yt = YouTube(link, use_oauth=True, allow_oauth_cache=True)

    # yt.streams.filter(file_extension="mp3")
    
    try:
        yt = YouTube(link, use_oauth=True, allow_oauth_cache=True)
    except VideoUnavailable:
        print(f"Video {link} is unavaiable")
        pass
    else:
        print("Downloading . . .")
        Download_File = yt.streams.first().download(output_path=Save_To)
        base, extension = os.path.splitext(Download_File)
        mp3 = base + ".mp3"
        os.rename(Download_File, mp3)

retrieve()

# File already exists error