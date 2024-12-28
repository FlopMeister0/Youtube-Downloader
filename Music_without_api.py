# test link: https://www.youtube.com/watch?v=zLrOS5oz6IQ
# streaming playlist: https://www.youtube.com/playlist?list=PLRvGeqCR1PHVpTBpuVQhd2oixW4FXi56z
# It's Bangers and mash time: https://youtube.com/playlist?list=PLRvGeqCR1PHXu9gwYaYEU60s1sDuCe712&si=-5dnVHX5oledQjai

from pytubefix import YouTube, Playlist
from pytubefix.exceptions import VideoUnavailable
import urllib.request
import os

"""Retrieves video ID"""
class ConvertMP3():
    # if the user wants a thumbnail to be downloaded also
    thumbnail_flag = False
    # playlist url
    Playlist_url = "https://www.youtube.com/playlist?list=PLRvGeqCR1PHVpTBpuVQhd2oixW4FXi56z"
    # where it will be saved
    Save_To = "MP3"
    
    def DownloadMP3(Playlist_url, Save_To, thumbnail_flag):
        
        def DownloadThumbnailMP3(base, url):
            thumbnail_url = yt.thumbnail_url # fetches url
            urllib.request.urlretrieve(thumbnail_url, f"{base}.jpg") # downloads from thumbnail url and names it the string of the file + .jpg without the extension.
            
        p = Playlist(Playlist_url) # recognises the playlist
        for url in p.video_urls: # for each url in the playlist videos
            try:
                yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)  # fetches the youtube video
            except VideoUnavailable:
                print("Video Unavailable")
                pass
            else: # if there are no errors
                Download_File = yt.streams.filter(only_audio=True).first().download(output_path=Save_To) # downloades only the audio and outputs to mp3
                base, extension = os.path.splitext(Download_File) # splits filename from it's extension
                mp3 = base + ".mp3" # replaces extension with .mp3
                os.rename(Download_File, mp3) 
                
                print(base)
                
                if thumbnail_flag == True: # if the flag is set to true
                    DownloadThumbnailMP3(base, url)
        
    DownloadMP3(Playlist_url, Save_To, thumbnail_flag)
            

def MP4():
    Playlist_url = "https://youtube.com/playlist?list=PLRvGeqCR1PHXu9gwYaYEU60s1sDuCe712&si=-5dnVHX5oledQjai"
    p = Playlist(Playlist_url)
    Save_To = "MP4"
    
    for url in p.video_urls:
        try:
            yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)
        except VideoUnavailable:
            print("Video Unavailable")
            pass
        else:
            Download_File = yt.streams.first().download(output_path=Save_To)
            print(Download_File)
            
if __name__ == "__main__":
    print("running")