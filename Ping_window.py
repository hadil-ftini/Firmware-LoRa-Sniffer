import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit, QMessageBox
from PyQt5.QtGui import QTransform, QPixmap
from PyQt5.QtCore import Qt
from SX127x.LoRa import *
from SX127x.board_config import BOARD

POLYNOMIAL = 0x07

def start(self):          
        while True:
            while (self.var==0):
                print ("Send: INF")
                self.write_payload([255, 255, 0, 0, 73, 78, 70, 0]) # Send INF
                self.set_mode(MODE.TX)
                time.sleep(3) # there must be a better solution but sleep() works
                self.reset_ptr_rx()
                self.set_mode(MODE.RXCONT) # Receiver mode
                self.var=0
                self.reset_ptr_rx()
                self.set_mode(MODE.RXCONT) # Receiver mode
                time.sleep(10)

def calculate_crc8(data):
    crc = 0x00
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = (crc << 1) ^ POLYNOMIAL
            else:
                crc <<= 1
            crc &= 0xFF
    return crc

def send_frame(frame):
    print("Envoi de la trame LoRa:", frame.hex())
    return frame.hex()

def ping_frame(node_id, lora):
    payload = 0x00
    sniffer_addr = 0x00000000
    ping_frame_byte = 0x05
    
    frame = bytearray()
    frame.append(payload)
    frame.extend(sniffer_addr.to_bytes(4, byteorder='big'))
    frame.extend(int(node_id, 16).to_bytes(4, byteorder='big'))
    frame.append(ping_frame_byte)

    crc = calculate_crc8(frame)
    frame.append(crc)

    return send_frame(frame)

class MyLoRa(LoRa):
    def __init__(self, parameters, packet_callback):
        super(MyLoRa, self).__init__(parameters)
        self.packet_callback = packet_callback

    def on_rx_done(self):
        payload = self.read_payload(nocheck=True)
        packet_hex = bytes(payload).hex()
        print("Paquet reçu : {}".format(packet_hex))
        self.packet_callback(packet_hex)
        self.clear_irq_flags(RxDone=1)
        self.set_mode(MODE.SLEEP)
        self.set_mode(MODE.RXCONT)
        
