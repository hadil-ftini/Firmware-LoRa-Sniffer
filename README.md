"# Firmware-LoRa-Sniffer" 
This project aims to develop specialized firmware for a LoRa sniffer using an RFM96/98 LoRa module coupled with a Raspberry Pi card. The goal is to create a graphical interface to interact with the LoRa module, configure its parameters, send packets, and analyze received data with signal quality indicators such as RSSI (Received Signal Strength Indicator) and SNR (Signal-to-Noise Ratio), as well as packet reception time (time rx).
1.Hardware :
Raspberry pi 3B+	LoRa RFM96/98
3.3V 	                3.3V
GND                  	GND
MOSI GPIO10         	MOSI 
MISO GPIO9	          MISO
SCK GPIO11	          SCK
GPIO8 	          NSS/Activer
GPIO4	               DIO 0
GPIO22	              RST
2.Firmware development:
Creation of firmware to manage communication between the Raspberry Pi and the LoRa module.
Implemented features to configure LoRa settings, send and receive packets.
3.GUI development:
Development of a graphical user interface (GUI) to interact with the LoRa module.
The GUI should allow configuring LoRa settings, sending packets, and displaying received data with signal quality indicators (RSSI, SNR) and reception time.Data analysis and display:
4.Data analysis and display:
Implementation of mechanisms to analyze LoRa packets captured by the sniffer.View analysis results, including signal quality measurements and reception time.
