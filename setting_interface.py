from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QGridLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QTransform,QPixmap
from PyQt5.QtGui import QFont, QPixmap

class TestInterface(QWidget):
    switch_ping_pong_window = pyqtSignal()
    switch_lora_window = pyqtSignal()
    switch_general_window = pyqtSignal()

    def __init__(self, previous_window):
        super().__init__()
        self.setWindowTitle("Setting Test Interface")
        self.setGeometry(100, 100, 400, 300)

        # Adjusting geometry for a 2.8 inch screen
        self.setGeometry(0, 0, 800, 480)
        

        # Logo
        self.logo_label = QLabel(self)
        pixmap = QPixmap('enterprise_logo.png')
        self.logo_label.setPixmap(pixmap)

        # Title Label
        self.title_label = QLabel("Setting Interface", self)
        self.title_label.setFont(QFont('Helvetica', 16))
        self.title_label.setAlignment(Qt.AlignCenter)

        # Buttons
        self.button1 = QPushButton("PING PONG", self)
        self.button1.clicked.connect(self.open_Ping_window)

        self.button2 = QPushButton("LoRa", self)
        self.button2.clicked.connect(self.open_lora_window)

        self.button3 = QPushButton("Generale", self)
        self.button3.clicked.connect(self.open_general_window)



        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.logo_label)
        layout.addWidget(self.title_label)
        
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.button1, 0, 0)
        grid_layout.addWidget(self.button2, 1, 0)
        grid_layout.addWidget(self.button3, 2, 0)
        layout.addLayout(grid_layout)
        
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

    def open_Ping_window(self):
        self.switch_ping_pong_window.emit()  

    def open_lora_window(self):
        self.switch_lora_window.emit()

    def open_general_window(self):
        self.switch_general_window.emit()
    
        transform = QTransform().rotate(90)
        rotated_pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)
        self.logo_label.setPixmap(rotated_pixmap)
        self.logo_label.setFixedSize(rotated_pixmap.size())
    