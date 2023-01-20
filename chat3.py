import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton
import serial.tools.list_ports
import serial

class DroneDataWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drone Data")

        # Create layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Create labels to display data
        self.altitude_label = QLabel("Altitude: N/A")
        self.speed_label = QLabel("Speed: N/A")
        self.battery_label = QLabel("Battery: N/A")
        self.layout.addWidget(self.altitude_label)
        self.layout.addWidget(self.speed_label)
        self.layout.addWidget(self.battery_label)

        # Create layout for baudrate and com port selection
        self.settings_layout = QHBoxLayout()
        self.layout.addLayout(self.settings_layout)

        # Create baudrate combo box
        self.baudrate_combo = QComboBox()
        self.baudrate_combo.addItems(["9600", "115200", "230400"])
        self.settings_layout.addWidget(self.baudrate_combo)

        # Create com port combo box
        self.com_port_combo = QComboBox()
        self.settings_layout.addWidget(self.com_port_combo)

        # Create connect button
        self.connect_button = QPushButton("Connect")
        self.settings_layout.addWidget(self.connect_button)
        self.connect_button.clicked.connect(self.connect_to_port)
        
        # Create disconnect button
        self.disconnect_button = QPushButton("Disconnect")
        self.settings_layout.addWidget(self.disconnect_button)
        self.disconnect_button.clicked.connect(self.disconnect_from_port)

        # populate available com ports
        self.populate_com_ports()
        self.serial_port = None

    def populate_com_ports(self):
        # Clear any existing items in the combo box
        self.com_port_combo.clear()

        # Get a list of all available serial ports
        available_ports = list(serial.tools.list_ports.comports())

        # Add the names of the available ports to the combo box
        for port in available_ports:
            self.com_port_combo.addItem(port.device)
    
    def connect_to_port(self):
        # Get selected baudrate and com port
        baudrate = int(self.baudrate_combo.currentText())
        com_port = self.com_port_combo.currentText()
        print(f"Selected baudrate: {baudrate}")
        print(f"Selected com port: {com_port}")
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        self.serial_port = serial.Serial(com_port, baudrate)
        # Connect data ready signal to update data function
        self.update_data()

    def disconnect_from_port(self):
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
    
    def update_data(self):
        if self.serial_port and self.serial_port.is_open:
            # Read data from serial port
            data = self.serial_port.readline()
            data = data.decode("utf-8")

            # Split data into variables
            data = data.split(",")
            altitude = data[0]
            speed = data[1]
            battery = data[2]

            # Update labels with new data
            self.altitude_label.setText("Altitude: " + altitude)
            self.speed_label.setText("Speed: " + speed)
            self.battery_label.setText("Battery: " + battery)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DroneDataWindow()
    window.show()
    sys.exit(app.exec_())
