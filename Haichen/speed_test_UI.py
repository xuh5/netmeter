import sys
import track_speed
from PyQt5.QtWidgets import (QWidget, QToolTip,QStackedWidget,QMainWindow,
    QPushButton, QApplication,QVBoxLayout, QHBoxLayout,QDesktopWidget,QLabel,QMessageBox)
from PyQt5.QtGui import (QFont,QPixmap,QImage)
from PyQt5.QtCore import (QRect,QTimer,QCoreApplication,pyqtSignal)
from dashboard import Dashboard
from speed_test import speed_test
import os

class speed_test_UI(QWidget):
    switch_to_track = pyqtSignal()
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
        self.initUI()
    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        ###### close/hide
    def closeEvent(self, event):
        message_box = QMessageBox()
        message_box.setWindowTitle("Exit Confirmation")
        message_box.setText("Are you sure you want to exit the application?")
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        hide_button = message_box.addButton("Hide", QMessageBox.ActionRole)
        message_box.setDefaultButton(QMessageBox.No)
        reply = message_box.exec_()

        if reply == QMessageBox.Yes:
            event.accept()
        elif reply == QMessageBox.No:
            event.ignore()
        elif message_box.clickedButton() == hide_button:
            event.ignore()
    def show_speed(self):
        x = None
        while x is None:
            x = speed_test()
            # Process any pending events in the event loop
            QCoreApplication.processEvents()
        
        self.up1.setText(str( round(x[0],1))+x[1])
        self.down1.setText(str(round(x[2],1))+x[3])
        self.ping.setText("ping:"+str(round(x[4]))+'ms')
        valueinmb= round(x[0]+x[2]) 
        self.dashboard.setValue(valueinmb)
        self.dashboard.update()

    def initUI(self):  
        pixmap = QPixmap(self.current_dir+"/logo.png")
        scaled_pixmap = pixmap.scaled(pixmap.width() // 4, pixmap.height() // 4)
  
        label = QLabel(self)
        label.setPixmap(scaled_pixmap)
        label.resize(scaled_pixmap.width(),scaled_pixmap.height())
        label.move(self.width()-scaled_pixmap.width(),0)

        heading = QWidget(self)
        heading.setGeometry(QRect(0,0,self.width(),scaled_pixmap.height()))
        heading.setStyleSheet("QWidget{background-color:rgb(255,255,235);border:none}")
        heading.lower()
        btn1 = QPushButton('Main', self)
        btn1.setStyleSheet("background-color: rgba(222,184,135,180) ")
        btn1.setGeometry(0, 0, scaled_pixmap.width(),scaled_pixmap.height())
        title= QLabel('Times font',self)
        title.setText("SpeedTest")
        title.move(int(self.width()//2.4), int(self.height()//10))
        title.setStyleSheet("background-color: rgba(255, 255, 255, 0)")
        
        bin_=(0,20,40,60,80,100,120,320,620)
        self.dashboard = Dashboard(bin_,self)

        self.dashboard.setGeometry(self.width()/5*1.7,self.height()/2.3,150,150)
        ###### switch ui
        btn1.clicked.connect(self.switch_to_track.emit)
        
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
        
        self.ping = QLabel(self)
        self.ping.setText("ping:0ms   ")
        self.ping.move(305,180)
        self.ping.setStyleSheet("background-color: rgba(255, 255, 255, 0)")
       
        
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
        button.clicked.connect(self.show_speed)
        #####
        self.show()
        