import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QMessageBox, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap
from lora_window import LoraValWindow 
class GeneralWindow(QWidget):
    def __init__(self, previous_window):
        super().__init__()
        self.setWindowTitle("General Window")
        self.setGeometry(100, 100, 400, 300)

        # Adjusting geometry for a 2.8 inch screen
        self.setGeometry(0, 0, 220, 320)

        # Logo
        self.logo_label = QLabel(self)
        self.logo_label.setGeometry(52, 10, 120, 120)
        pixmap = QPixmap('enterprise_logo.png')
        self.logo_label.setPixmap(pixmap)

        # Return button
        self.return_button = QPushButton("Return", self)
        self.return_button.clicked.connect(self.return_to_previous)


        self.reset_button = QPushButton("Reset", self)
        self.reset_button.clicked.connect(self.reset_parameters)

        # Layout for buttons below logo
        button_layout = QHBoxLayout()
        
        button_layout.addWidget(self.reset_button)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.return_button)  # Add return button at the top
        main_layout.addWidget(self.logo_label)  # Add logo label
        main_layout.addLayout(button_layout)  # Add buttons layout below logo
        self.setLayout(main_layout)

        self.previous_window = previous_window
    def reset_parameters(self):
        # Implement resetting parameters logic here
        print("Parameters reset")
        QMessageBox.information(self, "Reset", "Settings reset to default.")

    def return_to_previous(self):
        self.hide()
        self.previous_window.show()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    lora_window = LoraValWindow()
    general_window = GeneralWindow(lora_window)
    lora_window.general_window = general_window  # Pass reference to GeneralWindow to LoraValWindow
    general_window.show()
    sys.exit(app.exec_())