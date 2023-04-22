import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,QMessageBox
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from speedTestUI import SpeedTestUI
from mainUI import MainUI
from historyUI import HistoryUI
from dialWidgetUI import DialWidgetUI
import os
import ctypes
"""
a class the manager the connection between different UI
:param qwidget
:return:
"""
class Core(QWidget):
    """
    Initialize the 4 UI, connect the switching functions and close event
    :param self
    :return:
    """
    def __init__(self):
        super().__init__()
        #### set up files
        self.page1 = MainUI()
        self.page2 = SpeedTestUI()
        self.page3 = HistoryUI()
        self.page4 = DialWidgetUI()
        
        
        ####connecting switch function
        self.page1.switchToTest.connect(self.showPage2)
        self.page1.switchToHistory.connect(self.p1ToP3)
        self.page1.switchToDialwidget.connect(self.showDialWidget)
        self.page2.switchToTrack.connect(self.showPage1)
        self.page3.switchToTheMain.connect(self.p3ToP1)

        self.page4.switchToMainUI.connect(self.hideDialWidget)
        
        
        
        self.page1.show()
        self.page2.hide()
        self.page3.hide()
        self.page4.hide()
        
        ###connect custom close_event
        self.page1.closeEvent = self.handleCloseEvent
        self.page2.closeEvent = self.handleCloseEvent
        self.page3.closeEvent = self.handleCloseEvent
        self.page4.closeEvent = self.handleCloseEvent
    """
    helper function for custom close event : close all the UI
    :param self
    :return:
    """
    def closeAllPages(self):
        self.page1.deleteLater()
        self.page2.deleteLater()
        self.page3.deleteLater()
        self.page4.deleteLater()
    """
    custom close event, gives three options : confirm, no, hide
    :param self
    :param event: signal trigger
    :return:
    """
    def handleCloseEvent(self, event):
        messageBox = QMessageBox()
        messageBox.setWindowTitle("Exit Confirmation")
        messageBox.setText("Are you sure you want to exit the application?")
        messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        hideButton = messageBox.addButton("Hide", QMessageBox.ActionRole)
        messageBox.setDefaultButton(QMessageBox.No)
        reply = messageBox.exec_()

        if reply == QMessageBox.Yes:
            self.closeAllPages()
            event.accept()
        elif reply == QMessageBox.No:
            event.ignore()
        elif messageBox.clickedButton() == hideButton:
            event.ignore() 
    """
    switch function: page2 to page1
    :param self
    :return:
    """
    def showPage1(self):
        self.page1.show()
        self.page2.hide()
        page2Geometry = self.page2.frameGeometry() # get the position of page2.
        self.page1.move(page2Geometry.topLeft()) # keep the position the same with the other UI.
    """
    switch function: page1 to page2
    :param self
    :return:
    """
    def showPage2(self):
        self.page1.hide()
        self.page2.show()
        page1Geometry = self.page1.frameGeometry()
        self.page2.move(page1Geometry.topLeft())
    """
    switch function: page3 to page1
    :param self
    :return:
    """
    def p3ToP1(self):
        self.page3.hide()
        self.page1.show()
        page3Geometry = self.page3.frameGeometry()
        self.page1.move(page3Geometry.topLeft())
    """
    switch function: page1 to page3
    :param self
    :return:
    """
    def p1ToP3(self):
        #update the table
        self.page3.updateTable()
        self.page1.hide()
        self.page3.show()
        page1Geometry = self.page1.frameGeometry()
        self.page3.move(page1Geometry.topLeft())
    """
    switch function: page1 to page4
    :param self
    :return:
    """
    def showDialWidget(self):
        self.page1.hide()
        self.page4.show()
    """
    switch function: page4 to page1
    :param self
    :return:
    """
    def hideDialWidget(self):
        self.page1.show()
        self.page4.hide()
"""
Main . create the UI. and add logos to the task bard
:param self
:return:
"""        
if __name__ == "__main__":
    myappid = 'netmeter'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid) ## initialize the ctype.the logo on the task bar
                                                                        ## will be the same with the window icon
    currentDir = os.getcwd()# get current address
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(currentDir+"/logo.png"))# set the logo 
    window = Core()
    
    sys.exit(app.exec_())