import logging
import os
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QGraphicsOpacityEffect
from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation,  QTime
from PyQt5.QtGui import QPixmap
import qrcode
import requests
from services import Services
from video_player import VideoPlayer
from diagnostic_menu import DiagnosticMenu
import json


BASE_URL_VIDEO_ENDED = 'https://api.olhar.media/?regview=1'
ASSETS_FOLDER = "./assets"


logger = logging.getLogger('application')

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Видеоплеер")
        self.showFullScreen()

        self.service = Services()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget) # type: ignore
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.video_player = VideoPlayer()

        self.layout.addWidget(self.video_player)

        self.message_label = QLabel("Воспользуйтесь Вашим предложением прямо сейчас!", self)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("font-size: 60px;")
        self.message_label.hide()

        self.layout.addWidget(self.message_label)
        
        self.qr_code_label = QLabel(self)
        self.qr_code_label.setAlignment(Qt.AlignCenter)
        self.qr_code_label.setStyleSheet("""
            QLabel {
                margin-bottom: 20px;
                border-radius: 15px;
            }
        """)
        self.qr_code_label.hide()
        self.layout.addWidget(self.qr_code_label, 0, Qt.AlignBottom)

        self.current_video_index = 0
        self.video_list = []
        self.video_data = []
        self.diagnostic_window = None # It changes in set_video_data()
        self.diagnostic_window_open = False
        self.video_player.finished.connect(self.fade_out_video) # type: ignore

    def download_video(self, url, local_video_path: str):
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            logger.info(f"Downloading video {local_video_path}...")
            try:
                with open(f"{local_video_path}.dat.incomplete", "wb") as file:
                    for chunk in response.iter_content(chunk_size=1024*1024):
                        file.write(chunk)
                os.rename(f"{local_video_path}.dat.incomplete", local_video_path)
                logger.info(f"Video {local_video_path} downloaded successfully")
            except Exception as e:
                logger.critical(f"Video could not be downloaded. Error: {e}")
        else:
            logger.critical(f"Video could not be downloaded. Status code: {response.status_code}")

    def set_video_data(self, video_data):
        self.video_data = video_data
        self.diagnostic_window = DiagnosticMenu(json.dumps(video_data, indent=4))
        try:
            self.service.save_json(self.video_data, f'{ASSETS_FOLDER}/data/video_data.json')
        except Exception as e:
            logger.critical(e)

    def start_videos(self, video_data):
        self.video_url_list = ['https://api.olhar.media/' + '/videos/' + video['serverfilename'] for video in video_data]
        self.video_list = [video['serverfilename'] for video in video_data]

        for i, video_url in enumerate(self.video_url_list):
                    local_video_path = f'P{ASSETS_FOLDER}/videos/' + self.video_list[i]
                    self.download_video(video_url, local_video_path)
        if len(self.video_list) > 0:
            self.play_next_video()
        else:
            logger.critical(f"No videos found for city {self.current_city}.")
            # raise RuntimeError(f"No videos found for city {self.current_city}.")

    def play_next_video(self):
        self.service.set_brightness()
        self.qr_code_label.hide()
        self.message_label.hide()
        self.video_player.video_widget.show()
        if self.current_video_index < len(self.video_list):
            local_video_path = './assets/videos/' + self.video_list[self.current_video_index]
            try:
                self.video_player.show_local_video(local_video_path)
            except Exception as e:
                logger.critical(f"Error playing video: {e}")
                raise RuntimeError(f"Error playing video: {e}") from e
            self.current_video_index += 1
        else:
            self.current_video_index = 0
            self.start_videos(self.video_data)
            
    def fade_out_video(self):
        self.show_qr_code()

    def show_qr_code(self):
        self.video_player.video_widget.hide()
        try:
            if self.current_video_index > 0:
                current_video_data = self.video_data[self.current_video_index - 1]
                video_id = current_video_data['id']
                equip_id = self.service.get_param_from_config('config.ini', 'PN')
                equip_ip = f'{requests.get("https://api.ipify.org").content.decode("utf8")}'
                lat_and_lon = self.service.get_lat_lon()
                url = f"https://link.olhar.media/?golink=1&equipid={equip_id}&videoid={video_id}&equipip={equip_ip}&gpslat={lat_and_lon[0]}&gpslon={lat_and_lon[1]}"
                qr = qrcode.QRCode(  # type: ignore
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L, # type: ignore
                    box_size=10,
                    border=4,
                )
                qr.add_data(url)
                qr.make(fit=True)
                img = qr.make_image(fill='black', back_color='white')
                img.save(f'{ASSETS_FOLDER}/images/qr_code.png')
                pixmap = QPixmap(f'{ASSETS_FOLDER}/images/qr_code.png')
                self.qr_code_label.setPixmap(pixmap)
                self.qr_code_label.show()
                self.message_label.show()
                self.qr_opacity_effect = QGraphicsOpacityEffect(self.qr_code_label)
                self.qr_code_label.setGraphicsEffect(self.qr_opacity_effect)
                self.message_opacity_effect = QGraphicsOpacityEffect(self.message_label)
                self.message_label.setGraphicsEffect(self.message_opacity_effect)
                self.qr_opacity_animation = QPropertyAnimation(self.qr_opacity_effect, b"opacity")
                self.qr_opacity_animation.setDuration(3000)
                self.qr_opacity_animation.setStartValue(0)
                self.qr_opacity_animation.setEndValue(1)
                self.qr_opacity_animation.start()
                self.message_opacity_animation = QPropertyAnimation(self.message_opacity_effect, b"opacity")
                self.message_opacity_animation.setDuration(3000)
                self.message_opacity_animation.setStartValue(0)
                self.message_opacity_animation.setEndValue(1)
                self.message_opacity_animation.start()
                QTimer.singleShot(5000, self.play_next_video)
                self.logs["app.show_qr_code"] = "QR-код и сообщение успешно отображены."
        except Exception as e:
            self.logs["app.show_qr_code"] = f"Ошибка при отображении QR-кода и сообщения: {e}"

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == Qt.Key_Space: 
            self.openMenu()
        else:
            super().keyPressEvent(qKeyEvent)
    
    def openMenu(self):
        if not self.diagnostic_window_open:
            self.diagnostic_window_open = True
            self.diagnostic_window.sig.connect(self.menuClosed) 
            self.diagnostic_window.show()
        else:
            self.diagnostic_window_open = False
            self.diagnostic_window.hide()

    def menuClosed(self):
        self.diagnostic_window_open = False