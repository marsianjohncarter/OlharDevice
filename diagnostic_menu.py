import os
from time import sleep
from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation
from PyQt5.QtGui import QPixmap, QFont
import qrcode
import requests
from services import Services
from video_player import VideoPlayer
import logging
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QScrollArea
import shutil
import psutil 


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
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Menu')
        self.setGeometry(400, 400, 700, 500)
        self.logs_window = None
        default_font = QFont()
        default_font.setBold(True)
        layout = QVBoxLayout()

        
        self.logs_btn = QPushButton(text='Open Logs')
        self.logs_btn.clicked.connect(self.openLogs)
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

        layout.addWidget(self.logs_btn)
        layout.addWidget(self.storage_label)
        layout.addWidget(self.cpu_util_label)
        layout.addWidget(self.updateBtn)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def openLogs(self):
        if not self.logs_window:
            self.logs_window = logWindow()
        self.logs_window.show()

    def closeLogs(self):
        if self.logs_window:
            self.logs_window.hide()
        self.logs_window = None

    def getStorageInfo(self):
        total, used, free = shutil.disk_usage("/")
        return {'total':total % (total // (2**30)), 'used':used % (used // (2**30)), 'free':free % (free // (2**30))}
    
    def getCpuInfo(self):
        return f"CPU utilization: {psutil.cpu_percent()}%"
    
    def updateMenu(self):
        storage_info = self.getStorageInfo()
        self.storage_label.setText(f'Storage: \nTotal: {storage_info["total"]}GB | Used: {storage_info["used"]}GB | Free: {storage_info["free"]}GB')
        self.cpu_util_label.setText(f'{self.getCpuInfo()}')

