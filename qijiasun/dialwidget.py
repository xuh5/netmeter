import os
import math
from trackSpeed import trackSpeed

try:
    from PyQt5.QtWidgets import QWidget

    from PyQt5.QtGui import QPolygon, QPolygonF, QColor, QPen, QFont, QPainter, QFontMetrics, QConicalGradient, QRadialGradient, QFontDatabase

    from PyQt5.QtCore import Qt, QPoint, QPointF, QObject, QTimer

except:
    print("Error while importing PyQt5")
    exit()

"""
DialWidget class
a class that draws the dial widget
"""
class DialWidget(QWidget):
    
    """
    Initialize defualt values to create dial.
    :param self:
    :return: none
    """
    def __init__(self):
        super().__init__()

        # needle color: red
        self.NeedleColor = Qt.red

        # scale text color: neon green
        self.ScaleValueColor = QColor(57, 255, 20, 255)

        # value color: neon green
        self.DisplayValueColor = QColor(57, 255, 20, 255)

        # center pointer color: black
        self.CenterPointColor = Qt.black

        self.valueNeedle = QObject

        # default min and max
        self.minValue = 0
        self.maxValue = 1000

        # start value
        self.value = self.minValue

        # default offset
        self.valueOffset = 0

        # default radius
        self.gaugeColorOuterRadiusFactor = 1
        self.gaugeColorInnerRadiusFactor = 0.9

        self.centerHorizontalValue = 0
        self.centerVerticalValue = 0

        #3 default scale value
        self.scaleAngleStartValue = 135
        self.scaleAngleSize = 270

        self.angleOffset = 0

        self.scalaCount = 10
        self.scalaSubdivCount = 5

        self.pen = QPen(QColor(0, 0, 0))

        # load font
        QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(__file__), 'fonts/Orbitron/Orbitron-VariableFont_wght.ttf'))

        # default polygon color
        self.scalePolygonColors = []

        # big scale color: black
        self.bigScaleMarker = Qt.black

        # fine scale color: black
        self.fineScaleColor = Qt.black

        # scale text status
        self.scaleFontname = "Orbitron"
        self.initialScaleFontsize = 12
        self.scaleFontsize = self.initialScaleFontsize

        # value text status
        self.valueFontname = "Orbitron"
        self.initialValueFontsize = 40
        self.valueFontsize = self.initialValueFontsize
        self.textRadiusFactor = 0.5

        # enable bargraph
        self.enableBarGraph = True
        
        # fill polygon color
        self.enableFilledPolygon = True

        # needle scale factor/length
        self.needleScaleFactor = 0.8

        # dial units
        self.units = "b"

        self.update()

        # set theme
        self.setScalePolygonColors([[.00, Qt.red],
                                       [.1, Qt.yellow],
                                       [.15, Qt.green],
                                       [1, Qt.transparent]])

        self.needleCenterBg = [[0, QColor(35, 40, 3, 255)],
                                 [0.16, QColor(30, 36, 45, 255)],
                                 [0.225, QColor(36, 42, 54, 255)],
                                 [0.423963, QColor(19, 23, 29, 255)],
                                 [0.580645, QColor(45, 53, 68, 255)],
                                 [0.792627, QColor(59, 70, 88, 255)],
                                 [0.935, QColor(30, 35, 45, 255)],
                                 [1, QColor(35, 40, 3, 255)]]

        self.outerCircleBg = [[0.0645161, QColor(30, 30, 35, 255)],
                                [0.37788, QColor(57, 60, 75, 255)],
                                [1, QColor(30, 30, 35, 255)]]

        # resize dial
        self.rescaleMethod()

        self.previous = (0, 0, 0, 0)

        timer = QTimer(self)
        timer.timeout.connect(self.updateSpeed)
        timer.start(1000)

    """
    runs track speed to keep dial updated with correct value
    :param self:
    :return: none
    """
    def updateSpeed(self):
        x = trackSpeed(self.previous[2], self.previous[3], 1)
        self.previous = x
        download = x[1]
        if (download >= 1000000):
            self.setUnits("mb")
            download = download / 1000000
        elif (download >= 1000):
            self.setUnits("kb")
            download = download / 1000
        else:
            self.setUnits("b")
        
        self.updateValue(download)

    """
    updates dial parameters when resized
    :param self:
    :return: none
    """
    def rescaleMethod(self):
        
        # set h and w
        if self.width() <= self.height():
            self.widgetDiameter = self.width()
        else:
            self.widgetDiameter = self.height()

        # set needle size
        self.changeValueNeedleStyle([QPolygon([QPoint(4, 30),
                                                  QPoint(-4, 30),
                                                  QPoint(-2, int(- self.widgetDiameter / 2 * self.needleScaleFactor)),
                                                  QPoint(0, int(- self.widgetDiameter / 2 * self.needleScaleFactor - 6)),
                                                  QPoint(2, int(- self.widgetDiameter / 2 * self.needleScaleFactor))])])

        #set font size
        self.scaleFontsize = int(self.initialScaleFontsize * self.widgetDiameter / 400)
        self.valueFontsize = int(self.initialValueFontsize * self.widgetDiameter / 400)

    """
    change needle size
    :param self:
    :param design: needle dimensions
    :return: none
    """
    def changeValueNeedleStyle(self, design):
        self.valueNeedle = []
        for i in design:
            self.valueNeedle.append(i)
        self.update()

    """
    changes the current value displayed by dial
    :param self:
    :param value: new value
    :return: none
    """
    def updateValue(self, value):
        if value <= self.minValue:
            self.value = self.minValue
        elif value >= self.maxValue:
            self.value = self.maxValue
        else:
            self.value = value

        self.update()

    """
    changes the current units displayed by dial
    :param self:
    :return: none
    """
    def setUnits(self, units):
        self.units = units

    """
    changes the current minimum value displayed by dial
    :param self:
    :param min: new min value
    :return: none
    """
    def setMinValue(self, min):
        if self.value < min:
            self.value = min
        if min >= self.maxValue:
            self.minValue = self.maxValue - 1
        else:
            self.minValue = min

        self.update()

    """
    changes the current maximum value displayed by dial
    :param self:
    :param max: new max value
    :return: none
    """
    def setMaxValue(self, max):
        if self.value > max:
            self.value = max
        if max <= self.minValue:
            self.maxValue = self.minValue + 1
        else:
            self.maxValue = max

        self.update()

    """
    sets the color for the measurement bar of the dial
    :param self:
    :param colorArray: array of colors
    :return: none
    """
    def setScalePolygonColors(self, colorArray):
        if 'list' in str(type(colorArray)):
            self.scalePolygonColors = colorArray
        elif colorArray == None:
            self.scalePolygonColors = [[.0, Qt.transparent]]
        else:
            self.scalePolygonColors = [[.0, Qt.transparent]]

        self.update()

    """
    helper function that sections circle into slices
    :param self:
    :param outerRadius: outer radius of the circle
    :param innerRadius: inner radius of the circle
    :param start: start degree
    :param length: length of the pie
    :param barGraph:
    :return: polygon pie
    """
    def createPolygonPie(self, outerRadius, innerRaduis, start, lenght, barGraph=True):
        polygonPie = QPolygonF()

        n = 360     # angle steps size for full circle
        # changing n value will causes drawing issues
        w = 360 / n   # angle per step
        # create outer circle line from "start"-angle to "start + lenght"-angle
        x = 0
        y = 0

        if not self.enableBarGraph and barGraph:
            lenght = int(
                round((lenght / (self.maxValue - self.minValue)) * (self.value - self.minValue)))
            pass

        # add the points of polygon
        for i in range(lenght + 1):
            t = w * i + start - self.angleOffset
            x = outerRadius * math.cos(math.radians(t))
            y = outerRadius * math.sin(math.radians(t))
            polygonPie.append(QPointF(x, y))
        # create inner circle line from "start + lenght"-angle to "start"-angle
        # add the points of polygon
        for i in range(lenght + 1):
            t = w * (lenght - i) + start - self.angleOffset
            x = innerRaduis * math.cos(math.radians(t))
            y = innerRaduis * math.sin(math.radians(t))
            polygonPie.append(QPointF(x, y))

        # close outer line
        polygonPie.append(QPointF(x, y))
        return polygonPie

    """
    draws the measurement bar of the dial
    :param self:
    :param outlinePenWidth: width of the border
    :return: none
    """
    def drawFilledPolygon(self, outlinePenWith=0):
        if not self.scalePolygonColors == None:
            painterFilledPolygon = QPainter(self)
            painterFilledPolygon.setRenderHint(QPainter.Antialiasing)
            # place the coordinate origin in the middle of the area
            painterFilledPolygon.translate(
                self.width() / 2, self.height() / 2)

            painterFilledPolygon.setPen(Qt.NoPen)

            self.pen.setWidth(outlinePenWith)
            if outlinePenWith > 0:
                painterFilledPolygon.setPen(self.pen)

            coloredScalePolygon = self.createPolygonPie(
                ((self.widgetDiameter / 2) - (self.pen.width() / 2)) *
                self.gaugeColorOuterRadiusFactor,
                (((self.widgetDiameter / 2) - (self.pen.width() / 2))
                 * self.gaugeColorInnerRadiusFactor),
                self.scaleAngleStartValue, self.scaleAngleSize)

            grad = QConicalGradient(QPointF(0, 0), - self.scaleAngleSize - self.scaleAngleStartValue +
                                    self.angleOffset - 1)

            for eachcolor in self.scalePolygonColors:
                grad.setColorAt(eachcolor[0], eachcolor[1])

            painterFilledPolygon.setBrush(grad)

            painterFilledPolygon.drawPolygon(coloredScalePolygon)

    """
    draws the big scaled markers on dial
    :param self:
    :return: none
    """
    def drawBigScaledMarker(self):
        myPainter = QPainter(self)
        myPainter.setRenderHint(QPainter.Antialiasing)
        # place the coordinate origin in the middle of the area
        myPainter.translate(self.width() / 2, self.height() / 2)

        self.pen = QPen(self.bigScaleMarker)
        self.pen.setWidth(2)
        myPainter.setPen(self.pen)

        myPainter.rotate(self.scaleAngleStartValue - self.angleOffset)
        stepsSize = (float(self.scaleAngleSize) / float(self.scalaCount))
        scaleLineOuterStart = self.widgetDiameter // 2
        scaleLineLenght = int((self.widgetDiameter / 2) -
                                (self.widgetDiameter / 20))
        for i in range(self.scalaCount + 1):
            myPainter.drawLine(scaleLineLenght, 0,
                                scaleLineOuterStart, 0)
            myPainter.rotate(stepsSize)

    """
    draws the values on each scalar marker
    :param self:
    :return: none
    """
    def createScaleMarkerValuesText(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # place the coordinate origin in the middle of the area
        painter.translate(self.width() / 2, self.height() / 2)
        font = QFont(self.scaleFontname, self.scaleFontsize, QFont.Bold)
        fm = QFontMetrics(font)

        penShadow = QPen()

        penShadow.setBrush(self.ScaleValueColor)
        painter.setPen(penShadow)

        textRadiusFactor = 0.8
        textRadius = self.widgetDiameter / 2 * textRadiusFactor

        scalePerDiv = int((self.maxValue - self.minValue) / self.scalaCount)

        angleDistance = (float(self.scaleAngleSize) /
                          float(self.scalaCount))
        for i in range(self.scalaCount + 1):
            text = str(int(self.minValue + scalePerDiv * i))
            w = fm.width(text) + 1
            h = fm.height()
            painter.setFont(QFont(self.scaleFontname,
                            self.scaleFontsize, QFont.Bold))
            angle = angleDistance * i + \
                float(self.scaleAngleStartValue - self.angleOffset)
            x = textRadius * math.cos(math.radians(angle))
            y = textRadius * math.sin(math.radians(angle))

            painter.drawText(int(x - w / 2), int(y - h / 2), int(w),
                             int(h), Qt.AlignCenter, text)

    """
    draws the fine scaled markers on dial
    :param self:
    :return: none
    """
    def createFineScaledMarker(self):
        #  Description_dict = 0
        myPainter = QPainter(self)

        myPainter.setRenderHint(QPainter.Antialiasing)
        # place the coordinate origin in the middle of the area
        myPainter.translate(self.width() / 2, self.height() / 2)

        myPainter.setPen(self.fineScaleColor)
        myPainter.rotate(self.scaleAngleStartValue - self.angleOffset)
        stepsSize = (float(self.scaleAngleSize) /
                      float(self.scalaCount * self.scalaSubdivCount))
        scaleLineOuterStart = self.widgetDiameter // 2
        scaleLineLenght = int(
            (self.widgetDiameter / 2) - (self.widgetDiameter / 40))
        for i in range((self.scalaCount * self.scalaSubdivCount) + 1):
            myPainter.drawLine(scaleLineLenght, 0,
                                scaleLineOuterStart, 0)
            myPainter.rotate(stepsSize)

    """
    draws the value display by dial as a number
    :param self:
    :return: none
    """
    def createValuesText(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        font = QFont(self.valueFontname, self.valueFontsize, QFont.Bold)
        fm = QFontMetrics(font)

        penShadow = QPen()

        penShadow.setBrush(self.DisplayValueColor)
        painter.setPen(penShadow)

        textRadius = self.widgetDiameter / 2 * self.textRadiusFactor

        text = str(int(self.value))
        w = fm.width(text) + 1
        h = fm.height()
        painter.setFont(QFont(self.valueFontname,
                        self.valueFontsize, QFont.Bold))

        angleEnd = float(self.scaleAngleStartValue +
                          self.scaleAngleSize - 360)
        angle = (angleEnd - self.scaleAngleStartValue) / \
            2 + self.scaleAngleStartValue

        x = textRadius * math.cos(math.radians(angle))
        y = textRadius * math.sin(math.radians(angle))
        painter.drawText(int(x - w / 2), int(y - h / 2), int(w),
                         int(h), Qt.AlignCenter, text)

    """
    draws the units dial is currently using
    :param self:
    :return: none
    """
    def createUnitsText(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        font = QFont(self.valueFontname, int(
            self.valueFontsize / 2.5), QFont.Bold)
        fm = QFontMetrics(font)

        penShadow = QPen()

        penShadow.setBrush(self.DisplayValueColor)
        painter.setPen(penShadow)

        textRadius = self.widgetDiameter / 2 * self.textRadiusFactor

        text = str(self.units)
        w = fm.width(text) + 1
        h = fm.height()
        painter.setFont(QFont(self.valueFontname, int(
            self.valueFontsize / 2.5), QFont.Bold))

        angleEnd = float(self.scaleAngleStartValue +
                          self.scaleAngleSize + 180)
        angle = (angleEnd - self.scaleAngleStartValue) / \
            2 + self.scaleAngleStartValue

        x = textRadius * math.cos(math.radians(angle))
        y = textRadius * math.sin(math.radians(angle))
        painter.drawText(int(x - w / 2) - 45, int(y - h / 2) + 80, int(w),
                         int(h), Qt.AlignCenter, text)

    """
    draws object needle rotates around
    :param self:
    :param diameter: diameter of the needle's center
    :return: none
    """
    def drawBigNeedleCenterPoint(self, diameter=30):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # place the coordinate origin in the middle of the area
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        
        coloredScalePolygon = self.createPolygonPie(
            ((self.widgetDiameter / 8) - (self.pen.width() / 2)),
            0,
            self.scaleAngleStartValue, 360, False)

        grad = QConicalGradient(QPointF(0, 0), 0)

        for eachcolor in self.needleCenterBg:
            grad.setColorAt(eachcolor[0], eachcolor[1])

        painter.setBrush(grad)

        painter.drawPolygon(coloredScalePolygon)

    """
    draws background of dial
    :param self:
    :param diameter: diameter of dial
    :return: none
    """
    def drawOuterCircle(self, diameter=30):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        coloredScalePolygon = self.createPolygonPie(
            ((self.widgetDiameter / 2) - (self.pen.width())), 0,
            self.scaleAngleStartValue / 10, 360, False)

        radialGradient = QRadialGradient(QPointF(0, 0), self.width())

        for eachcolor in self.outerCircleBg:
            radialGradient.setColorAt(eachcolor[0], eachcolor[1])

        painter.setBrush(radialGradient)

        painter.drawPolygon(coloredScalePolygon)

    """
    draws needle
    :param self:
    :return: none
    """
    def drawNeedle(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.NeedleColor)
        painter.rotate(((self.value - self.valueOffset - self.minValue) * self.scaleAngleSize /
                        (self.maxValue - self.minValue)) + 90 + self.scaleAngleStartValue)

        painter.drawConvexPolygon(self.valueNeedle[0])

    #events

    """
    calls rescale method when window is resized
    :param self:
    :param event: resize event
    :return: none
    """
    def resizeEvent(self, event):
        self.rescaleMethod()
    
    """
    paints the dial
    :param self:
    :param event: paint event
    :return: none
    """
    def paintEvent(self, event):
        # Main Drawing Event:
        # Will be executed on every change
        # vgl http://doc.qt.io/qt-4.8/qt-demos-affine-xform-cpp.html

        self.drawOuterCircle()
        # colored pie area
        if self.enableFilledPolygon:
            self.drawFilledPolygon()

        # draw scale marker lines
        self.createFineScaledMarker()    
        self.drawBigScaledMarker()    

        # draw scale marker value text
        self.createScaleMarkerValuesText()

        # Display Value
        self.createValuesText()
        self.createUnitsText()    

        self.drawNeedle()

        self.drawBigNeedleCenterPoint(
                diameter=(self.widgetDiameter / 6))