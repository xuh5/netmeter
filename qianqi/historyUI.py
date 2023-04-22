import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox,QLabel,QDesktopWidget
from PyQt5.QtGui import QIcon,QFont,QStandardItemModel,QStandardItem
from PyQt5.QtCore import pyqtSlot,QRect,QSize,pyqtSignal
from PyQt5.QtWidgets import QTableWidget,QVBoxLayout,QHeaderView,QTableWidgetItem,QHeaderView,QSizePolicy,QAbstractScrollArea
from database import Database
import sqlite3
from fpdf import FPDF
"""
HistoryUI class
Its purpose is to display the data in the database which the user recorded in the MainUI
"""
class HistoryUI(QWidget):
    """
    Create the initial page for the windown and set up the window size
    :param self:
    :return: None
    """
    switchToTheMain = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.title = 'History'
        self.setFixedSize(640, 320)
        self.data = Database()
        self.center()
        self.initUI()

  
    """
    Set up the button for the history window, and set up the table for the window
    :param self:
    :return: None
    """
    def initUI(self):
        #set tilte for the page
        self.setWindowTitle(self.title)
        label = QLabel('History', self)
        label.resize(100, 30)
        label.move(290,0)
        label.setFont(QFont('Arial', 20))
        #set button for back to menu
        button = QPushButton('Back to Menu', self)
        button.clicked.connect(self.switchToTheMain.emit)
        button.setGeometry(535,0,110,40)
        #set button for download as txt
        button1 = QPushButton('As TXT', self)
        button1.clicked.connect(self.output)
        button1.setGeometry(0,0,110,40)
        #set button for download as pdf
        button2 = QPushButton('As PDF', self)
        button2.clicked.connect(self.aspdf)
        button2.setGeometry(110,0,110, 40)
        #create table to display database
        self.createTable()
        self.layout = QVBoxLayout()
        self.layout.insertSpacing(0,30)
        self.layout.addWidget(self.tableWidget) 
        self.setLayout(self.layout) 
        self.show()
    """
    Center the window for the windown
    :param self:
    :return: None
    """
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    """
    The function which the download as txt button use to transfer the database file into a txt file
    :param self:
    :return: None
    """
    def output(self):
        rows = self.data.selectAllRecords()
        #loop to put the data into txt version
        with open("output.txt", 'w') as f:
            f.write('{:<40}{:<40}{:<40}\n'.format("Time","Download", "Upload"))
            for i in range(len(rows)):
                f.write('{:<40}{:<40}{:<40}\n'.format(rows[i][3],rows[i][1], rows[i][2]))
    """
    The function which the download as pdf button use to transfer the database file into a pdf file
    :param self:
    :return: None
    """
    def aspdf(self):
        rows = self.data.selectAllRecords()
        #first transfer the file into txt version
        with open("output.txt", 'w') as f:
            f.write('{:<40}{:<40}{:<40}\n'.format("Time","Download", "Upload"))
            for i in range(len(rows)):
                f.write('{:<40}{:<40}{:<40}\n'.format(rows[i][3],rows[i][1], rows[i][2]))
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size = 15)
        f = open("output.txt", "r")
        #tranfer the file into pdf version
        for x in f:
            pdf.cell(200, 10, txt = x, ln = 1, align = 'C')
        pdf.output("output.pdf")
    """
    The function to set up the table to display data in database
    :param self:
    :return: None
    """
    def createTable(self):
        self.tableWidget = QTableWidget()
        #set the initial table
        rows = self.data.selectAllRecords()
        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setColumnWidth(0,190)
        self.tableWidget.setColumnWidth(1,190)
        self.tableWidget.setColumnWidth(2,190)
        #set the column name for the table
        header = self.tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0,QHeaderView.Stretch)
        header.setSectionResizeMode(1,QHeaderView.Stretch)
        header.setSectionResizeMode(2,QHeaderView.Stretch)
        self.tableWidget.setHorizontalHeaderLabels(('Time', 'Download', 'Upload'))
        #for loop to input the dta into the database
        for x in range(len(rows)):
                self.tableWidget.setItem(x, 0, QTableWidgetItem(str(rows[x][3])))
                self.tableWidget.setItem(x, 1, QTableWidgetItem(str(rows[x][1])))
                self.tableWidget.setItem(x, 2, QTableWidgetItem(str(rows[x][2])))
    """
    The function to update the table so that the table will change when user add more record into the database
    :param self:
    :return: None
    """
    def updateTable(self):
        rows = self.data.selectAllRecords()
        self.tableWidget.setRowCount(len(rows))
        #for loop to update the data in the table
        for x in range(len(rows)):
            self.tableWidget.setItem(x, 0, QTableWidgetItem(str(rows[x][3])))
            self.tableWidget.setItem(x, 1, QTableWidgetItem(str(rows[x][1])))
            self.tableWidget.setItem(x, 2, QTableWidgetItem(str(rows[x][2])))
