from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl, pyqtSignal
import logging
from datetime import date


logger = logging.getLogger('video_player')

class VideoPlayer(QWidget):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Видеоплеер")
        self.setGeometry(100, 100, 800, 600)
        self.layout = QVBoxLayout(self) # type: ignore
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.video_widget = QVideoWidget(self)
        self.layout.addWidget(self.video_widget)
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.mediaStatusChanged.connect(self.check_status)
        

    def show_local_video(self, video_path):
        try:
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(video_path)))
            self.media_player.play()
        except Exception as e:
            raise RuntimeError(f"Error playing video: {video_path}") from e

    def check_status(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.finished.emit() # type: ignore
