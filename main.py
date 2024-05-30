import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtWidgets import QApplication
from login_window import LoginWindow  
from setting_interface import TestInterface
from lora_window import LoraValWindow
from general_window import GeneralWindow
from Ping_window import PingTestWindow

class Controller:
    def __init__(self):
        vbox = QVBoxLayout()
        self.setLayout(vbox)
        self.login_window = LoginWindow()
        self.setting_interface = TestInterface(self.login_window)
        self.lora_window = LoraValWindow(self.setting_interface)
        self.general_window = GeneralWindow(self.setting_interface)
        self.ping_window = None
        self.result_window = None

        self.login_window.switch_window.connect(self.show_rf_interface)
        self.setting_interface.switch_lora_window.connect(self.show_lora_window)
        self.setting_interface.switch_general_window.connect(self.show_general_window)
        self.setting_interface.switch_ping_pong_window.connect(self.show_ping_window)

    def show_login_window(self):
        self.setting_interface.hide()
        self.login_window.show()

    def show_rf_interface(self):
        self.login_window.hide()
        self.setting_interface.show()

    def show_lora_window(self):
        self.setting_interface.hide()
        self.lora_window.show()

    def show_general_window(self):
        self.setting_interface.hide()
        self.general_window.show()

    def show_ping_window(self):
        self.setting_interface.hide()
        self.ping_window = PingTestWindow()
        self.ping_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller()
    controller.show_login_window()
    sys.exit(app.exec_())
