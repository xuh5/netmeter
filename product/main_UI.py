import sys
import track_speed
from PyQt5.QtWidgets import (QWidget, QToolTip,QStackedWidget,QMainWindow,
    QPushButton, QApplication,QVBoxLayout, QHBoxLayout,QDesktopWidget,QLabel,QMessageBox)
from PyQt5.QtGui import (QFont,QPixmap,QImage)
from PyQt5.QtCore import (QRect,QTimer,pyqtSignal)
from database import Database
from dashboard import Dashboard
from datetime import datetime
import os
"""
Main_UI class
Its purpose is to create the first / main Ui of the application.
It tracks the current download/upload speed.
"""
class main_UI(QWidget):
    # send signals when button is clicked
    switch_to_dialwidget = pyqtSignal()
    switch_to_test = pyqtSignal()
    switch_to_history = pyqtSignal()
    # address of the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

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
        self.database_= Database()


    def initUI(self):        
        #### set the logo
        pixmap = QPixmap(self.current_dir+"/logo.png")
        scaled_pixmap = pixmap.scaled(pixmap.width() // 4, pixmap.height() // 4)
        label = QLabel(self)
        label.setPixmap(scaled_pixmap)
        label.resize(scaled_pixmap.width(),scaled_pixmap.height())
        
        #creating buttons button
        
        #Set the title of buttons
        QToolTip.setFont(QFont('SansSerif', 10))
        btn1 = QPushButton('History', self)
        btn2 = QPushButton('speed test', self)
        self.btn3 = QPushButton('record', self)
        btn4 = QPushButton('pop out', self)

        #Set the font of buttons
        btn1.setFont(QFont('Times',10))
        self.btn3.setFont(QFont('Times',10))
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
        
        #Button 2 is different because it has different position
        btn2.setStyleSheet("""
            border-radius: 50px;
            border: 2px solid black;
            background-color: rgb(255,255,235);
        """)
        
        #Button 3 style
        self.btn3.setStyleSheet("""
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
        temp_width = (400-scaled_pixmap.width())//3
        
        tmp_height= (300-scaled_pixmap.height())//4
        
        #Set the geometry of button 1, 3, 4
        btn1.setGeometry(scaled_pixmap.width(),0,temp_width,scaled_pixmap.height())
                
        self.btn3.setGeometry(scaled_pixmap.width() + temp_width,0,temp_width,scaled_pixmap.height())
        
        btn4.setGeometry(scaled_pixmap.width() + temp_width * 2,0,temp_width,scaled_pixmap.height())
        
        #Special parameters only for button 2
        buttonWidth = 100
        
        buttonHeight = 100
        
        #Special geometry to make sure the position of button 2 is at the center horizontally and vertically
        btn2.setGeometry(scaled_pixmap.width()//2 - buttonWidth//2, (self.height()-scaled_pixmap.height())//2 - buttonHeight//2 + scaled_pixmap.height(), buttonWidth, buttonHeight)
        
        
        
        #butoon functionality,switch UI and send signals
        btn2.clicked.connect(self.switch_to_test.emit)
        btn1.clicked.connect(self.switch_to_history.emit)
        btn4.clicked.connect(self.switch_to_dialwidget.emit)

        ####set up the display speed area
        displayspeed = QWidget(self)
        displayspeed.setGeometry(QRect(scaled_pixmap.width(),scaled_pixmap.height(),300,tmp_height*4))
        displayspeed.setStyleSheet("QWidget{background-color:rgb(217,217,217);border:none}")
        
        #set up upload,download icon
        up = QPixmap(self.current_dir+"/arrow1.png")
        up = up.scaled(20,20)
        label1 = QLabel(self)
        label1.setPixmap(up)
        label1.setStyleSheet("background-color: rgba(255, 255, 255, 0)")
        label1.move(300, 150)
        down = QPixmap(self.current_dir+"/arrow2.png")
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
        timer.timeout.connect(self.updatespeed)
        timer.start(1000) 
        
        #set up dashboard
        bin_=(0,0.3,0.6,0.9,1.2,1.5,1.8,10,18)
        self.dashboard = Dashboard(bin_,self)
        self.dashboard.setGeometry(self.width()/5*1.7,self.height()/2.3,150,150)

        # record function
        self.btn3.clicked.connect(self.startrecord)
        self.timer_record = QTimer(self)
        self.timer_record.timeout.connect(self.recording)
        
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
    def getspeed(self):
        x=track_speed.track_speed(self.previous[2],self.previous[3],1)
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
    def startrecord(self):
        # if the button is off
        if self.check:
            self.btn3.setText("stop")
            self.timer_record.start(1000) # set timer for recording every 1 second
            self.check= not self.check
        # if it's already recording 
        else:
            self.btn3.setText("record")
            self.timer_record.stop()
            self.check= not self.check
            for i in self.record:
                print(i[1],i[0])
                with self.database_.conn:
                    self.database_.addRecord(i[1],i[0],i[2]) # add data to database
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
    def updatespeed(self):
        #update the text
        convert1,convert2,unit1,unit2 = self.getspeed()
        self.up1.setText(str( round(self.previous[0]/convert1,1))+unit1)
        self.down1.setText(str(round(self.previous[1]/convert2,1))+unit2)
        
        ###update dashboard pointer
        valueinmb = (self.previous[0]+self.previous[1])/1000000
        self.dashboard.setValue(valueinmb)
        self.dashboard.update()
