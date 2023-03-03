# import datetime

# current_time = datetime.datetime.now().strftime("%H:%M:%S")
# print("Current time:", current_time)
# print(type(current_time))



#-------------------------------------------------------------------------------------------------------


# import cv2

# # Load the image
# img = cv2.imread("img (33).jpg")

# # Define the region of interest (ROI)
# x = 0  # x coordinate of the top-left corner of the ROI
# y = 120  # y coordinate of the top-left corner of the ROI
# width = 1920  # width of the ROI
# height = 1080  # height of the ROI

# # Crop the image
# roi = img[y:y+height, x:x+width]

# # Display the cropped image
# cv2.imshow("Cropped Image", roi)
# cv2.waitKey(0)
# cv2.destroyAllWindows()



#-------------------------------------------------------------------------------------------------------
# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton,QMainWindow,QSlider,QLineEdit
# import serial.tools.list_ports
# import serial
# import threading
# import json
# from PyQt5.QtCore import QUrl
# from PyQt5.QtWebEngineWidgets import QWebEngineView
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
        
#         self.setWindowTitle("My App")

#         widget = QSlider()

#         widget.setMinimum(-10)
#         widget.setMaximum(3)
#         # Or: widget.setRange(-10,3)

#         widget.setSingleStep(3)

#         widget.valueChanged.connect(self.value_changed)
#         widget.sliderMoved.connect(self.slider_position)
#         widget.sliderPressed.connect(self.slider_pressed)
#         widget.sliderReleased.connect(self.slider_released)

#         self.setCentralWidget(widget)

#     def value_changed(self, i):
#         print(i)

#     def slider_position(self, p):
#         print("position", p)

#     def slider_pressed(self):
#         print("Pressed!")

#     def slider_released(self):
#         print("Released")

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.showMaximized()
#     sys.exit(app.exec_())

#-------------------------------------------------------------------------------------------------------
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize    

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(320, 140))    
        self.setWindowTitle("PyQt Line Edit example (textfield) - pythonprogramminglanguage.com") 

        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Name:')
        self.line = QLineEdit(self)

        self.line.move(80, 20)
        self.line.resize(200, 32)
        self.nameLabel.move(20, 20)

        pybutton = QPushButton('OK', self)
        pybutton.clicked.connect(self.clickMethod)
        pybutton.resize(200,32)
        pybutton.move(80, 60)        

    def clickMethod(self):
        print('Your name: ' + self.line.text())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_() )