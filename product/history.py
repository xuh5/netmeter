import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox,QLabel,QDesktopWidget
from PyQt5.QtGui import QIcon,QFont,QStandardItemModel,QStandardItem
from PyQt5.QtCore import pyqtSlot,QRect,QSize,pyqtSignal
from PyQt5.QtWidgets import QTableWidget,QVBoxLayout,QHeaderView,QTableWidgetItem,QHeaderView,QSizePolicy,QAbstractScrollArea
from database import Database
import sqlite3
class History_UI(QWidget):
    switch_to_the_main = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.title = 'History'
        self.setFixedSize(640, 320)
        self.data = Database()
        self.center()
        self.initUI()

  

    def initUI(self):
        self.setWindowTitle(self.title)
        label = QLabel('History', self)
        label.resize(100, 30)
        label.move(290,0)
        label.setFont(QFont('Arial', 20))
        button = QPushButton('Back to Menu', self)
        button.clicked.connect(self.switch_to_the_main.emit)

        #button.setToolTip('This is an example button')
        button.setGeometry(535,0,110,40)
        button1 = QPushButton('As TXT', self)
        button1.clicked.connect(self.output)
        button1.setGeometry(0,0,110,40)
        self.createTable()
        self.layout = QVBoxLayout()
        self.layout.insertSpacing(0,30)
        self.layout.addWidget(self.tableWidget) 
        self.setLayout(self.layout) 
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def output(self):
        rows = self.data.select_all_record()
        with open("output.txt", 'w') as f:
            f.write('{:<40}{:<40}{:<40}\n'.format("Time","Download", "Upload"))
            for i in range(len(rows)):
                f.write('{:<40}{:<40}{:<40}\n'.format(rows[i][3],rows[i][1], rows[i][2]))
    def createTable(self):
        self.tableWidget = QTableWidget()
        rows = self.data.select_all_record()
        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setColumnWidth(0,190)
        self.tableWidget.setColumnWidth(1,190)
        self.tableWidget.setColumnWidth(2,190)
        header = self.tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0,QHeaderView.Stretch)
        header.setSectionResizeMode(1,QHeaderView.Stretch)
        header.setSectionResizeMode(2,QHeaderView.Stretch)
        self.tableWidget.setHorizontalHeaderLabels(('Time', 'Download', 'Upload'))
        for x in range(len(rows)):
                self.tableWidget.setItem(x, 0, QTableWidgetItem(str(rows[x][3])))
                self.tableWidget.setItem(x, 1, QTableWidgetItem(str(rows[x][1])))
                self.tableWidget.setItem(x, 2, QTableWidgetItem(str(rows[x][2])))
    
    def updateTable(self):
        rows = self.data.select_all_record()
        self.tableWidget.setRowCount(len(rows))

        for x in range(len(rows)):
            self.tableWidget.setItem(x, 0, QTableWidgetItem(str(rows[x][3])))
            self.tableWidget.setItem(x, 1, QTableWidgetItem(str(rows[x][1])))
            self.tableWidget.setItem(x, 2, QTableWidgetItem(str(rows[x][2])))
