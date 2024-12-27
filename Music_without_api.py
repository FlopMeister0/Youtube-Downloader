# test link: https://www.youtube.com/watch?v=zLrOS5oz6IQ
# streaming playlist: https://www.youtube.com/playlist?list=PLRvGeqCR1PHVpTBpuVQhd2oixW4FXi56z

from pytubefix import YouTube, Playlist
from pytubefix.exceptions import VideoUnavailable
import os

"""Retrieves video ID"""
def retrieve():
    Playlist_url = "https://www.youtube.com/playlist?list=PLRvGeqCR1PHVpTBpuVQhd2oixW4FXi56z"
    p = Playlist(Playlist_url)
    Save_To = "MP3"
    
    for url in p.video_urls:
        try:
            yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)
        except VideoUnavailable:
            print("Video Unavailable")
            pass
        else:
            Download_File = yt.streams.filter(only_audio=True).first().download(output_path=Save_To)
            base, extension = os.path.splitext(Download_File)
            mp3 = base + ".mp3"
            os.rename(Download_File, mp3)

retrieve()