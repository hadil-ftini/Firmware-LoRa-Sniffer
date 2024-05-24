import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QMainWindow, QComboBox, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from SX127x.LoRa import *
from SX127x.board_config import BOARD
class LoraValWindow(QMainWindow):
    def __init__(self, previous_window=None):
        super().__init__()
        self.setWindowTitle("LoRa Setup")
        self.previous_window = previous_window
        self.setup_ui()

    def setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.logo_label = QLabel(self)
        self.logo_label.setGeometry(52, 40, 120, 120)
        pixmap = QPixmap('enterprise_logo.png')  
        self.logo_label.setPixmap(pixmap)
        self.layout.addWidget(self.logo_label)
        self.setGeometry(0, 0, 220, 320)
        self.setMinimumSize(220, 320)  


        # QLabel for Frequency
        self.freq_label = QLabel("Frequency (MHz):", self)
        self.layout.addWidget(self.freq_label)

        # QComboBox for Frequency
        self.freq_input = QComboBox(self)
        self.freq_input.addItems(["434", "869" ,"915"])
        self.layout.addWidget(self.freq_input)

        # QComboBox for Bandwidth
        self.bw_label = QLabel("Bandwidth:", self)
        self.bw_input = QComboBox(self)
        self.bw_input.addItems(["1", "2", "3", "4"])
        self.layout.addWidget(self.bw_label)
        self.layout.addWidget(self.bw_input)

        # QComboBox for Spreading Factor
        self.sf_label = QLabel("Spreading Factor:", self)
        self.sf_input = QComboBox(self)
        self.sf_input.addItems(["7", "8", "9", "10", "11", "12"])
        self.layout.addWidget(self.sf_label)
        self.layout.addWidget(self.sf_input)

        # QComboBox for Coding Rate
        self.cr_label = QLabel("Coding Rate:", self)
        self.cr_input = QComboBox(self)
        self.cr_input.addItems(["1", "2", "3", "4", "5"])
        self.layout.addWidget(self.cr_label)
        self.layout.addWidget(self.cr_input)

        self.setup_lora_button = QPushButton("Set LoRa")
        self.setup_lora_button.clicked.connect(self.setup_lora)
        self.layout.addWidget(self.setup_lora_button)

        # Return Button
        self.return_button = QPushButton("Return", self)
        self.return_button.clicked.connect(self.return_to_previous)
        self.layout.addWidget(self.return_button)

        # Save Button
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_parameters)
        self.layout.addWidget(self.save_button)

    def setup_lora(self):
        freq = int(self.freq_input.currentText())
        bw_index = self.bw_input.currentIndex()  # Get the index of the selected item
        bw_values = [1, 2, 3, 4]  # Corresponding values for the bandwidth options
        bw = bw_values[bw_index]  # Retrieve the value based on the index
        sf = int(self.sf_input.currentText())  # Get the currently selected spreading factor
        cr = int(self.cr_input.currentText())  # Get the currently selected coding rate
        
        BOARD.setup()
        lora = LoRa()
        lora.set_mode(MODE.STDBY)
        lora.set_freq(freq)
        lora.set_modem_config_1(bw=bw, coding_rate=cr)
        lora.set_modem_config_2(spreading_factor=sf)
        BOARD.teardown()

    def save_parameters(self):
        freq = self.freq_input.currentText()
        bw = self.bw_input.currentText()  # Get the currently selected bandwidth
        sf = self.sf_input.currentText()  # Get the currently selected spreading factor
        cr = self.cr_input.currentText()  # Get the currently selected coding rate

        parameters_string = f"Frequency: {freq}\nBandwidth: {bw}\nSpreading Factor: {sf}\nCoding Rate: {cr}\n"

        with open("lora_val.ini", "w") as f:
            f.write(parameters_string)

        QMessageBox.information(self, "Saved", "Parameters saved to lora_val.ini")

    def return_to_previous(self):
        if self.previous_window:
            self.hide()
            self.previous_window.show()

    def reset_parameters(self):
        # Resetting parameters to default values
        self.freq_input.setCurrentIndex(0)
        self.bw_input.setCurrentIndex(0)
        self.sf_input.setCurrentIndex(0)
        self.cr_input.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoraValWindow()
    window.show()
    sys.exit(app.exec_())
