# test link: https://www.youtube.com/watch?v=zLrOS5oz6IQ
# streaming playlist: https://www.youtube.com/playlist?list=PLRvGeqCR1PHVpTBpuVQhd2oixW4FXi56z
# It's Bangers and mash time: https://youtube.com/playlist?list=PLRvGeqCR1PHXu9gwYaYEU60s1sDuCe712&si=-5dnVHX5oledQjai

from pytubefix import YouTube, Playlist
from pytubefix.exceptions import VideoUnavailable
import urllib.request
import os

"""Retrieves Audio"""
class GetAudio():
    # if the user wants a thumbnail to be downloaded also
    thumbnail_flag = True
    # playlist url
    Playlist_url = input(str("Enter URL: "))
    # where it will be saved
    Save_To = "Audio"
    
    """Downloads Audio"""
    def DownloadAudio(Playlist_url, Save_To, thumbnail_flag):
        
        """Downloads thumbnail for MP3"""
        def DownloadThumbnail(base, url):
            thumbnail_url = yt.thumbnail_url # fetches url
            urllib.request.urlretrieve(thumbnail_url, f"{base}.jpg") # downloads from thumbnail url and names it the string of the file + .jpg without the extension.
        
        """Continuation of Audio function"""
        p = Playlist(Playlist_url) # recognises the playlist
        for url in p.video_urls: # for each url in the playlist videos
            try:
                yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)  # fetches the youtube video
            except VideoUnavailable:
                print("Video Unavailable")
                pass
            except FileExistsError:
                print("File already Exists")
                pass
            else: # if there are no errors
                Download_File = yt.streams.filter(only_audio=True).first().download(output_path=Save_To) # downloades only the audio and outputs to mp3
                base, extension = os.path.splitext(Download_File) # splits filename from it's extension

                print(f"\nsuccessfully downloaded: {yt.title}")
                
                if thumbnail_flag == True: # if the flag is set to true
                    DownloadThumbnail(base, url)
        
    DownloadAudio(Playlist_url, Save_To, thumbnail_flag)
            
"""Retrieves Original Video"""
def Original():
    Playlist_url = "https://youtube.com/playlist?list=PLRvGeqCR1PHXu9gwYaYEU60s1sDuCe712&si=-5dnVHX5oledQjai"
    p = Playlist(Playlist_url)
    Save_To = "Video"
    
    for url in p.video_urls:
        try:
            yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)
        except VideoUnavailable:
            print("Video Unavailable")
            pass
        else:
            Download_File = yt.streams.first().download(output_path=Save_To)
            print(Download_File)

"""Rums programme"""
__name__ == "__main__"

# if __name__ == "__main__":
#     print("more options")