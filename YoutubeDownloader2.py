from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
from pytubefix import YouTube, Playlist
from pytubefix.exceptions import VideoUnavailable
import urllib.request


class Ui_YoutubeDownloader(object):
    def setupUi(self, YoutubeDownloader):
        YoutubeDownloader.setObjectName("YoutubeDownloader")
        YoutubeDownloader.resize(698, 378)
        YoutubeDownloader.setMinimumSize(QtCore.QSize(698, 378))
        YoutubeDownloader.setMaximumSize(QtCore.QSize(698, 378))
        self.centralwidget = QtWidgets.QWidget(YoutubeDownloader)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButtonConvert = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.Convert())
        self.pushButtonConvert.setGeometry(QtCore.QRect(270, 40, 111, 31))
        self.pushButtonConvert.setObjectName("pushButtonConvert")
        self.listDownloaded = QtWidgets.QListWidget(self.centralwidget)
        self.listDownloaded.setGeometry(QtCore.QRect(20, 130, 361, 191))
        self.listDownloaded.setObjectName("listDownloaded")
        self.pushButtonDelete = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonDelete.setGeometry(QtCore.QRect(20, 110, 361, 21))
        self.pushButtonDelete.setObjectName("pushButtonDelete")
        self.textEditLink = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditLink.setGeometry(QtCore.QRect(20, 40, 251, 31))
        self.textEditLink.setObjectName("textEditLink")
        self.textEditName = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditName.setGeometry(QtCore.QRect(20, 80, 251, 31))
        self.textEditName.setObjectName("textEditName")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(20, 330, 361, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.radioButtonVideo = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButtonVideo.setGeometry(QtCore.QRect(390, 40, 82, 17))
        self.radioButtonVideo.setObjectName("radioButtonVideo")
        self.radioButtonAudio = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButtonAudio.setGeometry(QtCore.QRect(390, 60, 82, 17))
        self.radioButtonAudio.setObjectName("radioButtonAudio")
        self.radioButtonVideoAndAudio = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButtonVideoAndAudio.setGeometry(QtCore.QRect(390, 80, 91, 16))
        self.radioButtonVideoAndAudio.setObjectName("radioButtonVideoAndAudio")
        self.labelFormat = QtWidgets.QLabel(self.centralwidget)
        self.labelFormat.setGeometry(QtCore.QRect(390, 20, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelFormat.setFont(font)
        self.labelFormat.setObjectName("labelFormat")
        self.labelLink = QtWidgets.QLabel(self.centralwidget)
        self.labelLink.setGeometry(QtCore.QRect(20, 10, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelLink.setFont(font)
        self.labelLink.setObjectName("labelLink")
        self.labelExtra = QtWidgets.QLabel(self.centralwidget)
        self.labelExtra.setGeometry(QtCore.QRect(390, 100, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelExtra.setFont(font)
        self.labelExtra.setObjectName("labelExtra")
        self.textEditDirectDownloads = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditDirectDownloads.setGeometry(QtCore.QRect(390, 200, 291, 31))
        self.textEditDirectDownloads.setObjectName("textEditDirectDownloads")
        self.labelDirectDownloads = QtWidgets.QLabel(self.centralwidget)
        self.labelDirectDownloads.setGeometry(QtCore.QRect(390, 160, 251, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.labelDirectDownloads.setFont(font)
        self.labelDirectDownloads.setWordWrap(True)
        self.labelDirectDownloads.setObjectName("labelDirectDownloads")
        self.pushButtonSearch = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSearch.setGeometry(QtCore.QRect(270, 80, 111, 31))
        self.pushButtonSearch.setObjectName("pushButtonSearch")

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

        self.labelPlaylistSelected = QtWidgets.QLabel(self.centralwidget)
        self.labelPlaylistSelected.setGeometry(QtCore.QRect(390, 240, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelPlaylistSelected.setFont(font)
        self.labelPlaylistSelected.setObjectName("labelPlaylistSelected")
        self.labelVideoSelected = QtWidgets.QLabel(self.centralwidget)
        self.labelVideoSelected.setGeometry(QtCore.QRect(390, 290, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelVideoSelected.setFont(font)
        self.labelVideoSelected.setObjectName("labelVideoSelected")
        self.textEditPlaylistSelected = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditPlaylistSelected.setGeometry(QtCore.QRect(390, 270, 291, 31))
        self.textEditPlaylistSelected.setObjectName("textEditPlaylistSelected")
        self.textEditVideoSelected = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditVideoSelected.setGeometry(QtCore.QRect(390, 320, 291, 31))
        self.textEditVideoSelected.setObjectName("textEditVideoSelected")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(380, 240, 321, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.pushButtonConfirm = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonConfirm.setGeometry(QtCore.QRect(390, 230, 141, 21))
        self.pushButtonConfirm.setObjectName("pushButtonConfirm")
        self.pushButtonDefault = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonDefault.setGeometry(QtCore.QRect(530, 230, 151, 21))
        self.pushButtonDefault.setObjectName("pushButtonDefault")
        self.checkBoxThumbnail = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxThumbnail.setGeometry(QtCore.QRect(390, 120, 151, 17))
        self.checkBoxThumbnail.setObjectName("checkBoxThumbnail")
        self.checkBoxPlaylist = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxPlaylist.setGeometry(QtCore.QRect(390, 140, 211, 17))
        self.checkBoxPlaylist.setObjectName("checkBoxPlaylist")
        YoutubeDownloader.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(YoutubeDownloader)
        self.statusbar.setObjectName("statusbar")
        YoutubeDownloader.setStatusBar(self.statusbar)

        self.retranslateUi(YoutubeDownloader)
        QtCore.QMetaObject.connectSlotsByName(YoutubeDownloader)

    def retranslateUi(self, YoutubeDownloader):
        _translate = QtCore.QCoreApplication.translate
        YoutubeDownloader.setWindowTitle(_translate("YoutubeDownloader", "MainWindow"))
        self.pushButtonConvert.setText(_translate("YoutubeDownloader", "Convert"))
        self.pushButtonDelete.setText(_translate("YoutubeDownloader", "Delete Video"))
        self.radioButtonVideo.setText(_translate("YoutubeDownloader", "Video only"))
        self.radioButtonAudio.setText(_translate("YoutubeDownloader", "Audio only"))
        self.radioButtonVideoAndAudio.setText(_translate("YoutubeDownloader", "Video + Audio"))
        self.labelFormat.setText(_translate("YoutubeDownloader", "Format Settings"))
        self.labelLink.setText(_translate("YoutubeDownloader", "Input Link Here:"))
        self.labelExtra.setText(_translate("YoutubeDownloader", "Extra Settings"))
        self.labelDirectDownloads.setText(_translate("YoutubeDownloader", "Where should the downloads go? (leave blank for application folder)"))
        self.pushButtonSearch.setText(_translate("YoutubeDownloader", "Search"))
        self.labelPlaylistSelected.setText(_translate("YoutubeDownloader", "Playlist Selected:"))
        self.labelVideoSelected.setText(_translate("YoutubeDownloader", "Video Selected:"))
        self.pushButtonConfirm.setText(_translate("YoutubeDownloader", "Confirm"))
        self.pushButtonDefault.setText(_translate("YoutubeDownloader", "Default"))
        self.checkBoxThumbnail.setText(_translate("YoutubeDownloader", "Download Thumbnail Aswell"))
        self.checkBoxPlaylist.setText(_translate("YoutubeDownloader", "Check for Playlist / Uncheck for Video"))

    def Convert(self):
        """Functions"""
        # if the user wants a thumbnail to be downloaded also
        thumbnail_flag = self.checkBoxThumbnail.isChecked()
        # playlist url
        Playlist_url = self.textEditLink.toPlainText()
        # where it will be saved

        Save_To = self.textEditLink.toPlainText()
        if not Save_To:
            if Save_To == "" and self.radioButtonAudio.isChecked() and self.checkBoxPlaylist.isChecked():
                Save_To = "Audio"
                DownloadAudio(thumbnail_flag, Playlist_url, Save_To)
            elif Save_To == "" and self.radioButtonVideo.isChecked():
                Save_To = "Video"
                DownloadVideo(thumbnail_flag, Playlist_url, Save_To)
            elif Save_To == "" and self.radioButtonVideoAndAudio.isChecked():
                Save_To = "Original"

        if not os.path.isdir(Save_To):
            self.textEditDirectDownloads.setText("invalid directory!")
            
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

"""Starts programme when run"""
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    YoutubeDownloader = QtWidgets.QMainWindow()
    ui = Ui_YoutubeDownloader()
    ui.setupUi(YoutubeDownloader)
    YoutubeDownloader.show()
    sys.exit(app.exec_())