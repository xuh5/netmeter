import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,QMessageBox
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from Speed_test_UI import Speed_test_UI
from main_UI import main_UI
from History_UI import History_UI
from dialwidget_ui import DialWidgetUI
import os
import ctypes
"""
a class the manager the connection between different UI
:param qwidget
:return:
"""
class Manager(QWidget):
    """
    Initialize the 4 UI, connect the switching functions and close event
    :param self
    :return:
    """
    def __init__(self):
        super().__init__()
        #### set up files
        self.page1 = main_UI()
        self.page2 = Speed_test_UI()
        self.page3 = History_UI()
        self.page4 = DialWidgetUI()
        
        
        ####connecting switch function
        self.page1.switch_to_test.connect(self.show_page2)
        self.page2.switch_to_track.connect(self.show_page1)
        self.page3.switch_to_the_main.connect(self.p3_to_p1)
        self.page1.switch_to_history.connect(self.p1_to_p3)
        self.page1.switch_to_dialwidget.connect(self.showDialWidget)
        self.page4.switch_to_main_UI.connect(self.hideDialWidget)
        
        
        
        self.page1.show()
        self.page2.hide()
        self.page3.hide()
        self.page4.hide()
        
        ###connect custom close_event
        self.page1.closeEvent = self.handle_close_event
        self.page2.closeEvent = self.handle_close_event
        self.page3.closeEvent = self.handle_close_event
        self.page4.closeEvent = self.handle_close_event
    """
    helper function for custom close event : close all the UI
    :param self
    :return:
    """
    def close_all_pages(self):
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
    def handle_close_event(self, event):
        message_box = QMessageBox()
        message_box.setWindowTitle("Exit Confirmation")
        message_box.setText("Are you sure you want to exit the application?")
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        hide_button = message_box.addButton("Hide", QMessageBox.ActionRole)
        message_box.setDefaultButton(QMessageBox.No)
        reply = message_box.exec_()

        if reply == QMessageBox.Yes:
            self.close_all_pages()
            event.accept()
        elif reply == QMessageBox.No:
            event.ignore()
        elif message_box.clickedButton() == hide_button:
            event.ignore() 
    """
    switch function: page2 to page1
    :param self
    :return:
    """
    def show_page1(self):
        self.page1.show()
        self.page2.hide()
        page2_geometry = self.page2.frameGeometry() # get the position of page2.
        self.page1.move(page2_geometry.topLeft()) # keep the position the same with the other UI.
    """
    switch function: page1 to page2
    :param self
    :return:
    """
    def show_page2(self):
        self.page1.hide()
        self.page2.show()
        page1_geometry = self.page1.frameGeometry()
        self.page2.move(page1_geometry.topLeft())
    """
    switch function: page3 to page1
    :param self
    :return:
    """
    def p3_to_p1(self):
        self.page3.hide()
        self.page1.show()
        page3_geometry = self.page3.frameGeometry()
        self.page1.move(page3_geometry.topLeft())
    """
    switch function: page1 to page3
    :param self
    :return:
    """
    def p1_to_p3(self):
        #update the table
        self.page3.updateTable()
        self.page1.hide()
        self.page3.show()
        page1_geometry = self.page1.frameGeometry()
        self.page3.move(page1_geometry.topLeft())
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
    current_dir = os.getcwd()# get current address
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(current_dir+"/logo.png"))# set the logo 
    window = Manager()
    
    sys.exit(app.exec_())