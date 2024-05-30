from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QGridLayout, QApplication
from PyQt5.QtCore import Qt, pyqtSignal, QSettings
from PyQt5.QtGui import QFont, QPixmap, QPainter

class VirtualKeyboard(QWidget):
    key_pressed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QGridLayout()

        buttons = [
            ('q', 0, 0), ('w', 0, 1), ('e', 0, 2), ('r', 0, 3), ('t', 0, 4),
            ('y', 0, 5), ('u', 0, 6), ('i', 0, 7), ('o', 0, 8), ('p', 0, 9),
            ('a', 1, 0), ('s', 1, 1), ('d', 1, 2), ('f', 1, 3), ('g', 1, 4),
            ('h', 1, 5), ('j', 1, 6), ('k', 1, 7), ('l', 1, 8), ('z', 2, 0),
            ('x', 2, 1), ('c', 2, 2), ('v', 2, 3), ('b', 2, 4), ('n', 2, 5),
            ('m', 2, 6),
        ]

        for text, row, col in buttons:
            button = QPushButton(text)
            button.clicked.connect(self.buttonClicked)
            button.setFixedSize(20, 20)  # Adjust the button size as necessary
            layout.addWidget(button, row, col)

        back_button = QPushButton('Back')
        back_button.clicked.connect(self.buttonClicked)
        back_button.setFixedSize(40, 20)  # Set a different size for the "Back" button
        layout.addWidget(back_button, 2, 7, 1, 2)  # Span across multiple columns

        self.setLayout(layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.translate(self.width() / 2, self.height() / 2)  # Translation au centre du widget
        painter.rotate(90)  # Rotation de 90 degrés

    def buttonClicked(self):
        button = self.sender()
        text = button.text()
        self.key_pressed.emit(text)

class LoginWindow(QWidget):
    switch_window = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Page")
        self.setGeometry(0, 0, 800, 480)

        # Logo
        self.logo_label = QLabel(self)
        self.logo_label.setGeometry(52, 10, 120, 120)
        pixmap = QPixmap('enterprise_logo.png')
        self.logo_label.setPixmap(pixmap)

        self.title_label = QLabel("Irwise Data Logger", self)
        self.title_label.setFont(QFont('Helvetica', 16))
        self.title_label.setAlignment(Qt.AlignCenter)

        self.label_username = QLabel("Username:", self)
        self.label_password = QLabel("Password:", self)

        self.entry_username = QLineEdit(self)
        self.entry_password = QLineEdit(self)
        self.entry_password.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login)

        # Virtual keyboard
        self.virtual_keyboard = VirtualKeyboard()
        self.virtual_keyboard.key_pressed.connect(self.handle_key_pressed)

        # Show virtual keyboard when focused
        self.entry_username.installEventFilter(self)
        self.entry_password.installEventFilter(self)

        # Layouts
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.logo_label)
        input_layout.addWidget(self.title_label)
        input_layout.addWidget(self.label_username)
        input_layout.addWidget(self.entry_username)
        input_layout.addWidget(self.label_password)
        input_layout.addWidget(self.entry_password)
        input_layout.addWidget(self.login_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.virtual_keyboard)

        self.setLayout(main_layout)

        # Load login after creating the widgets
        self.load_login()

    def load_login(self):
        settings = QSettings('login.ini', QSettings.IniFormat)
        # Ensure the fields are empty
        self.entry_username.setText('')
        self.entry_password.setText('')

    def login(self):
        username = self.entry_username.text()
        password = self.entry_password.text()

    def handle_key_pressed(self, key):
        focused_widget = self.focusWidget
