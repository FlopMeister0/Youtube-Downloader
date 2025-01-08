from pytubefix import YouTube

url = "https://youtu.be/XRIE02v7Ri4?si=_hmFhT0PBDj-YjS1"
yt = YouTube(url)
print(yt.author)