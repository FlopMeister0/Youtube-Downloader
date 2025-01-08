from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
import sys
import os
from pytubefix import YouTube, Playlist, Search
from pytubefix.exceptions import VideoUnavailable, RegexMatchError
import urllib.request

class Downloader(QThread):
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self,url,save_to,download_type, thumbnail_flag):
        super().__init__()
        self.url = url
        self.save_to = save_to
        self.download_type = download_type
        self.thumbnail_flag = thumbnail_flag
        self.is_running = True

    def run(self):
        try:
            if self.download_type == "audio_playlist":
                self.download_audio_playlist()
            elif self.download_type == "video_playlist":
                self.download_video_playlist()
            elif self.download_type == "audio_single":
                self.download_audio_single()
            elif self.download_type == "video_single":
                self.download_video_single()
            elif self.download_type == "video_audio_playlist":
                self.download_video_audio_playlist()
            elif self.download_type == "video_audio_single":
                self.download_video_audio_single()
            else:
                self.status.emit("invalid download type")
            
            # More download types as needed here
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

    def download_audio_playlist(self):
        try:
            p = Playlist(self.url)
            total_videos = len(p.video_urls)
        
            for i, url in enumerate(p.video_urls):
                if not self.is_running:
                    break

                try:
                    yt = YouTube(url)
                    self.status.emit(f"Downloading: {yt.title}")

                    download_file = yt.streams.filter(only_audio=True).first().download(output_path=self.save_to)
                    base, _ = os.path.splitext(download_file)

                    if self.thumbnail_flag:
                        self.download_thumbnail(yt,base)

                    progress = int((i + 1) / total_videos * 100)
                    self.progress.emit(progress)

                except VideoUnavailable:
                    self.status.emit(f"Video Unavailable: {url}")
                    continue
                except Exception as e:
                    self.status.emit(f"Error Downloading {url}: {str(e)}")
                    continue

        except Exception as e:
            self.error.emit(f"Playlist error: {str(e)}")
    
    def download_video_playlist(self):
        try:
            p = Playlist(self.url)
            total_videos = len(p.video_urls)
        
            for i, url in enumerate(p.video_urls):
                if not self.is_running:
                    break

                try:
                    yt = YouTube(url)
                    self.status.emit(f"Downloading: {yt.title}")

                    download_file = yt.streams.filter(only_video=True).first().download(output_path=self.save_to)
                    base, _ = os.path.splitext(download_file)

                    if self.thumbnail_flag:
                        self.download_thumbnail(yt,base)

                    progress = int((i + 1) / total_videos * 100)
                    self.progress.emit(progress)

                except VideoUnavailable:
                    self.status.emit(f"Video Unavailable: {url}")
                    continue
                except Exception as e:
                    self.status.emit(f"Error Downloading {url}: {str(e)}")
                    continue

        except Exception as e:
            self.error.emit(f"Playlist error: {str(e)}")

    def download_audio_single(self):
        try:
            yt = YouTube(self.url)
            self.status.emit(f"downloading {yt.title}")
            download_file = yt.streams.filter(only_audio=True).first().download(output_path=self.save_to)
            base, _ = os.path.splitext(download_file)

            if self.thumbnail_flag:
                self.download_thumbnail(yt,base)
            
            self.progress.emit(100)
        except VideoUnavailable:
            self.status.emit(f"Video Unavailable: {self.url}")
        except Exception as e:
            self.status.emit(f"Error Downloading {self.url}: {str(e)}")
    
    def download_video_single(self):
        try:
            yt = YouTube(self.url)
            self.status.emit(f"downloading {yt.title}")
            download_file = yt.streams.filter(only_audio=True).first().download(output_path=self.save_to)
            base, _ = os.path.splitext(download_file)

            if self.thumbnail_flag:
                self.download_thumbnail(yt,base)
            
            self.progress.emit(100)
        except VideoUnavailable:
            self.status.emit(f"Video Unavailable: {self.url}")
        except Exception as e:
            self.status.emit(f"Error Downloading {self.url}: {str(e)}")

    def download_video_audio_playlist(self):
        try:
            p = Playlist(self.url)
            total_videos = len(p.video_urls)
        
            for i, url in enumerate(p.video_urls):
                if not self.is_running:
                    break

                try:
                    yt = YouTube(url)
                    self.status.emit(f"Downloading: {yt.title}")

                    download_file = yt.streams.first().download(output_path=self.save_to)
                    base, _ = os.path.splitext(download_file)

                    if self.thumbnail_flag:
                        self.download_thumbnail(yt,base)

                    progress = int((i + 1) / total_videos * 100)
                    self.progress.emit(progress)

                except VideoUnavailable:
                    self.status.emit(f"Video Unavailable: {url}")
                    continue
                except Exception as e:
                    self.status.emit(f"Error Downloading {url}: {str(e)}")
                    continue

        except Exception as e:
            self.error.emit(f"Playlist error: {str(e)}")

    def download_video_audio_single(self):
        try:
            yt = YouTube(self.url)
            self.status.emit(f"downloading {yt.title}")
            download_file = yt.streams.first().download(output_path=self.save_to)
            base, _ = os.path.splitext(download_file)

            if self.thumbnail_flag:
                self.download_thumbnail(yt,base)
            
            self.progress.emit(100)
        except VideoUnavailable:
            self.status.emit(f"Video Unavailable: {self.url}")
        except Exception as e:
            self.status.emit(f"Error Downloading {self.url}: {str(e)}")

    def download_thumbnail(self,yt,base):
        try:
            thumbnail_url = yt.thumbnail_url
            urllib.request.urlretrieve(thumbnail_url, f"{base}.jpg")
        except Exception as e:
            self.status.emit(f"Thumbnail download failed: {str(e)}")
    
    def stop(self):
        self.is_running = False


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
        self.pushButtonSearch = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.Search())
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
        self.pushButtonDefault = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.default())
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

        "intialising the downloader"
        self.downloader = None
        self.progressBar.setValue(0)


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

    def Search(self):
        url = self.textEditName.toPlainText()

        if self.checkBoxPlaylist.isChecked():
            try:
                playlist = Playlist(url)
            except RegexMatchError:
                self.textEditPlaylistSelected.setText("No Playlist Found")
            else:
                self.textEditPlaylistSelected.setText(f"Playlist: {playlist.title}")
        else:
            try:
                yt = YouTube(url)
            except RegexMatchError:
                self.textEditVideoSelected.setText("No Video Found")
            else:
                self.textEditVideoSelected.setText(f"Video: {yt.title}")


    def Convert(self):
        self.progressBar.setValue(0)
        self.statusbar.showMessage("")
        """Start the download process"""
        if self.downloader and self.downloader.isRunning():
         self.downloader.stop()
         self.downloader.wait()
         self.pushButtonConvert.setText("Convert")
         return

        thumbnail_flag = self.checkBoxThumbnail.isChecked()
        link = self.textEditLink.toPlainText()
        save_to = self.textEditDirectDownloads.toPlainText()

        if not link:
            self.statusbar.showMessage("Please enter a valid URL")
            return
        
        if not save_to:
            if self.radioButtonAudio.isChecked():
                save_to = "Audio"
            elif self.radioButtonVideo.isChecked():
                save_to = "Video"
            elif self.radioButtonVideoAndAudio.isChecked():
                save_to = "Original"
            
        if not os.path.exists(save_to):
            try:
                os.makedirs(save_to)
            except Exception as e:
                self.statusbar.showMessage(f"Error creating directory: {str(e)}")
                return

        # determining the download type
        if self.radioButtonAudio.isChecked() and self.checkBoxPlaylist.isChecked():
            download_type = "audio_playlist"
        elif self.radioButtonVideo.isChecked() and self.checkBoxPlaylist.isChecked():
            download_type = "video_playlist"
        elif self.radioButtonAudio.isChecked():
            download_type = "audio_single"
        elif self.radioButtonVideo.isChecked():
            download_type = "video_single"
        elif self.checkBoxPlaylist.isChecked():
            download_type = "video_audio_playlist"
        else:
            download_type = "video_audio_single"
        
        # create and starting the download worker:
        self.downloader = Downloader(link, save_to, download_type, thumbnail_flag)
        self.downloader.progress.connect(self.update_progress)
        self.downloader.error.connect(self.update_status)
        self.downloader.error.connect(self.handle_error)
        self.downloader.finished.connect(self.download_finished)

        self.pushButtonConvert.setText("Cancel")
        self.downloader.start()
    
    def update_progress(self,value):
        self.progressBar.setValue(value)

    def update_status(self, message):
        self.statusbar.showMessage(message)
        self.listDownloaded.addItem(message)
    
    def handle_error(self,error_message):
        self.statusbar.showMessage(f"Error: {error_message}")
        self.pushButtonConvert.setText("Convert")

    def download_finished(self):
        self.pushButtonConvert.setText("Convert")
        self.statusbar.showMessage("Download Completed!")
    
    def default(self):
        self.textEditDirectDownloads.setText("")


"""Starts programme when run"""
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    YoutubeDownloader = QtWidgets.QMainWindow()
    ui = Ui_YoutubeDownloader()
    ui.setupUi(YoutubeDownloader)
    YoutubeDownloader.show()
    sys.exit(app.exec_())