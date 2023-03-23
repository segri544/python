import sys
import serial
import struct
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton,QLineEdit
import serial.tools.list_ports
import serial
import threading
import json
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
import datetime
import time
current_time = datetime.datetime.now().strftime("%H_%M_%S")
logFile=current_time+".txt"


# create new empty txt file to save data
with open(logFile, 'w', encoding='utf-8') as f:
  pass

UpdateTimer=0.05



# create new empty txt file to save data

def get_coordinates():
    # read json file
    with open("map.geojson", "r") as json_file:
        data = json.load(json_file)

    # get coordinates information
    coordinates = data["features"][0]["geometry"]["coordinates"]

    # convert coordinates to tuple
    coordinates_tuple = tuple(coordinates)
    
    # print(coordinates_tuple)
    return coordinates_tuple

class DroneDataWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drone Data")

        # Create layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Create labels to display data
        self.unlem_label = QLabel("unlem: N/A")
        self.status_label = QLabel("status: N/A")
        self.motor1_label = QLabel("motor1: N/A")
        self.motor2_label = QLabel("motor2: N/A")
        self.motor3_label = QLabel("motor3: N/A")
        self.motor4_label = QLabel("motor4: N/A")
        self.battery_label = QLabel("battery: N/A")
        self.roll_label = QLabel("roll: N/A")
        self.pitch_label = QLabel("pitch: N/A")
        self.yaw_label = QLabel("yaw: N/A")
        self.altitude_label = QLabel("altitude: N/A")
        self.longtitude_label = QLabel("Longtitude: N/A")
        self.latitude_label = QLabel("Latitude: N/A")
        

        self.layout.addWidget(self.unlem_label)
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.motor1_label)
        self.layout.addWidget(self.motor2_label)
        self.layout.addWidget(self.motor3_label)
        self.layout.addWidget(self.motor4_label)
        self.layout.addWidget(self.battery_label)
        self.layout.addWidget(self.roll_label)
        self.layout.addWidget(self.pitch_label)
        self.layout.addWidget(self.yaw_label)
        self.layout.addWidget(self.altitude_label)
        self.layout.addWidget(self.longtitude_label)
        self.layout.addWidget(self.latitude_label)
        

        # add layout for buttons and input lines
        self.settings_layout = QHBoxLayout()
        self.layout.addLayout(self.settings_layout)
        self.pid_layout=QHBoxLayout()
        self.layout.addLayout(self.pid_layout)
        self.send_pid_layout=QHBoxLayout()
        self.layout.addLayout(self.send_pid_layout)
        self.map_layout=QHBoxLayout()
        self.layout.addLayout(self.map_layout)

        # Create layout for baudrate and com port selection
        # Create baudrate combo box
        self.baudrate_combo = QComboBox()
        self.baudrate_combo.addItems(["9600", "115200", "230400"])
        self.settings_layout.addWidget(self.baudrate_combo)

        # Create com port combo box
        self.com_port_combo = QComboBox()
        self.settings_layout.addWidget(self.com_port_combo)

        # Create connect button"
        self.connect_button = QPushButton("Connect")
        self.settings_layout.addWidget(self.connect_button)
        self.connect_button.clicked.connect(self.connect_to_port)
        
        # Create disconnect button
        self.disconnect_button = QPushButton("Disconnect")
        self.settings_layout.addWidget(self.disconnect_button)
        self.disconnect_button.clicked.connect(self.disconnect_from_port)
        
        
        # create PİD VALUES and send pid values  
        self.kp_label = QLabel("Kp:")
        self.ki_label = QLabel("Ki:")
        self.kd_label = QLabel("Kd:")
        self.linekp = QLineEdit(self)
        self.lineki = QLineEdit(self)
        self.linekd = QLineEdit(self)
        self.pid_layout.addWidget(self.kp_label)
        self.pid_layout.addWidget(self.linekp)
        self.pid_layout.addWidget(self.ki_label)
        self.pid_layout.addWidget(self.lineki)
        self.pid_layout.addWidget(self.kd_label)
        self.pid_layout.addWidget(self.linekd)
        self.send_pid_button = QPushButton("Send PID Parameters")
        self.send_pid_layout.addWidget(self.send_pid_button)
        self.send_pid_button.clicked.connect(self.send_pid_values)

        # Create stop motors button
        self.stop_motors_button = QPushButton("Stop Motors")
        self.layout.addWidget(self.stop_motors_button)
        self.stop_motors_button.clicked.connect(self.stop_motors)

        # populate available com ports
        self.populate_com_ports()
        self.serial_port = None

        # Create send the path button

        self.send_path_button = QPushButton("Send The Path")
        self.map_layout.addWidget(self.send_path_button)
        self.send_path_button.clicked.connect(self.send_path)

        # Create open map button
        self.open_map_button = QPushButton("Open Map")
        self.map_layout.addWidget(self.open_map_button)
        self.open_map_button.clicked.connect(self.open_map)

        self.update_timer = threading.Timer(1, self.update_data)
        self.update_timer.start()

    def send_pid_values(self):
        if self.serial_port and self.serial_port.is_open:
            # Send "stop motors" command
            print(f'PID values send...')
            i_am_sending_pid_command=34                                                      # as it is wanted by Şahin K.
            package=struct.pack('<Hfff',i_am_sending_pid_command,float(self.linekp.text()),float(self.lineki.text()),float(self.linekd.text()))   #totalde 2+4*3=16 byte
            print(package)
            self.serial_port.write(package)
           #H uint16 <-----> h int16

    def open_map(self):
        # Create a QWebEngineView and set the URL to geojson.io
        self.web_view = QWebEngineView(self)
        self.web_view.load(QUrl("https://geojson.io"))
        # Set the size of the web view
        self.web_view.resize(1500, 850)
        self.web_view.move(self.frameGeometry().topRight() - self.web_view.rect().topRight())
        # Show the web view
        self.web_view.show()

    def stop_motors(self):
        if self.serial_port and self.serial_port.is_open:
            # Send "stop motors" command
            i_am_sending_stop_motor_command=33  # as it is wanted by Şahin K.
            package=struct.pack('<H',i_am_sending_stop_motor_command)    #2byte
            print("Motor Stop Send")
            print(package)
            self.serial_port.write(package)

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

   # MAVİ EKRAN HATASI deneme1
    def closeEvent(self,event):
        self.disconnect_from_port()
        print('Window is closing!')


    def update_data(self):
        if self.serial_port and self.serial_port.is_open:
            raw = self.serial_port.read(32)
            if len(raw) == 32:
                data = struct.unpack('<HHHHHHHhhhHIIh', raw)
                #print(data)
                unlem= str(data[0])
                if unlem!="33":
                    self.disconnect_from_port()
                    time.sleep(1)
                    self.connect_to_port()
                
                status = str(data[1])
                motor1 = str(data[2])
                motor2= str(data[3])
                motor3 = str(data[4])
                motor4 = str(data[5])
                batarya = str(data[6])
                roll = str(data[7]/100.0)
                pitch = str(data[8]/100.0)
                yaw = str(data[9]/100.0)
                altitude = str(data[10]/10.0)
                longtitude=str(data[11]/(1.0**6))    # gönderirken çarptıgına böl
                latitude=str(data[12]/(1.0**6))      # gönderirken çarptıgına böl
                bos=str(data[13])               # son 2byte bosluk var
            
            # open the text file for writing
            with open(logFile, 'a',encoding='utf-8') as f:
                # write the data to the file
                f.write("unlem: "+unlem+" status: "+status+" motor1: "+motor1+" motor2: "+motor2+" motor3: "+motor3+" motor4: "+motor4+" battery: "+batarya+" roll: "+roll+" pitch: "+pitch+" yaw: "+yaw+" altitude: "+altitude+" lontitude: "+longtitude+" latitude: "+latitude+"\n")

           
            # Update labels with new data
            self.unlem_label.setText("unlem: " + unlem)  
            self.status_label.setText("status: " + status)  
            self.motor1_label.setText("motor1: " + motor1)  
            self.motor2_label.setText("motor2: " + motor2)  
            self.motor3_label.setText("motor3: " + motor3)  
            self.motor4_label.setText("motor4: " + motor4)  
            self.battery_label.setText("battery: " + batarya)  
            self.roll_label.setText("roll: " + roll)  
            self.pitch_label.setText("pitch: " + pitch)  
            self.yaw_label.setText("yaw: " + yaw)  
            self.altitude_label.setText("altitude: " + altitude)  
            self.longtitude_label.setText("longtitude: " + longtitude)  
            self.latitude_label.setText("latitude: " + latitude)  
            

            self.update_timer = threading.Timer(UpdateTimer, self.update_data)
            self.update_timer.start()

    def send_path(self):
        if self.serial_port and self.serial_port.is_open:
            # Define the path tuple
            # örnek path = ([1.0,2.0],[3.0,4.0],[5.0,6.0])
            path = get_coordinates()
            # Convert the path tuple to a json string
            path_json = json.dumps(path)
            # Send the path json string to the device
            self.serial_port.write(path_json.encode())
            # print("path_json binary hali: ",end="")
            # print(path_json.encode())
            if self.web_view:
                self.web_view.close()

    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DroneDataWindow()
    window.showNormal()
    sys.exit(app.exec_())
