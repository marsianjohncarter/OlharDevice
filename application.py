import os
import time
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QGraphicsOpacityEffect
from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation, pyqtSignal
from PyQt5.QtGui import QPixmap
import qrcode
import requests
from services import Services
from video_player import VideoPlayer
from diagnostic_menu import Menu

service = Services()

BASE_URL = 'https://api.olhar.media/'
BASE_URL_VIDEO_ENDED = 'https://api.olhar.media/?regview=1'
ASSETS_FOLDER = "./assets"
CURRENT_CITY = service.get_current_city()


logger = service.get_logger('application')
logger.info(f'Current city: {CURRENT_CITY}')


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Видеоплеер")
        self.showFullScreen()

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
        self.menu_window = None

        self.logs = {
                "app.load_video_data": "",
                "app.load_videos": "",
                "app.play_next_video": "",
                "app.show_qr_code": "",
            }
        
        self.video_player.finished.connect(self.fade_out_video) # type: ignore


    def download_video(self, url, local_video_path: str):
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            logger.info(f"Downloading video {local_video_path}...")
            try:
                with open(f"{local_video_path}", "wb") as file:
                    for chunk in response.iter_content(chunk_size=1024*1024):
                        file.write(chunk)
                logger.info(f"Video {local_video_path} downloaded successfully")
            except Exception as e:
                logger.critical(f"Video could not be downloaded. Error: {e}")
        else:
            logger.critical(f"Video could not be downloaded. Status code: {response.status_code}")

    def load_video_data(self, video_data):
        try:
            self.video_data = video_data
            self.logs["app.load_video_data"] = "Список видео успешно загружен."
        except Exception as e:
            self.logs["app.load_video_data"] = f"Ошибка при загрузке списка видео: {e}"

    def load_videos(self, video_data):
        for i in self.video_data:
            local_video_path = os.path.join(f'{ASSETS_FOLDER}/videos/', i['serverfilename'])
            if not os.path.exists(local_video_path):
                self.download_video(BASE_URL + "videos/"+ i['serverfilename'], local_video_path)
            else:
                logger.info(f"Video {i['serverfilename']} already downloaded.")


        self.video_list = []
        for video in video_data:
            for city in video['locations']:
                if city['city'] == CURRENT_CITY:
                    self.video_list.append(video['serverfilename'])
                else:
                    pass

        if self.video_list:
            self.play_next_video()

    def play_next_video(self):
        self.qr_code_label.hide()
        self.message_label.hide()
        self.video_player.video_widget.show()
        if self.current_video_index < len(self.video_list):
            local_video_path = './assets/videos/' + self.video_list[self.current_video_index]
            self.video_player.show_local_video(local_video_path)
            self.current_video_index += 1
        else:
            self.current_video_index = 0
            self.load_videos(self.video_data)
            
    def fade_out_video(self):
        self.show_qr_code()

    def show_qr_code(self):
        self.video_player.video_widget.hide()
        try:
            if self.current_video_index > 0:
                current_video_data = self.video_data[self.current_video_index - 1]
                video_id = current_video_data['id']
                equip_id = service.get_param_from_config('config.ini', 'PN')
                equip_ip = "192.168.1.1"
                url = f"https://link.olhar.media/?golink=1&equipid={equip_id}&videoid={video_id}&equipip={equip_ip}&gpslat=40&gpslon=40"
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
        if not self.menu_window:
            self.menu_window = Menu()
            self.menu_window.show()
            self.menu_window.updateMenu()
        else:
            self.menu_window.show()