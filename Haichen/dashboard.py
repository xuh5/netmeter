import math
import sys

from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QColor, QFont, QPainter, QRadialGradient, QPolygon, QPen
from PyQt5.QtWidgets import QApplication, QWidget, QLCDNumber, QFrame


class Dashboard(QWidget):
    """
        Initialze the dashboard
        :param self: 
        :param bin_ : a list of number for scale
        :parent
        :return: 
        """
    def __init__(self,bin_, parent=None):
        super(Dashboard, self).__init__(parent)

        self.setWindowTitle("QPainter test")
        # self.setMaximumSize(700, 700)

        # color setting
        self.bin_= bin_
        self.pieColorStart = QColor(63, 191, 127)  # green
        self.pieColorMid = QColor(255, 155, 0)  # yellow
        self.pieColorEnd = QColor(222, 0, 0)  # red
        self.pointerColor = QColor(72, 203, 203)  # cyan-blue
        self.startAngle = 60
        self.endAngle = 60
        self.minValue = 0
        self.maxValue = 16
        self.currentValue = 0
        self.scaleMajor = 8
        # set font
        self.font = QFont("宋体", 8)
        self.font.setBold(True)

        # other setting
        """
        Set the title of the UI
        :param self: 
        :param title str
        :return: 
        """
    def setTitle(self, title):
        self._title = title
        
        """
        Set the current value
        :param self: 
        :param value float
        :return: 
        """
    def setValue(self, value):
        self.currentValue = value
        """
        The paintevent manage all the painting
        :param self
        :param event: event trigger
        :return: 
        """
    def paintEvent(self, event):
        # change the x, y axies
        width = self.width()
        height = self.height()

        painter = QPainter(self)  # initialize painter
        painter.translate(width / 2, height / 2)  # use translate() to make the dashboard to the center of the UI

        # pick the min for the side
        side = min(width, height)
        painter.scale(side / 200.0, side / 200.0)
        # make a line length = side/200

        # use anti-aliasing to make it smoother
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        painter.begin(self)

        # start painting.
        self.drawColorPie(painter)
        self.drawPointerIndicator(painter)
        self.drawLine(painter)
        self.drawText(painter)
        # self.drawTitle(painter)

        """
        draw the three color sector
        :param self
        :param painter:manager
        :return: 
        """
    def drawColorPie(self, painter): 
        painter.save()  # save() the current position
        # set the area of the sector
        radius = 99  # 半径
        painter.setPen(Qt.NoPen)
        rect = QRectF(-radius, -radius, radius * 2, radius * 2)  # the position of the sector

        # calculate the angle of the sector。green：blue：red = 1：2：1
        angleAll = 360.0 - self.startAngle - self.endAngle  # self.startAngle = 45, self.endAngle = 45
        angleStart = angleAll * 0.25
        angleMid = angleAll * 0.5
        angleEnd = angleAll * 0.25

        # fill the cetner of the circle with transparent color to make a sector 
        rg = QRadialGradient(0, 0, radius, 0, 0)  
        ratio = 0.8  # transparent

        # drawing the green loop
        rg.setColorAt(0, Qt.transparent) 
        rg.setColorAt(ratio, Qt.transparent)
        rg.setColorAt(ratio + 0.01, self.pieColorStart)
        rg.setColorAt(1, self.pieColorStart)

        painter.setBrush(rg)
        painter.drawPie(rect, (270 - self.startAngle - angleStart) * 16, angleStart * 16)

        # drawing the blue loop
        rg.setColorAt(0, Qt.transparent)
        rg.setColorAt(ratio, Qt.transparent)
        rg.setColorAt(ratio + 0.01, self.pieColorMid)
        rg.setColorAt(1, self.pieColorMid)

        painter.setBrush(rg)
        painter.drawPie(rect, (270 - self.startAngle - angleStart - angleMid) * 16, angleMid * 16)

        # drawing the red loop
        rg.setColorAt(0, Qt.transparent)
        rg.setColorAt(ratio, Qt.transparent)
        rg.setColorAt(ratio + 0.01, self.pieColorEnd)
        rg.setColorAt(1, self.pieColorEnd)

        painter.setBrush(rg)
        painter.drawPie(rect, (270 - self.startAngle - angleStart - angleMid - angleEnd) * 16, angleEnd * 16)

        painter.restore()  # restore() the x,y axies
        
        """
        Drawing the pointer Indicator
        :param self
        :param painter:manager
        :return: 
        """
    def drawPointerIndicator(self, painter):
        painter.save()

        radius = 58  # length of the pointer
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.pointerColor)

        # make a polygon shape for the pointer
        pts = QPolygon()
        pts.setPoints(-5, 0, 0, -8, 5, 0, 0, radius)
        # print("radius:" + str(radius))

        # rotate the pointer to set it at 0
        painter.rotate(self.startAngle)
        degRotate = 0
        angleStep = (360.0 - self.startAngle - self.endAngle) / self.scaleMajor
        if(self.currentValue <self.bin_[6]):
            degRotate = (360.0 - self.startAngle - self.endAngle -2*angleStep) / self.bin_[6] \
                    * (self.currentValue - self.minValue)
        if(self.currentValue>self.bin_[6] and self.currentValue<self.bin_[8]):
            degRotate = (2*angleStep / self.bin_[8] * (self.currentValue - self.bin_[6]))+ 6* angleStep
        if(self.currentValue>=self.bin_[8]):
            degRotate = 8* angleStep
        painter.rotate(degRotate)
        painter.drawConvexPolygon(pts)
        painter.restore()
    """
        Drawing the Text to display the speed
        :param self
        :param painter:manager
        :return: 
        """
    def drawText(self, painter):
        painter.save()
        #drawing the scale

        startRad = 4
        deltaRad = 0.6
        radius = 63
        offset = 5.5
  
        for i in range(self.scaleMajor + 1):  # self.scaleMajor = 8
            # calculate the sin and cos
            sina = math.sin(startRad - i * deltaRad)
            cosa = math.cos(startRad - i * deltaRad)

            # calculate the number for each scale
            value = math.ceil((1.0 * i * (
                    (self.maxValue - self.minValue) / self.scaleMajor) + self.minValue))
            # math.ceil(x)：return the smallest integeter that is not smaller than x
            strValue = str(int(value))

            # text height and width
            textWidth = self.fontMetrics().width(strValue)
            textHeight = self.fontMetrics().height()

   
            x = radius * cosa - textWidth / 2
            y = -radius * sina + textHeight / 4

            painter.setFont(self.font)
            painter.setPen(QColor(26, 95, 95))  # set color
            painter.drawText(x - offset, y, str(self.bin_[i])+ 'm')
           
        painter.restore()
        """
        Drawing the line on the scale
        :param self
        :param painter:manager
        :return: 
        """
    def drawLine(self, painter):
        painter.save()
        # drawing scale
        # print("drawLine")
        radius = 79
        painter.rotate(self.startAngle)  # self.startAngle = 45,rotate 45 degree
        steps = self.scaleMajor  # 8 scale
        angleStep = (360.0 - self.startAngle - self.endAngle) / steps  # angle for each scale 
        for i in range(steps + 1):
            if i < 3:
                color = self.pieColorStart
            elif i < 7:
                color = self.pieColorMid
            else:
                color = self.pieColorEnd
            painter.setPen(QPen(color, Qt.SolidLine))
            painter.drawLine(0, radius - 5, 0, radius)
            painter.rotate(angleStep)
        painter.restore()
