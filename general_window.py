import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import Qt, QRect
from lora_window import LoraValWindow

class GeneralWindow(QWidget):
    def __init__(self, previous_window):
        super().__init__()
        vbox = QVBoxLayout()
        self.setLayout(vbox)
        
        # Logo
        self.logo_label = QLabel(self)
        pixmap = QPixmap('enterprise_logo.png')
        self.logo_label.setPixmap(pixmap)

        # Transform the logo
        transform = QTransform().rotate(180)
        rotated_pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)
        self.logo_label.setPixmap(rotated_pixmap)
        self.logo_label.setFixedSize(rotated_pixmap.size())

        self.setWindowTitle("General Window")
        self.setGeometry(100, 100, 400, 300)

        # Adjusting geometry for a 2.8 inch screen
        self.setGeometry(0, 0, 800, 480)

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

        self.rotate_interface()

    def rotate_interface(self):
        # Get the current geometry
        rect = self.geometry()

        # Rotate and reposition the widgets
        for widget in self.findChildren(QWidget):
            widget_rect = widget.geometry()
            new_x = rect.width() - widget_rect.x() - widget_rect.width()
            new_y = rect.height() - widget_rect.y() - widget_rect.height()
            new_widget_rect = QRect(new_x, new_y, widget_rect.width(), widget_rect.height())
            widget.setGeometry(new_widget_rect)

        # Adjust main layout to the new geometry
        self.setLayout(self.layout())

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
