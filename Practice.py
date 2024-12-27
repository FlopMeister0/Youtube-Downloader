from pytubefix import YouTube

Save_To = "MP3"
link = f"https://www.youtube.com/watch?v=zLrOS5oz6IQ"

yt = YouTube(link, use_oauth=True, allow_oauth_cache=True)

mp3 = yt.streams.filter(file_extension="mp3")

yt.streams.first().download(output_path=Save_To)

