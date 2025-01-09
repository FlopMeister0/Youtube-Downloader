from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
import sys
import os
from pytubefix import YouTube, Playlist, Search
from pytubefix.exceptions import VideoUnavailable, RegexMatchError
import urllib.request

"""Download Worker"""
class Downloader(QThread):
    # Signals to display information for downloading, errors or status
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    # Properties for Downloads
    def __init__(self,url,save_to,download_type, thumbnail_flag, author_flag):
        super().__init__()
        self.url = url
        self.save_to = save_to
        self.download_type = download_type
        self.thumbnail_flag = thumbnail_flag
        self.author_flag = author_flag
        self.is_running = True

    # Determining what download type to run.
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
            # Emit finished download
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e)) # if download contains error

    """Downloading audio playlist"""
    def download_audio_playlist(self):
        try:
            p = Playlist(self.url)
            total_videos = len(p.video_urls) 
            
            # iterating through the video playlist
            for i, url in enumerate(p.video_urls):
                if not self.is_running: # is the the download worker is not running.
                    break

                try: # Attempt download for youtube video
                    yt = YouTube(url)
                    self.status.emit(f"Downloading: {yt.title}") # status update

                    download_file = yt.streams.filter(only_audio=True).first().download(output_path=self.save_to) # specficially download audio
                    base, extension = os.path.splitext(download_file) # contains only the base for download file

                    if self.author_flag: # checking to add the author to filename
                        download_file = self.include_author(base,yt, extension, download_file)

                    if self.thumbnail_flag: # if the thumbnail box is checked.
                        self.download_thumbnail(yt,base) # passing the youtube url and file

                    progress = int((i + 1) / total_videos * 100) # for each item in playlist divide that + 1 with the total videos x 100 to get percentage.
                    self.progress.emit(progress) # emit the progress to progress bar.

                except VideoUnavailable: # Error handling for unavailable videos and any unexpected occurences
                    self.status.emit(f"Video Unavailable: {url}")
                    continue
                except Exception as e:
                    self.status.emit(f"Error Downloading {url}: {str(e)}")
                    continue

        except Exception as e: # error handling for an unexpected playlist error
            self.error.emit(f"Playlist error: {str(e)}")
    
    def download_video_playlist(self): # Similar setup to the audio playlist comments
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
                    base, extension = os.path.splitext(download_file)

                    if self.author_flag: # checking to add the author to filename
                        download_file = self.include_author(base,yt, extension, download_file)

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

    """Downloads audio or video from specific url instead of a playlist."""
    def download_audio_single(self): # downloads audio from a video rather than a playlist.
        try:
            yt = YouTube(self.url)
            self.status.emit(f"downloading {yt.title}")
            download_file = yt.streams.filter(only_audio=True).first().download(output_path=self.save_to)
            base, extension = os.path.splitext(download_file)

            if self.author_flag: # checking to add the author to filename
                download_file = self.include_author(base,yt, extension, download_file)

            if self.thumbnail_flag:
                self.download_thumbnail(yt,base)
            
            self.progress.emit(100) # pass 100 to progress since it's only 1 video being downloaded.
        except VideoUnavailable:
            self.status.emit(f"Video Unavailable: {self.url}")
        except Exception as e:
            self.status.emit(f"Error Downloading {self.url}: {str(e)}")
    
    def download_video_single(self): # similar setup to download_audio_single but only downloads video
        try:
            yt = YouTube(self.url)
            self.status.emit(f"downloading {yt.title}")
            download_file = yt.streams.filter(only_video=True).first().download(output_path=self.save_to)
            base, extension = os.path.splitext(download_file)

            if self.author_flag: # checking to add the author to filename
                download_file = self.include_author(base,yt, extension, download_file)

            if self.thumbnail_flag:
                self.download_thumbnail(yt,base)
            
            self.progress.emit(100)
        except VideoUnavailable:
            self.status.emit(f"Video Unavailable: {self.url}")
        except Exception as e:
            self.status.emit(f"Error Downloading {self.url}: {str(e)}")

    """Downloads the original youtube video with both audio and video"""
    def download_video_audio_playlist(self): # this is a very similar setup again to playlist but there is no filter.
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
                    base, extension = os.path.splitext(download_file)

                    if self.author_flag: # checking to add the author to filename
                        download_file = self.include_author(base,yt, extension, download_file)

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

    def download_video_audio_single(self): # very similar setup to downloading either video or audio but there is not filter
        try:
            yt = YouTube(self.url)
            self.status.emit(f"downloading {yt.title}")
            download_file = yt.streams.first().download(output_path=self.save_to)
            base, extension = os.path.splitext(download_file)

            if self.author_flag: # checking to add the author to filename
                download_file = self.include_author(base,yt, extension, download_file)

            if self.thumbnail_flag:
                self.download_thumbnail(yt,base)
            
            self.progress.emit(100)
        except VideoUnavailable:
            self.status.emit(f"Video Unavailable: {self.url}")
        except Exception as e:
            self.status.emit(f"Error Downloading {self.url}: {str(e)}")

    """Includes the author"""
    def include_author(self,base,yt,extension, download_file):
        directory = os.path.dirname(download_file) # updates directory
        new_filename = f"{base} (From - {yt.author}){extension}"
        new_download_file = os.path.join(directory, new_filename)

        try:
            os.rename(download_file, new_download_file)
            download_file = new_download_file # update the current value of file
            self.status.emit(f"Renamed file to include Author: {os.path.basename(new_download_file)}") # emits to list
        except Exception as rename_error:
            self.status.emit(f"Error renaming file: {str(rename_error)}") # emits to download list

    """Downloads thumbnail as well as normal download"""
    def download_thumbnail(self,yt,base): # given the youtube url, pass the thumbnail url request and convert it to .jpg
        try:
            thumbnail_url = yt.thumbnail_url
            urllib.request.urlretrieve(thumbnail_url, f"{base}.jpg")
        except Exception as e: # error for any unexpected download failure.
            self.status.emit(f"Thumbnail download failed: {str(e)}")
    
    def stop(self): # stops download worker.
        self.is_running = False

