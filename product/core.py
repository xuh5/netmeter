import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal
from speed_test_UI import speed_test_UI
from main_UI import main_menu
from history import History_UI
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.page1 = main_menu()
        self.page2 = speed_test_UI()
        self.page3 = History_UI()

        self.page1.switch_to_test.connect(self.show_page2)
        self.page2.switch_to_track.connect(self.show_page1)
        self.page3.switch_to_the_main.connect(self.p3_to_p1)
        self.page1.switch_to_history.connect(self.p1_to_p3)
                                          
        self.page1.show()
        self.page2.hide()
        self.page3.hide()

    def show_page1(self):
        self.page1.show()
        self.page2.hide()
        page2_geometry = self.page2.frameGeometry()
        self.page1.move(page2_geometry.topLeft())

    def show_page2(self):
        self.page1.hide()
        self.page2.show()
        page1_geometry = self.page1.frameGeometry()
        self.page2.move(page1_geometry.topLeft())
    def p3_to_p1(self):
        self.page3.hide()
        self.page1.show()
        page3_geometry = self.page3.frameGeometry()
        self.page1.move(page3_geometry.topLeft())
    def p1_to_p3(self):
        self.page3.updateTable()
        self.page1.hide()
        self.page3.show()
        page1_geometry = self.page1.frameGeometry()
        self.page3.move(page1_geometry.topLeft())
        
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()

    sys.exit(app.exec_())