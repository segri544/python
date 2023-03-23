import sys
import serial
import struct
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton,QLineEdit
import serial.tools.list_ports
import serial
import threading
import json
from PyQt5.QtCore import QUrl,QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView
import datetime
import time
import folium

current_time = datetime.datetime.now().strftime("%H_%M_%S")
logFile=current_time+".txt"


# # create new empty txt file to save data
# with open(logFile, 'w', encoding='utf-8') as f:
#   pass

UpdateTimer=0.05

# create new empty txt file to save data

class DroneDataWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drone Data")

        # Create layout
        self.layoutV= QVBoxLayout()
        self.setLayout(self.layoutV)
        self.layout = QHBoxLayout()
        self.layoutV.addLayout(self.layout)
        self.dataLayout=QVBoxLayout()
        self.layout.addLayout(self.dataLayout)
        self.buttonLay= QHBoxLayout()
        self.layoutV.addLayout(self.buttonLay)
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
        

        self.dataLayout.addWidget(self.unlem_label)
        self.dataLayout.addWidget(self.status_label)
        self.dataLayout.addWidget(self.motor1_label)
        self.dataLayout.addWidget(self.motor2_label)
        self.dataLayout.addWidget(self.motor3_label)
        self.dataLayout.addWidget(self.motor4_label)
        self.dataLayout.addWidget(self.battery_label)
        self.dataLayout.addWidget(self.roll_label)
        self.dataLayout.addWidget(self.pitch_label)
        self.dataLayout.addWidget(self.yaw_label)
        self.dataLayout.addWidget(self.altitude_label)
        self.dataLayout.addWidget(self.longtitude_label)
        self.dataLayout.addWidget(self.latitude_label)
#---------------------------------------------------------------------------------------------------------------------------------------
        # initialize folium map
        self.m = folium.Map(location=[39.94523994189189, 32.84516220237323], zoom_start=10)
        # add marker to map
        # folium.Marker(
        #     location=[39.94523994189189, 32.84516220237323],s
        #     popup='drone',
        #     icon=folium.Icon(color='red', icon='info-sign')
        # ).add_to(self.m)

        # create web view
        self.view = QWebEngineView()
        map_html = self.m._repr_html_()
        self.view.setHtml(map_html)
        
        # create layout
        self.layout.addWidget(self.view)
        # self.map_layout.addWidget(self.view)
        
        # time.sleep(5)
        

        


#---------------------------------------------------------------------------------------------------------------------------------------

        
        # Create layout for baudrate and com port selection
        # Create baudrate combo box
        self.baudrate_combo = QComboBox()
        self.baudrate_combo.addItems(["9600", "115200", "230400"])
        self.buttonLay.addWidget(self.baudrate_combo)

        # Create com port combo box
        self.com_port_combo = QComboBox()
        self.buttonLay.addWidget(self.com_port_combo)

        # Create connect button"
        self.connect_button = QPushButton("Connect")
        self.buttonLay.addWidget(self.connect_button)
        self.connect_button.clicked.connect(self.connect_to_port)
        
        # Create disconnect button
        self.disconnect_button = QPushButton("Disconnect")
        self.buttonLay.addWidget(self.disconnect_button)
        self.disconnect_button.clicked.connect(self.disconnect_from_port)
        
        

        
        

        # Create stop motors button
        self.stop_motors_button = QPushButton("Stop Motors")
        self.layoutV.addWidget(self.stop_motors_button)
        self.stop_motors_button.clicked.connect(self.stop_motors)

        # populate available com ports
        self.populate_com_ports()
        self.serial_port = None

        self.update_timer = threading.Timer(1, self.update_data)
        self.update_timer.start()
    def update_location_map(self,longtitude,latitude):
        pass

        
        # # # add marker to map
        # folium.Marker(
        #     location=[longtitude, latitude],
        #     popup='Boston',
        #     icon=folium.Icon(color='red', icon='info-sign')
        # ).add_to(self.m)

        # # # create web view
        # self.view = QWebEngineView()
        # map_html = self.m._repr_html_()
        # self.view.setHtml(map_html)
        
        
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
    def closeEvent(self,event):
        try:
            self.disconnect_from_port()
        except:
            pass
        print('Window is closing!')
        
    def update_data(self):
        if self.serial_port and self.serial_port.is_open:
            raw = self.serial_port.read(32)
            if len(raw) == 32:
                data = struct.unpack('<HHHHHHHhhhHIIh', raw)
                #print(data)
                unlem= str(data[0])
                # if unlem!="33":
                #     self.disconnect_from_port()
                #     time.sleep(1)
                #     self.connect_to_port()
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
                longtitude = str(data[11]/(1.0**6))   # gönderirken çarptıgına böl
                latitude=str(data[12]/(1.0**6))   # gönderirken çarptıgına böl
                bos=str(data[13])               # son 2byte bosluk var
            # open the text file for writing
            # with open(logFile, 'a',encoding='utf-8') as f:
            #     # write the data to the file
            #     f.write("unlem: "+unlem+" status: "+status+" motor1: "+motor1+" motor2: "+motor2+" motor3: "+motor3+" motor4: "+motor4+" battery: "+batarya+" roll: "+roll+" pitch: "+pitch+" yaw: "+yaw+" altitude: "+altitude+" lontitude: "+str(longtitude)+" latitude: "+str(latitude)+"\n")
            # # Update labels with new data
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
            self.longtitude_label.setText("longtitude: " + str(longtitude))  
            self.latitude_label.setText("latitude: " + str(latitude))  
            self.update_timer = threading.Timer(UpdateTimer, self.update_data)
            self.update_timer.start()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DroneDataWindow()
    window.showNormal()
    sys.exit(app.exec_())
