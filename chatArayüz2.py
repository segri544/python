import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton
from PyQt5.QtSerialPort import QSerialPort

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
        self.com_port_combo.addItems(["com3", "com4", "com5"])
        self.settings_layout.addWidget(self.com_port_combo)

        # Create connect button
        self.connect_button = QPushButton("Connect")
        self.settings_layout.addWidget(self.connect_button)
        self.connect_button.clicked.connect(self.connect_to_port)

        # Create serial port object
        self.serial_port = QSerialPort()

    def connect_to_port(self):
        # Get selected baudrate and com port
        baudrate = int(self.baudrate_combo.currentText())
        com_port = self.com_port_combo.currentText()

        # Set baudrate and com port for serial port
        self.serial_port.setBaudRate(baudrate)
        self.serial_port.setPortName(com_port)

        # Open serial port
        self.serial_port.open(QSerialPort.ReadOnly)

        # Connect data ready signal to update data function
        self.serial_port.readyRead.connect(self.update_data)

    def update_data(self):
        # Read data from serial port
        data = self.serial_port.readAll()
        data = data.data().decode("utf-8")

        # Split data into variables
        data = data.split(",")
        altitude = data[0]
        speed = data[1]
        battery = data[2]

        # Update labels with new data
        self.altitude_label.setText("Altitude: " +altitude)
        self.speed_label.setText("Speed: " + speed)
        self.battery_label.setText("Battery: " + battery)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DroneDataWindow()
    window.show()
    sys.exit(app.exec_())
