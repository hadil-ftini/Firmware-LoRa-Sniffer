from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QGridLayout, QApplication
from PyQt5.QtCore import Qt, pyqtSignal, QSettings
from PyQt5.QtGui import QFont, QPixmap, QTransform
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QTransform

class VirtualKeyboard(QWidget):
    key_pressed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setRotation(90)


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

    def buttonClicked(self):
        button = self.sender()
        text = button.text()
        self.key_pressed.emit(text)
# Rotate the pixmap 90 degrees
        def paintEvent(self, event):
        painter = QPainter(self)
        painter.translate(self.width() / 2, self.height() / 2)  # Translation au centre du widget
        painter.rotate(90)
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
        # Rotate the pixmap 90 degrees
        transform = QTransform().rotate(90)
        rotated_pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)
        self.logo_label.setPixmap(rotated_pixmap)
        self.logo_label.setFixedSize(rotated_pixmap.size())

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

        # Connect the signal after initializing virtual keyboard
        self.virtual_keyboard.key_pressed.connect(self.handle_key_pressed1)

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

        settings = QSettings('login.ini', QSettings.IniFormat)
        correct_username = settings.value('Login/username')
        correct_password = settings.value('Login/password')

        if username == correct_username and password == correct_password:
            QMessageBox.information(self, "Login Successful", f"Welcome, {username}")
            self.switch_window.emit()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")

    def handle_key_pressed1(self, key):
        focused_widget = self.focusWidget()
        if isinstance(focused_widget, QLineEdit):
            if key == 'Back':
                current_text = focused_widget.text()
                focused_widget.setText(current_text[:-1])
            else:
                focused_widget.insert(key)
        elif isinstance(focused_widget, QPushButton) and focused_widget.text() == 'Back':
            if key == 'Back':
                current_text = focused_widget.text()
                if current_text:
                    focused_widget.setText(current_text[:-1])
        elif isinstance(self.entry_username, QLineEdit):
            self.entry_username.setFocus()
            self.entry_username.insert(key)
    def handle_key_pressed2(self, key):
        focused_widget = self.focusWidget()
        if isinstance(focused_widget, QLineEdit):
            if key == 'Back':
                current_text = focused_widget.text()
                focused_widget.setText(current_text[:-1])
            else:
                focused_widget.insert(key)
        elif isinstance(focused_widget, QPushButton) and focused_widget.text() == 'Back':
            if key == 'Back':
                current_text = focused_widget.text()
                if current_text:
                    focused_widget.setText(current_text[:-1])
        elif isinstance(self.entry_password, QLineEdit):
            self.entry_password.setFocus()
            self.entry_password.insert(key)
    def eventFilter(self, source, event):
        if event.type() == event.FocusIn:
            if source == self.entry_username:
                self.virtual_keyboard.key_pressed.disconnect()
                self.virtual_keyboard.key_pressed.connect(self.handle_key_pressed1)
            elif source == self.entry_password:
                self.virtual_keyboard.key_pressed.disconnect()
                self.virtual_keyboard.key_pressed.connect(self.handle_key_pressed2)
            self.virtual_keyboard.show()
        return super().eventFilter(source, event)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
