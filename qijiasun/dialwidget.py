import os
import math
import track_speed

try:
    from PyQt5.QtWidgets import QWidget

    from PyQt5.QtGui import QPolygon, QPolygonF, QColor, QPen, QFont, QPainter, QFontMetrics, QConicalGradient, QRadialGradient, QFontDatabase

    from PyQt5.QtCore import Qt, QPoint, QPointF, QRect, QSize, QObject, pyqtSignal, QTimer

except:
    print("Error while importing PyQt5")
    exit()

# dialwidget

class DialWidget(QWidget):
    
    valueChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super(DialWidget, self).__init__(parent)

        # needle color: red
        self.NeedleColor = Qt.red

        # scale text color: neon green
        self.ScaleValueColor = QColor(57, 255, 20, 255)

        # value color: neon green
        self.DisplayValueColor = QColor(57, 255, 20, 255)

        # center pointer color: black
        self.CenterPointColor = Qt.black

        self.value_needle = QObject

        # default min and max
        self.minValue = 0
        self.maxValue = 1000

        # start value
        self.value = self.minValue

        # default offset
        self.value_offset = 0

        # default radius
        self.gauge_color_outer_radius_factor = 1
        self.gauge_color_inner_radius_factor = 0.9

        self.center_horizontal_value = 0
        self.center_vertical_value = 0

        #3 default scale value
        self.scale_angle_start_value = 135
        self.scale_angle_size = 270

        self.angle_offset = 0

        self.scalaCount = 10
        self.scala_subdiv_count = 5

        self.pen = QPen(QColor(0, 0, 0))

        # load font
        QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(__file__), 'fonts/Orbitron/Orbitron-VariableFont_wght.ttf'))

        # default polygon color
        self.scale_polygon_colors = []

        # big scale color: black
        self.bigScaleMarker = Qt.black

        # fine scale color: black
        self.fineScaleColor = Qt.black

        # scale text status
        self.scale_fontname = "Orbitron"
        self.initial_scale_fontsize = 12
        self.scale_fontsize = self.initial_scale_fontsize

        # value text status
        self.value_fontname = "Orbitron"
        self.initial_value_fontsize = 40
        self.value_fontsize = self.initial_value_fontsize
        self.text_radius_factor = 0.5

        # enable bargraph
        self.enableBarGraph = True
        
        # fill polygon color
        self.enable_filled_Polygon = True

        # needle scale factor/length
        self.needle_scale_factor = 0.8

        # dial units
        self.units = "b"

        self.update()

        # set theme
        self.set_scale_polygon_colors([[.00, Qt.red],
                                       [.1, Qt.yellow],
                                       [.15, Qt.green],
                                       [1, Qt.transparent]])

        self.needle_center_bg = [[0, QColor(35, 40, 3, 255)],
                                 [0.16, QColor(30, 36, 45, 255)],
                                 [0.225, QColor(36, 42, 54, 255)],
                                 [0.423963, QColor(19, 23, 29, 255)],
                                 [0.580645, QColor(45, 53, 68, 255)],
                                 [0.792627, QColor(59, 70, 88, 255)],
                                 [0.935, QColor(30, 35, 45, 255)],
                                 [1, QColor(35, 40, 3, 255)]]

        self.outer_circle_bg = [[0.0645161, QColor(30, 30, 35, 255)],
                                [0.37788, QColor(57, 60, 75, 255)],
                                [1, QColor(30, 30, 35, 255)]]

        # resize dial
        self.rescale_method()

        self.previous = (0, 0, 0, 0)

        timer = QTimer(self)
        timer.timeout.connect(self.updatespeed)
        timer.start(1000)

    # update speed
    def updatespeed(self):
        x = track_speed.track_speed(self.previous[2], self.previous[3], 1)
        print(x)
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

    # rescale

    def rescale_method(self):
        
        # set h and w
        if self.width() <= self.height():
            self.widget_diameter = self.width()
        else:
            self.widget_diameter = self.height()

        # set needle size
        self.change_value_needle_style([QPolygon([QPoint(4, 30),
                                                  QPoint(-4, 30),
                                                  QPoint(-2, int(- self.widget_diameter / 2 * self.needle_scale_factor)),
                                                  QPoint(0, int(- self.widget_diameter / 2 * self.needle_scale_factor - 6)),
                                                  QPoint(2, int(- self.widget_diameter / 2 * self.needle_scale_factor))])])

        #set font size
        self.scale_fontsize = int(self.initial_scale_fontsize * self.widget_diameter / 400)
        self.value_fontsize = int(self.initial_value_fontsize * self.widget_diameter / 400)

    def change_value_needle_style(self, design):
        # prepared for multiple needle instrument
        self.value_needle = []
        for i in design:
            self.value_needle.append(i)
        self.update()

    #update value
    def updateValue(self, value):
        if value <= self.minValue:
            self.value = self.minValue
        elif value >= self.maxValue:
            self.value = self.maxValue
        else:
            self.value = value
        self.valueChanged.emit(int(value))

        self.update()

    def updateAngleOffset(self, offset):
        self.angle_offset = offset
        self.update()

    def center_horizontal(self, value):
        self.center_horizontal_value = value

    def center_vertical(self, value):
        self.center_vertical_value = value

    # set label
    def setUnits(self, units):
        self.units = units

    # set min value
    def setMinValue(self, min):
        if self.value < min:
            self.value = min
        if min >= self.maxValue:
            self.minValue = self.maxValue - 1
        else:
            self.minValue = min

        self.update()

    # set max value
    def setMaxValue(self, max):
        if self.value > max:
            self.value = max
        if max <= self.minValue:
            self.maxValue = self.minValue + 1
        else:
            self.maxValue = max

        self.update()

    # set scale polygon colors
    def set_scale_polygon_colors(self, color_array):
        if 'list' in str(type(color_array)):
            self.scale_polygon_colors = color_array
        elif color_array == None:
            self.scale_polygon_colors = [[.0, Qt.transparent]]
        else:
            self.scale_polygon_colors = [[.0, Qt.transparent]]

        self.update()

    # get max value
    def get_value_max(self):
        return self.maxValue

    # create pie
    def create_polygon_pie(self, outer_radius, inner_raduis, start, lenght, bar_graph=True):
        polygon_pie = QPolygonF()

        n = 360     # angle steps size for full circle
        # changing n value will causes drawing issues
        w = 360 / n   # angle per step
        # create outer circle line from "start"-angle to "start + lenght"-angle
        x = 0
        y = 0

        if not self.enableBarGraph and bar_graph:
            lenght = int(
                round((lenght / (self.maxValue - self.minValue)) * (self.value - self.minValue)))
            pass

        # add the points of polygon
        for i in range(lenght + 1):
            t = w * i + start - self.angle_offset
            x = outer_radius * math.cos(math.radians(t))
            y = outer_radius * math.sin(math.radians(t))
            polygon_pie.append(QPointF(x, y))
        # create inner circle line from "start + lenght"-angle to "start"-angle
        # add the points of polygon
        for i in range(lenght + 1):
            t = w * (lenght - i) + start - self.angle_offset
            x = inner_raduis * math.cos(math.radians(t))
            y = inner_raduis * math.sin(math.radians(t))
            polygon_pie.append(QPointF(x, y))

        # close outer line
        polygon_pie.append(QPointF(x, y))
        return polygon_pie

    def draw_filled_polygon(self, outline_pen_with=0):
        if not self.scale_polygon_colors == None:
            painter_filled_polygon = QPainter(self)
            painter_filled_polygon.setRenderHint(QPainter.Antialiasing)
            # place the coordinate origin in the middle of the area
            painter_filled_polygon.translate(
                self.width() / 2, self.height() / 2)

            painter_filled_polygon.setPen(Qt.NoPen)

            self.pen.setWidth(outline_pen_with)
            if outline_pen_with > 0:
                painter_filled_polygon.setPen(self.pen)

            colored_scale_polygon = self.create_polygon_pie(
                ((self.widget_diameter / 2) - (self.pen.width() / 2)) *
                self.gauge_color_outer_radius_factor,
                (((self.widget_diameter / 2) - (self.pen.width() / 2))
                 * self.gauge_color_inner_radius_factor),
                self.scale_angle_start_value, self.scale_angle_size)

            gauge_rect = QRect(QPoint(0, 0), QSize(
                int(self.widget_diameter / 2 - 1), int(self.widget_diameter - 1)))
            grad = QConicalGradient(QPointF(0, 0), - self.scale_angle_size - self.scale_angle_start_value +
                                    self.angle_offset - 1)

            for eachcolor in self.scale_polygon_colors:
                grad.setColorAt(eachcolor[0], eachcolor[1])

            painter_filled_polygon.setBrush(grad)

            painter_filled_polygon.drawPolygon(colored_scale_polygon)
            # return painter_filled_polygon

    # big scale markers
    def draw_big_scaled_marker(self):
        my_painter = QPainter(self)
        my_painter.setRenderHint(QPainter.Antialiasing)
        # place the coordinate origin in the middle of the area
        my_painter.translate(self.width() / 2, self.height() / 2)

        self.pen = QPen(self.bigScaleMarker)
        self.pen.setWidth(2)
        my_painter.setPen(self.pen)

        my_painter.rotate(self.scale_angle_start_value - self.angle_offset)
        steps_size = (float(self.scale_angle_size) / float(self.scalaCount))
        scale_line_outer_start = self.widget_diameter // 2
        scale_line_lenght = int((self.widget_diameter / 2) -
                                (self.widget_diameter / 20))
        for i in range(self.scalaCount + 1):
            my_painter.drawLine(scale_line_lenght, 0,
                                scale_line_outer_start, 0)
            my_painter.rotate(steps_size)

    def create_scale_marker_values_text(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # place the coordinate origin in the middle of the area
        painter.translate(self.width() / 2, self.height() / 2)
        font = QFont(self.scale_fontname, self.scale_fontsize, QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.ScaleValueColor)
        painter.setPen(pen_shadow)

        text_radius_factor = 0.8
        text_radius = self.widget_diameter / 2 * text_radius_factor

        scale_per_div = int((self.maxValue - self.minValue) / self.scalaCount)

        angle_distance = (float(self.scale_angle_size) /
                          float(self.scalaCount))
        for i in range(self.scalaCount + 1):
            text = str(int(self.minValue + scale_per_div * i))
            w = fm.width(text) + 1
            h = fm.height()
            painter.setFont(QFont(self.scale_fontname,
                            self.scale_fontsize, QFont.Bold))
            angle = angle_distance * i + \
                float(self.scale_angle_start_value - self.angle_offset)
            x = text_radius * math.cos(math.radians(angle))
            y = text_radius * math.sin(math.radians(angle))

            painter.drawText(int(x - w / 2), int(y - h / 2), int(w),
                             int(h), Qt.AlignCenter, text)

    # fine scale markers
    def create_fine_scaled_marker(self):
        #  Description_dict = 0
        my_painter = QPainter(self)

        my_painter.setRenderHint(QPainter.Antialiasing)
        # place the coordinate origin in the middle of the area
        my_painter.translate(self.width() / 2, self.height() / 2)

        my_painter.setPen(self.fineScaleColor)
        my_painter.rotate(self.scale_angle_start_value - self.angle_offset)
        steps_size = (float(self.scale_angle_size) /
                      float(self.scalaCount * self.scala_subdiv_count))
        scale_line_outer_start = self.widget_diameter // 2
        scale_line_lenght = int(
            (self.widget_diameter / 2) - (self.widget_diameter / 40))
        for i in range((self.scalaCount * self.scala_subdiv_count) + 1):
            my_painter.drawLine(scale_line_lenght, 0,
                                scale_line_outer_start, 0)
            my_painter.rotate(steps_size)

    # value text
    def create_values_text(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        font = QFont(self.value_fontname, self.value_fontsize, QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.DisplayValueColor)
        painter.setPen(pen_shadow)

        text_radius = self.widget_diameter / 2 * self.text_radius_factor

        text = str(int(self.value))
        w = fm.width(text) + 1
        h = fm.height()
        painter.setFont(QFont(self.value_fontname,
                        self.value_fontsize, QFont.Bold))

        angle_end = float(self.scale_angle_start_value +
                          self.scale_angle_size - 360)
        angle = (angle_end - self.scale_angle_start_value) / \
            2 + self.scale_angle_start_value

        x = text_radius * math.cos(math.radians(angle))
        y = text_radius * math.sin(math.radians(angle))
        painter.drawText(int(x - w / 2), int(y - h / 2), int(w),
                         int(h), Qt.AlignCenter, text)

    # units text
    def create_units_text(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        font = QFont(self.value_fontname, int(
            self.value_fontsize / 2.5), QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.DisplayValueColor)
        painter.setPen(pen_shadow)

        text_radius = self.widget_diameter / 2 * self.text_radius_factor

        text = str(self.units)
        w = fm.width(text) + 1
        h = fm.height()
        painter.setFont(QFont(self.value_fontname, int(
            self.value_fontsize / 2.5), QFont.Bold))

        angle_end = float(self.scale_angle_start_value +
                          self.scale_angle_size + 180)
        angle = (angle_end - self.scale_angle_start_value) / \
            2 + self.scale_angle_start_value

        x = text_radius * math.cos(math.radians(angle))
        y = text_radius * math.sin(math.radians(angle))
        painter.drawText(int(x - w / 2) - 45, int(y - h / 2) + 80, int(w),
                         int(h), Qt.AlignCenter, text)

    # center pointer
    def draw_big_needle_center_point(self, diameter=30):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # place the coordinate origin in the middle of the area
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        
        colored_scale_polygon = self.create_polygon_pie(
            ((self.widget_diameter / 8) - (self.pen.width() / 2)),
            0,
            self.scale_angle_start_value, 360, False)

        grad = QConicalGradient(QPointF(0, 0), 0)

        for eachcolor in self.needle_center_bg:
            grad.setColorAt(eachcolor[0], eachcolor[1])

        painter.setBrush(grad)

        painter.drawPolygon(colored_scale_polygon)
        # return painter_filled_polygon

    # create outer cover
    def draw_outer_circle(self, diameter=30):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        colored_scale_polygon = self.create_polygon_pie(
            ((self.widget_diameter / 2) - (self.pen.width())), 0,
            self.scale_angle_start_value / 10, 360, False)

        radialGradient = QRadialGradient(QPointF(0, 0), self.width())

        for eachcolor in self.outer_circle_bg:
            radialGradient.setColorAt(eachcolor[0], eachcolor[1])

        painter.setBrush(radialGradient)

        painter.drawPolygon(colored_scale_polygon)

    # needle pointer
    def draw_needle(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.NeedleColor)
        painter.rotate(((self.value - self.value_offset - self.minValue) * self.scale_angle_size /
                        (self.maxValue - self.minValue)) + 90 + self.scale_angle_start_value)

        painter.drawConvexPolygon(self.value_needle[0])

    #events

    # on window resize
    def resizeEvent(self, event):
        self.rescale_method()
    
    # on paint event
    def paintEvent(self, event):
        # Main Drawing Event:
        # Will be executed on every change
        # vgl http://doc.qt.io/qt-4.8/qt-demos-affine-xform-cpp.html

        self.draw_outer_circle()
        # colored pie area
        if self.enable_filled_Polygon:
            self.draw_filled_polygon()

        # draw scale marker lines
        self.create_fine_scaled_marker()    
        self.draw_big_scaled_marker()    

        # draw scale marker value text
        self.create_scale_marker_values_text()

        # Display Value
        self.create_values_text()
        self.create_units_text()    

        self.draw_needle()

        self.draw_big_needle_center_point(
                diameter=(self.widget_diameter / 6))