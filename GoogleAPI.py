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