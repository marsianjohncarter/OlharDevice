from datetime import date
from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from PyQt5.QtGui import QFont
import logging
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QScrollArea
import shutil
import psutil 

ASSETS_FOLDER = "./assets"


logger = logging.getLogger('diagnostic_menu')


class DataScrollArea(QScrollArea):
    def __init__(self, video_data):
        super().__init__()
        self.setWindowTitle('Logs')
        self.setGeometry(400, 400, 700, 500)
        self.setStyleSheet("background-color: black;") 

        self.data = video_data

        self.json_label = QLabel(text=f'{self.data}')
        self.json_label.setStyleSheet('color: white; font-weight: bold;')


        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(self.json_label)

        widget = QWidget()
        widget.setLayout(layout)
        self.setWidget(widget)
        self.setWidgetResizable(True)

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == Qt.Key_Escape: 
            self.close()
        else:
            super().keyPressEvent(qKeyEvent)

class LogScrollArea(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f'Log file: {date.today()}.log')
        self.setGeometry(400, 400, 700, 500)
        self.setStyleSheet("background-color: black;") 

        self.logs = 'Test'

        self.logs_label = QLabel(text=f'{self.logs}')
        self.logs_label.setStyleSheet('color: white; font-weight: bold;')

        self.updateLogs(f'{ASSETS_FOLDER}/logs/{date.today()}.log')


        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(self.logs_label)

        widget = QWidget()
        widget.setLayout(layout)
        self.timer = QTimer(self)

        self.timer.timeout.connect(lambda: self.updateLogs(f'{ASSETS_FOLDER}/logs/{date.today()}.log'))
        self.timer.start(1000)
        

        self.setWidget(widget)
        self.setWidgetResizable(True)
  
    def updateLogs(self, file):
        try:
            with open(file, 'r') as txt:
                list_of_lines = txt.read() 
            self.logs = list_of_lines
        except FileNotFoundError:
            logger.error(f'File {file} not found')
            self.logs = 'File not found'
        self.logs_label.setText(list_of_lines)
       
    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == Qt.Key_Escape: 
            self.close()
        else:
            super().keyPressEvent(qKeyEvent)

class DiagnosticWindow(QMainWindow):
    sig = pyqtSignal()

    def __init__(self, video_data):
        super().__init__()
        self.setWindowTitle('Diagnostic Menu')
        self.setGeometry(400, 400, 700, 500)

        self.video_data = video_data

        self.logs_scroll_area = LogScrollArea()
        self.logs_scroll_area_open = False

        self.json_scroll_area = DataScrollArea(self.video_data)
        self.json_scroll_area_open = False

        default_font = QFont()
        default_font.setBold(True)
        layout = QVBoxLayout()

        
        self.logs_btn = QPushButton(text='Open Logs')
        self.logs_btn.clicked.connect(self.toggleLogs)        
        self.json_btn = QPushButton(text='Open Company Data')
        self.json_btn.clicked.connect(self.toggleJson)
        storage_info = self.getStorageInfo()
        self.storage_label = QLabel(text=f'Storage: \nTotal: {storage_info["total"]}GB | Used: {storage_info["used"]}GB | Free: {storage_info["free"]}GB')
        self.storage_label.setStyleSheet("font-size: 15px;")
        self.storage_label.setAlignment(Qt.AlignCenter)
        self.storage_label.setFont(default_font)

        self.cpu_util_label = QLabel(text=f'{self.getCpuInfo()}')
        self.cpu_util_label.setAlignment(Qt.AlignCenter)
        self.cpu_util_label.setFont(default_font)
        self.cpu_util_label.setStyleSheet("font-size: 15px;")

        self.info_label = QLabel(text='(To exit press ESC)')
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setFont(default_font)

        layout.addWidget(self.info_label)
        layout.addWidget(self.json_btn)
        layout.addWidget(self.logs_btn)
        layout.addWidget(self.storage_label)
        layout.addWidget(self.cpu_util_label)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.timer = QTimer(self)

        self.timer.timeout.connect(self.updatediagnosticMenu)
        self.timer.start(1000)
        
    def toggleLogs(self):
        if not self.logs_scroll_area_open:
            self.logs_scroll_area.show()
            self.logs_scroll_area_open = True
        else:
            self.logs_scroll_area.hide()
            self.logs_scroll_area_open = False
    
    def toggleJson(self):
        if not self.json_scroll_area_open:
            self.json_scroll_area.show()
            self.json_scroll_area_open = True
        else:
            self.json_scroll_area.hide()
            self.json_scroll_area_open = False

    def getStorageInfo(self):
        total, used, free = shutil.disk_usage("/")
        return {'total':total % (total // (2**30)), 'used':used % (used // (2**30)), 'free':free % (free // (2**30))}
    
    def getCpuInfo(self):
        return f"CPU utilization: {psutil.cpu_percent()}%"

    def updatediagnosticMenu(self):
        storage_info = self.getStorageInfo()
        self.storage_label.setText(f'Storage: \nTotal: {storage_info["total"]}GB | Used: {storage_info["used"]}GB | Free: {storage_info["free"]}GB')
        self.cpu_util_label.setText(f'{self.getCpuInfo()}')
    
    def closeEvent(self, event):
        self.sig.emit() # type: ignore

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == Qt.Key_Escape: 
            self.close()
        else:
            super().keyPressEvent(qKeyEvent)



