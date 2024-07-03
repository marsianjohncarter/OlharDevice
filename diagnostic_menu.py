import os
from time import sleep
from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation, QTime, pyqtSignal
from PyQt5.QtGui import QFont
from services import Services
import logging
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QScrollArea
import shutil
import psutil 

ASSETS_FOLDER = "./assets"

# TODO: Add parent class for all widgets
class dataWindow(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Logs')
        self.setGeometry(400, 400, 700, 500)
        self.setStyleSheet("background-color: black;") 

        self.data = 'None'
        self.openData(f'{ASSETS_FOLDER}/data/video_data.json')

        self.json_label = QLabel(text=f'{self.data}')
        self.json_label.setStyleSheet('color: white')

        self.update_data_btn = QPushButton(text='Update data')
        self.update_data_btn.clicked.connect(lambda: self.updateJsonLabel(f'{ASSETS_FOLDER}/data/video_data.json'))
        self.update_data_btn.setStyleSheet('background-color: white')

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(self.update_data_btn)
        layout.addWidget(self.json_label)

        widget = QWidget()
        widget.setLayout(layout)
        self.setWidget(widget)
        self.setWidgetResizable(True)



    def openData(self, file):
        with open(file, 'r') as txt:
            list_of_lines = txt.read() 
        self.data = list_of_lines
    
    def updateJsonLabel(self, file):
        with open(file, 'r') as txt:
            list_of_lines = txt.read() 
        self.json_label.setText(list_of_lines)

class logWindow(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Logs')
        self.setGeometry(400, 400, 700, 500)
        self.setStyleSheet("background-color: black;") 

        self.logs = 'Test'
        self.openLogs('./dev.log')

        self.logs_label = QLabel(text=f'{self.logs}')
        self.logs_label.setStyleSheet('color: white')

        self.updateLogsBtn = QPushButton(text='Update Logs')
        self.updateLogsBtn.clicked.connect(lambda: self.updateLogLabel('./dev.log'))
        self.updateLogsBtn.setStyleSheet('background-color: white')

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(self.updateLogsBtn)
        layout.addWidget(self.logs_label)

        widget = QWidget()
        widget.setLayout(layout)

        # self.setCentralWidget(widget)
        

        self.setWidget(widget)
        self.setWidgetResizable(True)



    def openLogs(self, file):
        with open(file, 'r') as txt:
            list_of_lines = txt.read() 
        self.logs = list_of_lines
    
    def updateLogLabel(self, file):
        with open(file, 'r') as txt:
            list_of_lines = txt.read() 
        self.logs_label.setText(list_of_lines)

class Menu(QMainWindow):
    sig = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Menu')
        self.setGeometry(400, 400, 700, 500)
        self.logs_window = None
        self.json_window = None



        default_font = QFont()
        default_font.setBold(True)
        layout = QVBoxLayout()

        
        self.logs_btn = QPushButton(text='Open Logs')
        self.logs_btn.clicked.connect(self.openLogs)        
        self.json_btn = QPushButton(text='Open Company Data')
        self.json_btn.clicked.connect(self.openJson)
        storage_info = self.getStorageInfo()
        self.storage_label = QLabel(text=f'Storage: \nTotal: {storage_info["total"]}GB | Used: {storage_info["used"]}GB | Free: {storage_info["free"]}GB')
        self.storage_label.setStyleSheet("font-size: 15px;")
        self.storage_label.setAlignment(Qt.AlignCenter)
        self.storage_label.setFont(default_font)

        self.cpu_util_label = QLabel(text=f'{self.getCpuInfo()}')
        self.cpu_util_label.setAlignment(Qt.AlignCenter)
        self.cpu_util_label.setFont(default_font)
        self.cpu_util_label.setStyleSheet("font-size: 15px;")

        self.updateBtn = QPushButton(text='Update Menu')
        self.updateBtn.clicked.connect(self.updateMenu)

        layout.addWidget(self.json_btn)
        layout.addWidget(self.logs_btn)
        layout.addWidget(self.storage_label)
        layout.addWidget(self.cpu_util_label)
        layout.addWidget(self.updateBtn)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.timer = QTimer(self)

        self.timer.timeout.connect(self.updateMenu)
        self.timer.start(1000)
        

    def openLogs(self):
        if not self.logs_window:
            self.logs_window = logWindow()
            self.logs_window.show()
        else:
            self.logs_window.hide()
            self.logs_window= None
    
    def openJson(self):
        if not self.json_window:
            self.json_window = dataWindow()
            self.json_window.show()
        else:
            self.json_window.hide()
            self.json_window = None

    def getStorageInfo(self):
        total, used, free = shutil.disk_usage("/")
        return {'total':total % (total // (2**30)), 'used':used % (used // (2**30)), 'free':free % (free // (2**30))}
    
    def getCpuInfo(self):
        return f"CPU utilization: {psutil.cpu_percent()}%"

    def updateMenu(self):
        storage_info = self.getStorageInfo()
        self.storage_label.setText(f'Storage: \nTotal: {storage_info["total"]}GB | Used: {storage_info["used"]}GB | Free: {storage_info["free"]}GB')
        self.cpu_util_label.setText(f'{self.getCpuInfo()}')
    
    def closeEvent(self, event):
        self.sig.emit() # type: ignore