class PingTestWindow(QWidget):
    
    class PingTestWindow(QWidget):
    
     def __init__(self):
        super().__init__()
        transform = QTransform().rotate(180)
        pixmap = QPixmap()  # Create a QPixmap instance
        rotated_pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)
        self.logo_label = QLabel()  # Create the QLabel instance
        self.logo_label.setPixmap(rotated_pixmap)
        self.logo_label.setFixedSize(rotated_pixmap.size())
        self.setWindowTitle("Ping Pong Test")
        self.setGeometry(0, 0, 800, 480)
         
        self.setup_ui()
        self.lora = self.setup_lora()
        self.lora.packet_callback = self.update_packet_display
        self.update_signal_values()  
        self.ping_start_time = None


    def setup_lora(self):
        BOARD.setup()
        BOARD.reset()
        lora = LoRa()
        lora.set_pa_config(pa_select=1, max_power=21, output_power=17)
        lora.set_bw(BW.BW125)
        lora.set_coding_rate(CODING_RATE.CR4_7)
        lora.set_spreading_factor(9)
        lora.set_rx_crc(True)
        lora.set_low_data_rate_optim(True)
        return lora

    def setup_ui(self):
        self.title_label = QLabel("Node ID (HEX) ", self)
        self.title_label.setAlignment(Qt.AlignCenter)

        button_layout_top = QHBoxLayout()
        for i in range(8):
            increment_button = QPushButton('▲')
            increment_button.clicked.connect(lambda state, index=i: self.increment_hex(index))
            increment_button.setFixedSize(15, 15)
            button_layout_top.addWidget(increment_button)
       
        hex_input_layout = QHBoxLayout()
        self.hex_inputs = []
        for _ in range(8):
            hex_input = QLineEdit('0')
            hex_input.setMaximumSize(100, 20)  
            hex_input.setMinimumSize(100, 20)
            hex_input.textChanged.connect(self.update_node_id)
            hex_input_layout.addWidget(hex_input)
            self.hex_inputs.append(hex_input)

        button_layout_bottom = QHBoxLayout()
        for i in range(8):
            decrement_button = QPushButton('▼')
            decrement_button.clicked.connect(lambda state, index=i: self.decrement_hex(index))
            decrement_button.setFixedSize(15, 15)
            button_layout_bottom.addWidget(decrement_button)

        signal_layout = QHBoxLayout()

        self.rssi_label = QLabel("RSSI:")
        self.rssi_value_label = QLabel("")  

        self.snr_label = QLabel("SNR:")
        self.snr_value_label = QLabel("")

        signal_layout.addWidget(self.rssi_label)
        signal_layout.addWidget(self.rssi_value_label)
        signal_layout.addWidget(self.snr_label)
        signal_layout.addWidget(self.snr_value_label)

        self.lora_frame_label = QLabel("Packet RX(hex):")
        self.read_payload_value = QLabel("")
        signal_layout.addWidget(self.read_payload_value)

        self.time_label = QLabel("Rx Time (ms): ")
        self.elapsed_time_label = QLabel("")

        ping_button = QPushButton("PING")
        ping_button.clicked.connect(self.start_ping)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_parameters)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title_label)
        main_layout.addLayout(button_layout_top)
        main_layout.addLayout(hex_input_layout)
        main_layout.addLayout(button_layout_bottom)
        main_layout.addLayout(signal_layout)
        main_layout.addWidget(self.lora_frame_label)
        main_layout.addWidget(self.time_label)
        main_layout.addWidget(self.elapsed_time_label)
        main_layout.addWidget(ping_button)
        main_layout.addWidget(save_button)
       
        self.setLayout(main_layout)

    def update_node_id(self):
        node_id = ''.join([hex_input.text() for hex_input in self.hex_inputs])
        self.title_label.setText(f"Node ID: {node_id}")

    def increment_hex(self, index):
        current_value = int(self.hex_inputs[index].text(), 16)
        new_value = (current_value + 1) % 16
        self.hex_inputs[index].setText(hex(new_value)[2:].upper())

    def decrement_hex(self, index):
        current_value = int(self.hex_inputs[index].text(), 16)
        new_value = (current_value - 1) % 16
        self.hex_inputs[index].setText(hex(new_value)[2:].upper())

    
    def start_ping(self):
        self.ping_start_time = time.time()  # Record the time when PING button is clicked
        self.ping()

    def ping(self):
        node_id = ''.join([hex_input.text() for hex_input in self.hex_inputs])
        packet_hex = ping_frame(node_id, self.lora)
        self.elapsed_time = time.time() - self.ping_start_time  # Update elapsed_time
        self.elapsed_time_label.setText(f"{self.elapsed_time:.2f}")
        if self.elapsed_time > 60:  # Use self.elapsed_time instead of elapsed_time
            QMessageBox.warning(self, "Warning", "Time Out")
    def save_parameters(self):
        node_id = ''.join([hex_input.text() for hex_input in self.hex_inputs])
        rssi_value = self.rssi_value_label.text()
        snr_value = self.snr_value_label.text()
        try:
            with open("save.txt", 'w') as file:
                file.write(f"Node ID: {node_id}\n")
                file.write(f"RSSI: {rssi_value}\n")
                file.write(f"SNR: {snr_value}\n")
            
            QMessageBox.information(self, "Success", "Parameters saved successfully.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save parameters:\n{str(e)}")

    def update_signal_values(self):
    # Update RSSI and SNR values
        rssi_value = self.lora.get_pkt_rssi_value()
        snr_value = self.lora.get_pkt_snr_value()
        self.rssi_value_label.setText(str(rssi_value))  
        self.snr_value_label.setText(str(snr_value))  

    def update_packet_display(self, packet_hex):
    # Update the display with the received packet
        self.read_payload_value.setText("Paquet reçu : {}".format(packet_hex))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PingTestWindow()
    window.show()
    sys.exit(app.exec_())
