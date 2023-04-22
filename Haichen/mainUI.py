import sys
from trackSpeed import trackSpeed
from PyQt5.QtWidgets import (QWidget, QToolTip,QStackedWidget,QMainWindow,
    QPushButton, QApplication,QVBoxLayout, QHBoxLayout,QDesktopWidget,QLabel,QMessageBox)
from PyQt5.QtGui import (QFont,QPixmap,QImage)
from PyQt5.QtCore import (QRect,QTimer,pyqtSignal)
from database import Database
from dashboard import Dashboard
from datetime import datetime
import os
"""
MainUI class
Its purpose is to create the first / main Ui of the application.
It tracks the current download/upload speed.
"""
class MainUI(QWidget):
    # send signals when button is clicked
    switchToDialwidget = pyqtSignal()
    switchToTest = pyqtSignal()
    switchToHistory = pyqtSignal()
    # address of the current directory
    currentDir = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        super().__init__()
        # initialize 
        self.previous =(0,0,0,0)
        self.count=0
        # UI setting
        self.setStyleSheet("background-color:rgb(217,217,217)") #was 135,206, 235
        self.setFixedSize(400, 300)
        self.center()
        self.setWindowTitle('Netmeter')
        self.record = list()
        self.check = True
        self.initUI()
        self.database= Database()


    def initUI(self):        
        #### set the logo
        pixmap = QPixmap(self.currentDir+"/logo.png")
        scaledPixmap = pixmap.scaled(pixmap.width() // 4, pixmap.height() // 4)
        label = QLabel(self)
        label.setPixmap(scaledPixmap)
        label.resize(scaledPixmap.width(),scaledPixmap.height())
        
        #creating buttons button
        
        #Set the title of buttons
        QToolTip.setFont(QFont('SansSerif', 10))
        btn1 = QPushButton('History', self)
        btn2 = QPushButton('speed test', self)
        self.btn3 = QPushButton('record', self)
        btn4 = QPushButton('pop out', self)

        #Set the font of buttons
        btn1.setFont(QFont('Times',10))
        btn2.setFont(QFont('Times',10))
        btn4.setFont(QFont('Times',10))
        
        #Set the style of button
        btn1.setStyleSheet("""
            QPushButton{
                border: none;
                background-color: rgb(135,206, 235);
            }
            QPushButton::hover{
                background-color: rgb(255, 0, 191);
            }
        """)
        
        #Button 3 is different because it has different position
        self.btn3.setStyleSheet("""
            border-radius: 50px;
            border: 2px solid black;
            background-color: rgb(255,255,235);
        """)
        
        #Button 2 style
        btn2.setStyleSheet("""
            QPushButton{
                border: none;
                background-color: rgb(135,206, 235);
            }
            QPushButton::hover{
                background-color: rgb(255, 0, 191);
            }
        """)
        
        #Button 4 style
        btn4.setStyleSheet("""
            QPushButton{
                border: none;
                background-color: rgb(135,206, 235);
            }
            QPushButton::hover{
                background-color: rgb(255, 0, 191);
            }
        """)
        
        #Some parameters to make sure all buttons except button 2 has the same size
        tempWidth = (400-scaledPixmap.width())//3
        
        tmpHeight= (300-scaledPixmap.height())//4
        
        #Set the geometry of button 1, 2, 4
        btn1.setGeometry(scaledPixmap.width(),0,tempWidth,scaledPixmap.height())
                
        btn2.setGeometry(scaledPixmap.width() + tempWidth,0,tempWidth,scaledPixmap.height())
        
        btn4.setGeometry(scaledPixmap.width() + tempWidth * 2,0,tempWidth,scaledPixmap.height())
        
        #Special parameters only for button 3
        buttonWidth = 100
        
        buttonHeight = 100
        
        #Special geometry to make sure the position of button 2 is at the center horizontally and vertically
        self.btn3.setGeometry(scaledPixmap.width()//2 - buttonWidth//2, (self.height()-scaledPixmap.height())//2 - buttonHeight//2 + scaledPixmap.height(), buttonWidth, buttonHeight)
        
        
        
        #butoon functionality,switch UI and send signals
        btn2.clicked.connect(self.switchToTest.emit)
        btn1.clicked.connect(self.switchToHistory.emit)
        btn4.clicked.connect(self.switchToDialwidget.emit)

        ####set up the display speed area
        displaySpeed = QWidget(self)
        displaySpeed.setGeometry(QRect(scaledPixmap.width(),scaledPixmap.height(),300,tmpHeight*4))
        displaySpeed.setStyleSheet("QWidget{background-color:rgb(217,217,217);border:none}")
        
        #set up upload,download icon
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
        
        #show upload/download number
        self.up1= QLabel(self)
        self.down1 = QLabel(self)
        self.up1.setText("0B      ")
        self.down1.setText("0B      ")
        self.up1.move(325, 150)
        self.down1.move(325, 230)
        self.up1.setStyleSheet("background-color: rgba(255, 255, 255, 0)")
        self.down1.setStyleSheet("background-color: rgba(255, 255, 255, 0)")
        timer = QTimer(self)
        timer.timeout.connect(self.updateSpeed)
        timer.start(1000) 
        
        #set up dashboard
        binList=(0,0.3,0.6,0.9,1.2,1.5,1.8,10,18)
        self.dashboard = Dashboard(binList,self)
        self.dashboard.setGeometry(int(self.width()/5*1.7),int(self.height()/2.3),150,150)

        # record function
        self.btn3.clicked.connect(self.startRecord)
        self.timerRecord = QTimer(self)
        self.timerRecord.timeout.connect(self.recording)
        
        #display
        self.show()
    """
    make the UI at the center of the laptop
    :param self: 
    :return:
    """
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    """
    gets the current download/upload speed and transform it into different unit
    :param self: 
    :return: download/upload speed with their unit
    """
    def getSpeed(self):
        x=trackSpeed(self.previous[2],self.previous[3],1)
        self.previous =x
        unit1 = "B"
        unit2 = "B"
        convert1=1
        convert2=1
        if(self.count!=0):
            if(self.previous[0]>=1000):
                if(self.previous[0]>=1000000):
                    unit1="MB"
                    convert1=1000000
                else:
                    unit1="KB"
                    convert1=1000
            if(self.previous[1]>=1000):
                if(self.previous[1]>=1000000):
                    unit2="MB"
                    convert2=1000000
                else:
                    unit2="KB"
                    convert2=1000
        self.count+=1
        return convert1,convert2,unit1,unit2
    """
    functionality for record button: start to record the speed and add into database
    :param self: 
    :return:
    """
    def startRecord(self):
        # if the button is off
        if self.check:
            self.btn3.setText("stop")
            self.timerRecord.start(1000) # set timer for recording every 1 second
            self.check= not self.check
        # if it's already recording 
        else:
            self.btn3.setText("record")
            self.timerRecord.stop()
            self.check= not self.check
            for i in self.record:
                print(i[1],i[0])
                with self.database.conn:
                    self.database.addRecord(i[1],i[0],i[2]) # add data to database
            self.record.clear()
    """
    add the record into a private list every 1 second
    :param self: 
    :return:
    """
    def recording(self):
        self.record.append([self.previous[0]/1000000,self.previous[1]/1000000,datetime.now()])
        
    """
    update the speed in text and dashboard every 1 second
    :param self: 
    :return:
    """
    def updateSpeed(self):
        #update the text
        convert1,convert2,unit1,unit2 = self.getSpeed()
        self.up1.setText(str( round(self.previous[0]/convert1,1))+unit1)
        self.down1.setText(str(round(self.previous[1]/convert2,1))+unit2)
        
        ###update dashboard pointer
        valueinmb = (self.previous[0]+self.previous[1])/1000000
        self.dashboard.setValue(valueinmb)
        self.dashboard.update()

