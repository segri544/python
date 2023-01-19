from PyQt5.QtWidgets import QApplication,QMainWindow,QLabel,QPushButton
import sys

class Win(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initGUI()
        self.show()
    def initGUI(self):
        self.setGeometry(100,100,900,600)
        self.setWindowTitle("Butonclicked")
        self.labelmerhaba = QLabel("",self)
        self.pushButtonSelamla = QPushButton("Tıkla",self)
        self.pushButtonSelamla.setGeometry(10,20,100,50)
        self.pushButtonSelamla.clicked.connect(lambda:self.pushButtonSelamla_Clicked("mehabalardasds")) #        self.pushButtonSelamla.clicked.connect(self.pushButtonSelamla_Clicked()) 
    def pushButtonSelamla_Clicked(self,message):
        self.labelmerhaba.setText(message)


if __name__=="__main__":

    app=QApplication(sys.argv)

    win=Win()
    sys.exit(app.exec())
    