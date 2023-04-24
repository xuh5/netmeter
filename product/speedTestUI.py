import sys
from PyQt5.QtWidgets import (QWidget, QToolTip,QStackedWidget,QMainWindow,
    QPushButton, QApplication,QVBoxLayout, QHBoxLayout,QDesktopWidget,QLabel,QMessageBox)
from PyQt5.QtGui import (QFont,QPixmap,QImage)
from PyQt5.QtCore import (QRect,QTimer,QCoreApplication,pyqtSignal)
from dashboard import Dashboard
from speedTest import speedTest
import os
"""
SpeedTestUI class
Its purpose is to let the user test their maximum speed
"""
class SpeedTestUI(QWidget):
    # set signals and get the current directory
    switchToTrack = pyqtSignal()
    currentDir = os.path.dirname(os.path.abspath(__file__))
    """
    initialize the UI
    :param self:
    :return: 
    """
    def __init__(self):
        super().__init__()
        #### initialize 
        self.previous =(0,0,0,0)
        self.count=0
        ##### UI setting
        self.setStyleSheet("background-color:rgb(135,206,235)")
        self.setFixedSize(420, 300)
        self.center()
        self.setWindowTitle('Netmeter')
        self.label1 = QLabel("Please wait after you click the 'start' button", self) #initilize the text label
        self.label1.setFont(QFont('Arial', 8))
        self.label1.move(int(self.width()//5), int(self.height()//10)+50)
        self.initUI()
    """
    Make the Ui at the center of the window
    :param self:
    :return: 
    """
    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    """
    display the speed in text, dashboard after the speed test is completed
    :param self:
    :return: 
    """
    def showSpeed(self):
        x = None
        while x is None:
            x = speedTest()
            # Process any pending events in the event loop
            QCoreApplication.processEvents()
        
        self.up1.setText(str( round(x[0],1))+x[1])
        self.down1.setText(str(round(x[2],1))+x[3])
        self.ping.setText("ping:"+str(round(x[4]))+'ms')
        valueinmb= round(x[0]+x[2]) 
        self.label1.setText("Speed test finished") #change the text label
        self.dashboard.setValue(valueinmb)
        self.dashboard.update()
    """
    setting up the layout of the UI
    :param self:
    :return: 
    """
    def initUI(self):  
        # add logo
        pixmap = QPixmap(self.currentDir+"/logo.png")
        scaledPixmap = pixmap.scaled(pixmap.width() // 4, pixmap.height() // 4)
     
        label = QLabel(self)
        label.setPixmap(scaledPixmap)
        label.resize(scaledPixmap.width(),scaledPixmap.height())
        label.move(self.width()-scaledPixmap.width(),0)
        
        #add the heading widget
        heading = QWidget(self)
        heading.setGeometry(QRect(0,0,self.width(),scaledPixmap.height()))
        heading.setStyleSheet("QWidget{background-color:rgb(255,255,235);border:none}")
        heading.lower()
        
        #set up buttons
        btn1 = QPushButton('Back to Main', self)
        btn1.setStyleSheet("""
            background-color: rgba(222,184,135,180);
            border: none;
        """)
        btn1.setGeometry(0, 0, scaledPixmap.width(),scaledPixmap.height())
        
        # set up the title
        title= QLabel('Times font',self)
        title.setText("SpeedTest")
        title.move(int(self.width()//2.4), int(self.height()//10))
        title.setStyleSheet("background-color: rgba(255, 255, 255, 0)")
        
        # make a bin for the scale of the dashboard
        binList=(0,20,40,60,80,100,120,320,620)
        self.dashboard = Dashboard(binList,self)

        self.dashboard.setGeometry(int(self.width()/5*1.7),int(self.height()/2.3),150,150)
        ###### switch ui
        btn1.clicked.connect(self.switchToTrack.emit)
        
         ######upload,download icon
        up = QPixmap(self.currentDir+"/arrow1.png")
        up = up.scaled(20,20)
        label1 = QLabel(self)
        label1.setPixmap(up)
        label1.setStyleSheet("background-color: rgba(255, 255, 255, 0)")
        label1.move(300, 150)
        down = QPixmap(self.currentDir+"/arrow2.png")
        down = down.scaled(20,20)
        label2 = QLabel(self)
        label2.setPixmap(down)
        label2.setStyleSheet("background-color: rgba(255, 255, 255, 0)")
        label2.move(300, 230)
        
        ########show upload/download number
        self.up1= QLabel(self)
        self.down1 = QLabel(self)
        self.up1.setText("0B          ")
        self.down1.setText("0B            ")
        self.up1.move(325, 150)
        self.down1.move(325, 230)
        self.up1.setStyleSheet("background-color: rgba(255, 255, 255, 0)")
        self.down1.setStyleSheet("background-color: rgba(255, 255, 255, 0)")
        
        # show the ping
        self.ping = QLabel(self)
        self.ping.setText("ping:0ms     ")
        self.ping.move(305,180)
        self.ping.setStyleSheet("background-color: rgba(255, 255, 255, 0)")
       
        #button to start the speed test
        button = QPushButton("start",self)
        button.setGeometry(self.width()//20, self.height()//2, 70, 70)
        button.setStyleSheet("""
            QPushButton {
                border-radius: 35px;
                border: 2px solid black;
                background-color: rgb(255,255,235);
            }
            QPushButton:pressed {
                background-color: green;
            }
        """)
        button.clicked.connect(self.showSpeed)
        
        #display
        self.show()
        
