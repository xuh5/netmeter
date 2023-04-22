from dialWidget import DialWidget
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton,QApplication,QToolTip
from PyQt5.QtCore import Qt, QPoint, pyqtSignal

"""
DialWidgetUI class
a class that displays the dial with an UI
"""
class DialWidgetUI(QWidget):

    switchToMainUI = pyqtSignal()

    """
    Initializes the DialWidgetUI
    :param self:
    :return: none
    """
    def __init__(self):
        super().__init__()
        self.title = 'dialWidget'
        self.initUI()


    """
    Sets up the UI of DialWidgetUI
    :param self:
    :return: none
    """
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setFixedSize(250, 300)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        topLeftPoint = QApplication.desktop().availableGeometry().topLeft()
        self.move(topLeftPoint)

        layout = QVBoxLayout()

        backbtn = QPushButton("back", self)
        backbtn.setStyleSheet("background-color: rgba(222,184,135,255) ")
        backbtn.clicked.connect(self.switchToMainUI.emit)

        dialWidget = DialWidget()

        layout.addWidget(dialWidget)
        layout.addWidget(backbtn)

        self.setLayout(layout)

    """
    changes position of window when mouse is pressed
    :param self:
    :return: none
    """
    def mousePressEvent(self, event):
        self.oldPosition = event.globalPos()
        return
    
    """
    changes position of window when mouse is moving
    :param self:
    :return: none
    """
    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPosition)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPosition = event.globalPos()
        return