"""PyQt5 Youtube Downloader Ui"""
class Ui_YoutubeDownloader(object):
    def setupUi(self, YoutubeDownloader):
        # Window
        YoutubeDownloader.setObjectName("YoutubeDownloader")
        YoutubeDownloader.resize(698, 378)
        YoutubeDownloader.setMinimumSize(QtCore.QSize(698, 378))
        YoutubeDownloader.setMaximumSize(QtCore.QSize(698, 378))
        self.centralwidget = QtWidgets.QWidget(YoutubeDownloader)
        self.centralwidget.setObjectName("centralwidget")
        # Convert Button
        self.pushButtonConvert = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.Convert())
        self.pushButtonConvert.setGeometry(QtCore.QRect(270, 40, 111, 31))
        self.pushButtonConvert.setObjectName("pushButtonConvert")
        # List of downloaded items
        self.listDownloaded = QtWidgets.QListWidget(self.centralwidget)
        self.listDownloaded.setGeometry(QtCore.QRect(20, 110, 361, 211))
        self.listDownloaded.setObjectName("listDownloaded")
        # Where user enters link to retrieve download data
        self.textEditLink = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditLink.setGeometry(QtCore.QRect(20, 40, 251, 31))
        self.textEditLink.setObjectName("textEditLink")
        # User enters link to retrieve name
        self.textEditName = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditName.setGeometry(QtCore.QRect(20, 80, 251, 31))
        self.textEditName.setObjectName("textEditName")
        # Checkbox for Author
        self.checkBoxAuthor = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxAuthor.setGeometry(QtCore.QRect(390, 160, 211, 17))
        self.checkBoxAuthor.setObjectName("checkBoxAuthor")
        # Progress bar set to default
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(20, 330, 361, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        # Video only Select
        self.radioButtonVideo = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButtonVideo.setGeometry(QtCore.QRect(390, 40, 82, 17))
        self.radioButtonVideo.setObjectName("radioButtonVideo")
        # Audio only Select
        self.radioButtonAudio = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButtonAudio.setGeometry(QtCore.QRect(390, 60, 82, 17))
        self.radioButtonAudio.setObjectName("radioButtonAudio")
        # Original Youtube upload select
        self.radioButtonVideoAndAudio = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButtonVideoAndAudio.setGeometry(QtCore.QRect(390, 80, 91, 16))
        self.radioButtonVideoAndAudio.setObjectName("radioButtonVideoAndAudio")
        # Label for format setting
        self.labelFormat = QtWidgets.QLabel(self.centralwidget)
        self.labelFormat.setGeometry(QtCore.QRect(390, 20, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelFormat.setFont(font)
        self.labelFormat.setObjectName("labelFormat")
        # Label for where the user inputs link
        self.labelLink = QtWidgets.QLabel(self.centralwidget)
        self.labelLink.setGeometry(QtCore.QRect(20, 10, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelLink.setFont(font)
        self.labelLink.setObjectName("labelLink")
        # Label for extra settings
        self.labelExtra = QtWidgets.QLabel(self.centralwidget)
        self.labelExtra.setGeometry(QtCore.QRect(390, 100, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelExtra.setFont(font)
        self.labelExtra.setObjectName("labelExtra")
        # Textedit for the user to specify where downloads go
        self.textEditDirectDownloads = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditDirectDownloads.setGeometry(QtCore.QRect(390, 200, 291, 31))
        self.textEditDirectDownloads.setObjectName("textEditDirectDownloads")
        # Label to direct what the user inputs into TextEditDirectDownloads
        self.labelDirectDownloads = QtWidgets.QLabel(self.centralwidget)
        self.labelDirectDownloads.setGeometry(QtCore.QRect(390, 170, 251, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.labelDirectDownloads.setFont(font)
        self.labelDirectDownloads.setWordWrap(True)
        self.labelDirectDownloads.setObjectName("labelDirectDownloads")
        # Button to search a url for video or playlist title.
        self.pushButtonSearch = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.Search())
        self.pushButtonSearch.setGeometry(QtCore.QRect(270, 80, 111, 31))
        self.pushButtonSearch.setObjectName("pushButtonSearch")
        # Youtube Icon
        self.iconYoutube = QtWidgets.QLabel(self.centralwidget)
        self.iconYoutube.setGeometry(QtCore.QRect(560, 30, 121, 81))
        iconYoutube = "YouTube.png"
        Download_dir = os.path.dirname(__file__)
        icon_youtube_file = os.path.join(Download_dir, "Icons")
        icon_youtube_file_path = os.path.join(icon_youtube_file, iconYoutube)
        self.iconYoutube.setText("")
        self.iconYoutube.setPixmap(QtGui.QPixmap(icon_youtube_file_path))
        self.iconYoutube.setScaledContents(True)
        self.iconYoutube.setObjectName("iconYoutube")
        # Label for what playlist is selected.
        self.labelPlaylistSelected = QtWidgets.QLabel(self.centralwidget)
        self.labelPlaylistSelected.setGeometry(QtCore.QRect(390, 240, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelPlaylistSelected.setFont(font)
        self.labelPlaylistSelected.setObjectName("labelPlaylistSelected")
        # Label for what video is selected.
        self.labelVideoSelected = QtWidgets.QLabel(self.centralwidget)
        self.labelVideoSelected.setGeometry(QtCore.QRect(390, 290, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelVideoSelected.setFont(font)
        self.labelVideoSelected.setObjectName("labelVideoSelected")
        # The textedit that will replace what title is found from a playlist url
        self.textEditPlaylistSelected = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditPlaylistSelected.setGeometry(QtCore.QRect(390, 270, 291, 31))
        self.textEditPlaylistSelected.setObjectName("textEditPlaylistSelected")
        # The textedit that will replace what title is found from a video url
        self.textEditVideoSelected = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditVideoSelected.setGeometry(QtCore.QRect(390, 320, 291, 31))
        self.textEditVideoSelected.setObjectName("textEditVideoSelected")
        # Line to seperate settings and selection.
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(380, 240, 321, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        # To restore default directory
        self.pushButtonDefault = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.default())
        self.pushButtonDefault.setGeometry(QtCore.QRect(390, 230, 291, 21))
        self.pushButtonDefault.setObjectName("pushButtonDefault")
        # Check box for the thumbnail downloads
        self.checkBoxThumbnail = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxThumbnail.setGeometry(QtCore.QRect(390, 120, 151, 17))
        self.checkBoxThumbnail.setObjectName("checkBoxThumbnail")
        # Checkbox to enable if the download if for a playlist.
        self.checkBoxPlaylist = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxPlaylist.setGeometry(QtCore.QRect(390, 140, 211, 17))
        self.checkBoxPlaylist.setObjectName("checkBoxPlaylist")
        # Window and status bar intilization.
        YoutubeDownloader.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(YoutubeDownloader)
        self.statusbar.setObjectName("statusbar")
        YoutubeDownloader.setStatusBar(self.statusbar)

        # Translates widgets and text to eachtother.
        self.retranslateUi(YoutubeDownloader)
        QtCore.QMetaObject.connectSlotsByName(YoutubeDownloader)

        "intialising the downloader"
        self.downloader = None
        self.progressBar.setValue(0)

    """Translates text to widgets"""
    def retranslateUi(self, YoutubeDownloader):
        _translate = QtCore.QCoreApplication.translate
        YoutubeDownloader.setWindowTitle(_translate("YoutubeDownloader", "YoutubeDownloader"))
        self.pushButtonConvert.setText(_translate("YoutubeDownloader", "Convert"))
        self.radioButtonVideo.setText(_translate("YoutubeDownloader", "Video only"))
        self.radioButtonAudio.setText(_translate("YoutubeDownloader", "Audio only"))
        self.radioButtonVideoAndAudio.setText(_translate("YoutubeDownloader", "Video + Audio"))
        self.labelFormat.setText(_translate("YoutubeDownloader", "Format Settings"))
        self.labelLink.setText(_translate("YoutubeDownloader", "Input Links Here:"))
        self.labelExtra.setText(_translate("YoutubeDownloader", "Extra Settings"))
        self.labelDirectDownloads.setText(_translate("YoutubeDownloader", "Optional Download Directory"))
        self.pushButtonSearch.setText(_translate("YoutubeDownloader", "Search"))
        self.labelPlaylistSelected.setText(_translate("YoutubeDownloader", "Playlist Searched:"))
        self.labelVideoSelected.setText(_translate("YoutubeDownloader", "Video Searched:"))
        self.pushButtonDefault.setText(_translate("YoutubeDownloader", "Set back to Default"))
        self.checkBoxThumbnail.setText(_translate("YoutubeDownloader", "Download Thumbnail Aswell"))
        self.checkBoxPlaylist.setText(_translate("YoutubeDownloader", "Check for Playlist / Uncheck for Video"))
        self.checkBoxAuthor.setText(_translate("YoutubeDownloader", "Include Author in Filename"))

    """Searches for youtube video or playlist."""
    def Search(self):
        # Reset the text.
        self.textEditVideoSelected.setText("")
        self.textEditPlaylistSelected.setText("")
        # assigns the url to the plain text.
        url = self.textEditName.toPlainText()

        if self.checkBoxPlaylist.isChecked(): # If the playlist box is checked, it will set the title of the playlist to the textedit.
            try:
                playlist = Playlist(url)
            except RegexMatchError:
                self.textEditPlaylistSelected.setText("No Playlist Found")
            else:
                self.textEditPlaylistSelected.setText(f"Playlist: {playlist.title}")
        else: # when the checkboxplaylist is not checked it will recognise it as a video instead.
            try:
                yt = YouTube(url)
            except RegexMatchError:
                self.textEditVideoSelected.setText("No Video Found")
            else:
                self.textEditVideoSelected.setText(f"Video: {yt.title}")

    """Converting the youtube playlist or video"""
    def Convert(self): 
        self.listDownloaded.clear()
        self.progressBar.setValue(0) # reset the progressbar 
        self.statusbar.showMessage("") # Reset the status bar.
        """Start the download process"""
        if self.downloader and self.downloader.isRunning(): # checking if the download worker is running.
         self.downloader.stop() # resets worker
         self.downloader.wait() 
         self.pushButtonConvert.setText("Convert") # Reset the button back to "convert"
         return

        # Variables for if the user wants the thumbnail, where to save to or the actual link.
        thumbnail_flag = self.checkBoxThumbnail.isChecked()
        author_flag = self.checkBoxAuthor.isChecked()
        link = self.textEditLink.toPlainText()
        save_to = self.textEditDirectDownloads.toPlainText()

        # if the link is invalid.
        if not link:
            self.statusbar.showMessage("Please enter a valid URL")
            return
        
        # if there is no save_to that the user wants. Puts them into programme defaults.
        if not save_to:
            if self.radioButtonAudio.isChecked():
                save_to = "Audio"
            elif self.radioButtonVideo.isChecked():
                save_to = "Video"
            elif self.radioButtonVideoAndAudio.isChecked():
                save_to = "Original"
        
        # if the os path does not exit or is invalid when trying to create it.
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
        self.downloader = Downloader(link, save_to, download_type, thumbnail_flag, author_flag)
        self.downloader.progress.connect(self.update_progress)
        self.downloader.status.connect(self.update_status)
        self.downloader.error.connect(self.handle_error)
        self.downloader.finished.connect(self.download_finished)

        # option to cancel download.
        self.pushButtonConvert.setText("Cancel")
        self.downloader.start()
    
    # updating the progress bar with new values.
    def update_progress(self,value):
        self.progressBar.setValue(value)

    # upading the status bar of downloads.
    def update_status(self, message):
        self.statusbar.showMessage(message)
        self.listDownloaded.addItem(message)
    
    # handling errors.
    def handle_error(self,error_message):
        self.statusbar.showMessage(f"Error: {error_message}")
        self.pushButtonConvert.setText("Convert")

    # if the download has finished.
    def download_finished(self):
        self.pushButtonConvert.setText("Convert")
        self.statusbar.showMessage("Download Completed!")
    
    # reset the directdownloads to nothing.
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