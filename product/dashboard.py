import math
import sys

from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QColor, QFont, QPainter, QRadialGradient, QPolygon, QPen
from PyQt5.QtWidgets import QApplication, QWidget, QLCDNumber, QFrame


class Dashboard(QWidget):
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

    def setTitle(self, title):
        self._title = title

    def setValue(self, value):
        self.currentValue = value

    def paintEvent(self, event):
        # 坐标轴变换 默认640*480
        width = self.width()
        height = self.height()

        painter = QPainter(self)  # initialize painter
        painter.translate(width / 2, height / 2)  # use translate() to make the dashboard to the center of the UI

        # pick the min for the side
        side = min(width, height)
        painter.scale(side / 200.0, side / 200.0)
        # 本项目中将坐标缩小为side/200倍，即画出length=10的直线，其实际长度应为10*(side/200)。

        # 启用反锯齿，使画出的曲线更平滑
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        painter.begin(self)

        # 开始画图
        self.drawColorPie(painter)
        self.drawPointerIndicator(painter)
        self.drawLine(painter)
        self.drawText(painter)
        # self.drawTitle(painter)


    def drawColorPie(self, painter):  # 绘制三色环
        painter.save()  # save()保存当前坐标系
        # print("drawColorPie")
        # 设置扇形部分区域
        radius = 99  # 半径
        painter.setPen(Qt.NoPen)
        rect = QRectF(-radius, -radius, radius * 2, radius * 2)  # 扇形所在圆区域

        # 计算三色圆环范围角度。green：blue：red = 1：2：1
        angleAll = 360.0 - self.startAngle - self.endAngle  # self.startAngle = 45, self.endAngle = 45
        angleStart = angleAll * 0.25
        angleMid = angleAll * 0.5
        angleEnd = angleAll * 0.25

        # 圆的中心部分填充为透明色，形成环的样式
        rg = QRadialGradient(0, 0, radius, 0, 0)  # 起始圆心坐标，半径，焦点坐标
        ratio = 0.8  # 透明：实色 = 0.8 ：1

        # 绘制绿色环
        rg.setColorAt(0, Qt.transparent)  # 透明色
        rg.setColorAt(ratio, Qt.transparent)
        rg.setColorAt(ratio + 0.01, self.pieColorStart)
        rg.setColorAt(1, self.pieColorStart)

        painter.setBrush(rg)
        painter.drawPie(rect, (270 - self.startAngle - angleStart) * 16, angleStart * 16)

        # 绘制蓝色环
        rg.setColorAt(0, Qt.transparent)
        rg.setColorAt(ratio, Qt.transparent)
        rg.setColorAt(ratio + 0.01, self.pieColorMid)
        rg.setColorAt(1, self.pieColorMid)

        painter.setBrush(rg)
        painter.drawPie(rect, (270 - self.startAngle - angleStart - angleMid) * 16, angleMid * 16)

        # 绘制红色环
        rg.setColorAt(0, Qt.transparent)
        rg.setColorAt(ratio, Qt.transparent)
        rg.setColorAt(ratio + 0.01, self.pieColorEnd)
        rg.setColorAt(1, self.pieColorEnd)

        painter.setBrush(rg)
        painter.drawPie(rect, (270 - self.startAngle - angleStart - angleMid - angleEnd) * 16, angleEnd * 16)

        painter.restore()  # restore()恢复坐标系

    def drawPointerIndicator(self, painter):
        painter.save()
        # 绘制指针
        # print("drawPointerIndicator")
        radius = 58  # 指针长度
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.pointerColor)

        # (-5, 0), (0, -8), (5, 0)和（0, radius) 四个点绘出指针形状
        # 绘制多边形做指针
        pts = QPolygon()
        pts.setPoints(-5, 0, 0, -8, 5, 0, 0, radius)
        # print("radius:" + str(radius))

        # 旋转指针，使得指针起始指向为0刻度处
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

    def drawText(self, painter):
        painter.save()
        # 绘制刻度值
        # print("drawText")
        # 位置调整
        startRad = 4
        deltaRad = 0.6
        radius = 63
        offset = 5.5
  
        for i in range(self.scaleMajor + 1):  # self.scaleMajor = 8, 8个主刻度
            # 正余弦计算
            sina = math.sin(startRad - i * deltaRad)
            cosa = math.cos(startRad - i * deltaRad)

            # 刻度值计算
            value = math.ceil((1.0 * i * (
                    (self.maxValue - self.minValue) / self.scaleMajor) + self.minValue))
            # math.ceil(x)：返回不小于x的最小整数
            strValue = str(int(value))

            # 字符的宽度和高度
            textWidth = self.fontMetrics().width(strValue)
            textHeight = self.fontMetrics().height()

            # 字符串的起始位置。注意考虑到字符宽度和高度进行微调
            x = radius * cosa - textWidth / 2
            y = -radius * sina + textHeight / 4

            painter.setFont(self.font)
            painter.setPen(QColor(26, 95, 95))  # 还是用自己选的颜色
            painter.drawText(x - offset, y, str(self.bin_[i])+ 'm')
            # 可以不加，直接在 Title 中进行总体设置也行
        painter.restore()

    def drawLine(self, painter):
        painter.save()
        # 绘制刻度线
        # print("drawLine")
        radius = 79
        painter.rotate(self.startAngle)  # self.startAngle = 45,旋转45度
        steps = self.scaleMajor  # 8个刻度
        angleStep = (360.0 - self.startAngle - self.endAngle) / steps  # 刻度角
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
