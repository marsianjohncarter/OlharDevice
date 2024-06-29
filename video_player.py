from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl, pyqtSignal


class VideoPlayer(QWidget):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Видеоплеер")
        self.setGeometry(100, 100, 800, 600)
        self.layout = QVBoxLayout(self) # type: ignore
        self.video_widget = QVideoWidget(self)
        self.layout.addWidget(self.video_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.mediaStatusChanged.connect(self.check_status)

    def show_video(self, video_url):
        self.media_player.setMedia(QMediaContent(QUrl(video_url)))
        self.media_player.play()

    def show_local_video(self, video_path):
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(video_path)))
        self.media_player.play()

    def check_status(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.finished.emit() # type: ignore
