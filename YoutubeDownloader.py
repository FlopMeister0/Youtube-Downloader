from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
from pytubefix import YouTube, Playlist
from pytubefix.exceptions import VideoUnavailable
import urllib.request

"""YoutubeDownloader Ui"""
class Ui_YoutubeDownloader(object):
    def setupUi(self, YoutubeDownloader):
        # Window
        YoutubeDownloader.setObjectName("YoutubeDownloader")
        YoutubeDownloader.resize(698, 378)
        YoutubeDownloader.setMinimumSize(QtCore.QSize(698, 378))
        YoutubeDownloader.setMaximumSize(QtCore.QSize(698, 378))
        self.centralwidget = QtWidgets.QWidget(YoutubeDownloader)
        self.centralwidget.setObjectName("centralwidget")
        # Button Convert
        self.pushButtonConvert = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.Convert())
        self.pushButtonConvert.setGeometry(QtCore.QRect(270, 40, 111, 31))
        self.pushButtonConvert.setObjectName("pushButtonConvert")
        # List of downloaded items
        self.listDownloaded = QtWidgets.QListWidget(self.centralwidget)
        self.listDownloaded.setGeometry(QtCore.QRect(20, 130, 361, 191))
        self.listDownloaded.setObjectName("listDownloaded")
        # Button Delete item
        self.pushButtonDelete = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonDelete.setGeometry(QtCore.QRect(20, 110, 361, 21))
        self.pushButtonDelete.setObjectName("pushButtonDelete")
        # Text to edit link for video or playlist
        self.textEditLink = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditLink.setGeometry(QtCore.QRect(20, 40, 251, 31))
        self.textEditLink.setObjectName("textEditLink")
        # Name of video search query
        self.textEditName = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditName.setGeometry(QtCore.QRect(20, 80, 251, 31))
        self.textEditName.setObjectName("textEditName")
        # Progress bar
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(20, 330, 361, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        # Video only select button
        self.radioButtonVideo = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButtonVideo.setGeometry(QtCore.QRect(390, 40, 82, 17))
        self.radioButtonVideo.setObjectName("radioButtonVideo")
        # Audio only select button
        self.radioButtonAudio = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButtonAudio.setGeometry(QtCore.QRect(390, 60, 82, 17))
        self.radioButtonAudio.setObjectName("radioButtonAudio")
        # To be able to download the original source
        self.radioButtonVideoAndAudio = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButtonVideoAndAudio.setGeometry(QtCore.QRect(390, 80, 91, 16))
        self.radioButtonVideoAndAudio.setObjectName("radioButtonVideoAndAudio")
        # thumbnail download select button
        self.radioButtonThumbnail = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButtonThumbnail.setGeometry(QtCore.QRect(390, 120, 171, 17))
        self.radioButtonThumbnail.setObjectName("radioButtonThumbnail")
        # textedit for settings format
        self.labelFormat = QtWidgets.QLabel(self.centralwidget)
        self.labelFormat.setGeometry(QtCore.QRect(390, 20, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelFormat.setFont(font)
        self.labelFormat.setObjectName("labelFormat")
        # text for the link
        self.labelLink = QtWidgets.QLabel(self.centralwidget)
        self.labelLink.setGeometry(QtCore.QRect(20, 10, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelLink.setFont(font)
        self.labelLink.setObjectName("labelLink")
        # text for the extra settings
        self.labelExtra = QtWidgets.QLabel(self.centralwidget)
        self.labelExtra.setGeometry(QtCore.QRect(390, 100, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelExtra.setFont(font)
        self.labelExtra.setObjectName("labelExtra")
        # The edit line for where the user wants to download their items
        self.textEditDirectDownloads = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditDirectDownloads.setGeometry(QtCore.QRect(390, 180, 291, 31))
        self.textEditDirectDownloads.setObjectName("textEditDirectDownloads")
        # Text for directing user to the downloads text edit
        self.labelDirectDownloads = QtWidgets.QLabel(self.centralwidget)
        self.labelDirectDownloads.setGeometry(QtCore.QRect(390, 140, 251, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.labelDirectDownloads.setFont(font)
        self.labelDirectDownloads.setWordWrap(True)
        self.labelDirectDownloads.setObjectName("labelDirectDownloads")
        # Button to search the video query
        self.pushButtonSearch = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSearch.setGeometry(QtCore.QRect(270, 80, 111, 31))
        self.pushButtonSearch.setObjectName("pushButtonSearch")
        # Youtube Icon
        self.iconYoutube = QtWidgets.QLabel(self.centralwidget)
        self.iconYoutube.setGeometry(QtCore.QRect(560, 30, 121, 81))
        iconYoutube = "YouTube.png"
        Music_dir = os.path.dirname(__file__)
        icon_youtube_file = os.path.join(Music_dir, "Icons")
        icon_youtube_file_path = os.path.join(icon_youtube_file, iconYoutube)
        self.iconYoutube.setText("")
        self.iconYoutube.setPixmap(QtGui.QPixmap(icon_youtube_file_path))
        self.iconYoutube.setScaledContents(True)
        self.iconYoutube.setObjectName("iconYoutube")
        # text for what playlist is selected
        self.labelPlaylist = QtWidgets.QLabel(self.centralwidget)
        self.labelPlaylist.setGeometry(QtCore.QRect(390, 230, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelPlaylist.setFont(font)
        self.labelPlaylist.setObjectName("labelPlaylist")
        # text for what video is selected
        self.labelVideo = QtWidgets.QLabel(self.centralwidget)
        self.labelVideo.setGeometry(QtCore.QRect(390, 290, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelVideo.setFont(font)
        self.labelVideo.setObjectName("labelVideo")
        # The Textedit for the selected playlist 
        self.textEditPlaylistSelected = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditPlaylistSelected.setGeometry(QtCore.QRect(390, 260, 291, 31))
        self.textEditPlaylistSelected.setObjectName("textEditPlaylistSelected")
        # The Textedit for the selected video
        self.textEditVideoSelected = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditVideoSelected.setGeometry(QtCore.QRect(390, 320, 291, 31))
        self.textEditVideoSelected.setObjectName("textEditVideoSelected")
        # The line seperating the settings and selection
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(380, 230, 321, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        # The button confirming the download directory
        self.pushButtonConfirm = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonConfirm.setGeometry(QtCore.QRect(390, 210, 141, 21))
        self.pushButtonConfirm.setObjectName("pushButtonConfirm")
        # The button to set download directory to default
        self.pushButtonDefault = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonDefault.setGeometry(QtCore.QRect(530, 210, 151, 21))
        self.pushButtonDefault.setObjectName("pushButtonDefault")
        YoutubeDownloader.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(YoutubeDownloader)
        self.statusbar.setObjectName("statusbar")
        YoutubeDownloader.setStatusBar(self.statusbar)

        self.retranslateUi(YoutubeDownloader)
        QtCore.QMetaObject.connectSlotsByName(YoutubeDownloader)

    """Translates text to widgets"""
    def retranslateUi(self, YoutubeDownloader):
        _translate = QtCore.QCoreApplication.translate
        YoutubeDownloader.setWindowTitle(_translate("YoutubeDownloader", "MainWindow"))
        self.pushButtonConvert.setText(_translate("YoutubeDownloader", "Convert"))
        self.pushButtonDelete.setText(_translate("YoutubeDownloader", "Delete Video"))
        self.radioButtonVideo.setText(_translate("YoutubeDownloader", "Video only"))
        self.radioButtonAudio.setText(_translate("YoutubeDownloader", "Audio only"))
        self.radioButtonVideoAndAudio.setText(_translate("YoutubeDownloader", "Video + Audio"))
        self.radioButtonThumbnail.setText(_translate("YoutubeDownloader", "Download  Thumbnail as well"))
        self.labelFormat.setText(_translate("YoutubeDownloader", "Format Settings"))
        self.labelLink.setText(_translate("YoutubeDownloader", "Input Link Here"))
        self.labelExtra.setText(_translate("YoutubeDownloader", "Extra Settings"))
        self.labelDirectDownloads.setText(_translate("YoutubeDownloader", "Where should the downloads go? (leave blank for application folder)"))
        self.pushButtonSearch.setText(_translate("YoutubeDownloader", "Search"))
        self.labelPlaylist.setText(_translate("YoutubeDownloader", "Playlist Selected:"))
        self.labelVideo.setText(_translate("YoutubeDownloader", "Video Selected:"))
        self.pushButtonConfirm.setText(_translate("YoutubeDownloader", "Confirm"))
        self.pushButtonDefault.setText(_translate("YoutubeDownloader", "Default"))

    def Convert(self):
        """Functions"""
        # if the user wants a thumbnail to be downloaded also
        thumbnail_flag = self.radioButtonThumbnail.isChecked()
        # playlist url
        Playlist_url = self.textEditPlaylistSelected.toPlainText()
        # where it will be saved

        Save_To = self.textEditDirectDownloads.toPlainText()
        if not Save_To:
            if Save_To == "" and self.radioButtonAudio.isChecked():
                Save_To = "Audio"
                DownloadAudio(thumbnail_flag, Playlist_url, Save_To)
            elif Save_To == "" and self.radioButtonVideo.isChecked():
                Save_To = "Video"
                DownloadVideo(thumbnail_flag, Playlist_url, Save_To)
            elif Save_To == "" and self.radioButtonVideoAndAudio.isChecked():
                Save_To = "Original"

        if not os.path.isdir(Save_To):
            self.textEditDirectDownloads.setText("invalid directory!")
            






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

"""Downloads Video Only"""
def DownloadVideo(Playlist_url, Save_To, thumbnail_flag):
    
    print("Download")

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

"""Downloads Audio"""
def DownloadAudio(Playlist_url, Save_To, thumbnail_flag):
    
    print("Download")

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

"""Starts programme when run"""
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    YoutubeDownloader = QtWidgets.QMainWindow()
    ui = Ui_YoutubeDownloader()
    ui.setupUi(YoutubeDownloader)
    YoutubeDownloader.show()
    sys.exit(app.exec_())
