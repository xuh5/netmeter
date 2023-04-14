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

class main_menu(QWidget):
    switch_to_dialwidget = pyqtSignal()
    switch_to_test = pyqtSignal()
    switch_to_history = pyqtSignal()
    current_dir = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        super().__init__()
        #### initialize 
        self.previous =(0,0,0,0)
        self.count=0
        ##### UI setting
        self.setStyleSheet("background-color:rgb(135,206,235)")
        self.setFixedSize(400, 300)
        self.center()
        self.setWindowTitle('Netmeter')
        self.record = list()
        self.check = True
        self.initUI()
        self.database_= Database()


    def initUI(self):        
        #### logo
        pixmap = QPixmap(self.current_dir+"/logo.png")
        scaled_pixmap = pixmap.scaled(pixmap.width() // 4, pixmap.height() // 4)
        label = QLabel(self)
        label.setPixmap(scaled_pixmap)
        label.resize(scaled_pixmap.width(),scaled_pixmap.height())
        
        ########## button
        QToolTip.setFont(QFont('SansSerif', 10))
        btn1 = QPushButton('History', self)
        btn2 = QPushButton('speed test', self)
        self.btn3 = QPushButton('record', self)
        btn4 = QPushButton('pop out', self)
        btn1.setStyleSheet("background-color: rgba(222,184,135,180) ")
        btn2.setStyleSheet("background-color: rgba(222,184,135) ")
        self.btn3.setStyleSheet("background-color: rgba(222,184,135,180) ")
        btn4.setStyleSheet("background-color: rgba(222,184,135,180) ")
        tmp_height= (300-scaled_pixmap.height())//4
        btn1.setGeometry(0, scaled_pixmap.height(), scaled_pixmap.width(),tmp_height)
        btn2.setGeometry(0, scaled_pixmap.height()+tmp_height, scaled_pixmap.width(),tmp_height)
        self.btn3.setGeometry(0, scaled_pixmap.height()+tmp_height*2, scaled_pixmap.width(),tmp_height)
        btn4.setGeometry(0, scaled_pixmap.height()+tmp_height*3, scaled_pixmap.width(),tmp_height)
        
        #### button functionality
        ### switch UI
        btn2.clicked.connect(self.switch_to_test.emit)
        btn1.clicked.connect(self.switch_to_history.emit)
        btn4.clicked.connect(self.switch_to_dialwidget.emit)

        ####display speed area
        displayspeed = QWidget(self)
        displayspeed.setGeometry(QRect(scaled_pixmap.width(),scaled_pixmap.height(),300,tmp_height*4))
        displayspeed.setStyleSheet("QWidget{background-color:rgb(255,255,235);border:none}")
        
        ######upload,download icon
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
        
        ########show upload/download number
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
        
        #####dashboard
        bin_=(0,0.3,0.6,0.9,1.2,1.5,1.8,10,18)
        self.dashboard = Dashboard(bin_,self)
        self.dashboard.setGeometry(self.width()/5*1.7,self.height()/2.3,150,150)

        #### record function
        self.btn3.clicked.connect(self.startrecord)
        self.timer_record = QTimer(self)
        self.timer_record.timeout.connect(self.recording)

        ###### circular dashboard

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

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
    
    def startrecord(self):
        if self.check:
            self.btn3.setText("stop")
            self.timer_record.start(1000)
            self.check= not self.check
        else:
            self.btn3.setText("record")
            self.timer_record.stop()
            self.check= not self.check
            for i in self.record:
                print(i[1],i[0])
                with self.database_.conn:
                    self.database_.addRecord(i[1],i[0],i[2])
            self.record.clear()

    def recording(self):
        self.record.append([self.previous[0]/1000000,self.previous[1]/1000000,datetime.now()])

    def updatespeed(self):
        convert1,convert2,unit1,unit2 = self.getspeed()
        self.up1.setText(str( round(self.previous[0]/convert1,1))+unit1)
        self.down1.setText(str(round(self.previous[1]/convert2,1))+unit2)
        
        ###update dashboard pointer
        valueinmb = (self.previous[0]+self.previous[1])/1000000
        self.dashboard.setValue(valueinmb)
        self.dashboard.update()
        
