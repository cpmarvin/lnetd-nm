import math
from bisect import *
from PyQt5 import QtCore, QtGui, QtWidgets
from support import generate_path_config

from PyQt5.QtCore import (
    Qt,
    QSize,
    QTimer,
    QPointF,
    QRectF,
    QMetaObject,
    QRect,
    QCoreApplication,
    QPoint,
    QLineF,
    pyqtSlot,
)

from PyQt5.QtGui import (
    QPainter,
    QBrush,
    QPen,
    QFont,
    QIcon,
    QTransform,
    QPalette,
    QColor,
)
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QFrame,
    QCheckBox,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QFileDialog,
    QSizePolicy,
    QMenu,
    QSlider,
    QDialog,
    QComboBox,
    QLabel,
    QSpacerItem,
    QMainWindow,
    QMenuBar,
    QOpenGLWidget,
)

from graph import Graph
from node import Node
from interface import Interface

from utilities import Vector, distance
import configparser

file_path = generate_path_config()


config = configparser.ConfigParser()
config.read(file_path)

blue_threshold = config.get("threshold", "blue_threshold")
green_threshold = config.get("threshold", "green_threshold")
yellow_threshold = config.get("threshold", "yellow_threshold")
orange_threshold = config.get("threshold", "orange_threshold")


class Link(QtWidgets.QGraphicsLineItem):
    def __init__(self, source_node, link):
        super(Link, self).__init__(parent=None)
        self.source_node = source_node
        self.link = link
        self.show_latency = False
        self.link_width = 2.5
        # fix me here , set. self threshold for blue and then in paint create the dict
        self.blue_threshold = int(blue_threshold)
        self.green_threshold = int(green_threshold)
        self.yellow_threshold = int(yellow_threshold)
        self.orange_threshold = int(orange_threshold)

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)

        self.setAcceptHoverEvents(True)

        # self.font_family: str = "Times New Roman"
        self.font_family = "Roboto"
        self.font_size: int = 18
        self.show_context = True

    def updatePosition(self):
        self.prepareGeometryChange()
        self.update()

    def shape(self):
        """this is the selection area and colision detection"""
        path = QtGui.QPainterPath()
        path.addRect(self._generate_bounding_rect())

        return path

    def boundingRect(self):
        return self.shape().boundingRect()

    def itemChange(self, change, value):
        result = super(Link, self).itemChange(change, value)
        if isinstance(result, QtWidgets.QGraphicsLineItem):
            result = sip.cast(result, QtWidgets.QGraphicsLineItem)
        self.prepareGeometryChange()
        return result

    def paint(self, painter, option, widget=None):
        super(Link, self).paint(painter, option, widget)
        util = self.link.utilization()
        orangeColor = QColor(255, 165, 0)

        colour_values = {
            self.blue_threshold: QtCore.Qt.blue,
            self.green_threshold: QtCore.Qt.green,
            self.yellow_threshold: QtCore.Qt.yellow,
            self.orange_threshold: orangeColor,
        }

        colour_values_list = sorted(colour_values)
        link_color_index = bisect_left(colour_values_list, util)

        if self.link._failed:
            link_color = QtCore.Qt.red
        elif util == 0:
            link_color = QtCore.Qt.black
        elif util > int(orange_threshold):
            link_color = QtCore.Qt.magenta
        else:
            try:
                link_color_key = colour_values_list[link_color_index]
                link_color = colour_values[link_color_key]
                # print(util, link_color, link_color_index, link_color_key)
            except:
                # guard agains <100% thresholds value
                link_color = QtCore.Qt.magenta
        painter.save()
        painter.setFont(QFont(self.font_family, self.font_size / 3))

        if self.link.link_num % 2 == 0:
            targetDistance = self.link.link_num * 5
        else:
            targetDistance = (-self.link.link_num + 1) * 5
        # hours of calculation and still can't figure out where it's wrong
        n1_p = Vector(*self.source_node.get_position())
        n2_p = Vector(*self.link.target.get_position())
        x1_x0 = n2_p[0] - n1_p[0]
        y1_y0 = n2_p[1] - n1_p[1]

        if y1_y0 == 0:
            x2_x0 = 0
            y2_y0 = targetDistance
        else:
            angle = math.atan((x1_x0) / (y1_y0))
            x2_x0 = -targetDistance * math.cos(angle)
            y2_y0 = targetDistance * math.sin(angle)

        d0x = n1_p[0] + (1 * x2_x0)
        d0y = n1_p[1] + (1 * y2_y0)
        d1x = n2_p[0] + (1 * x2_x0)
        d1y = n2_p[1] + (1 * y2_y0)

        dx = (d1x - d0x,)
        dy = (d1y - d0y,)

        dr = math.sqrt(dx[0] * dx[0] + dy[0] * dy[0])

        endX = (d1x + d0x) / 2
        endY = (d1y + d0y) / 2

        len1 = dr - ((dr / 2) * math.sqrt(3))
        endX = endX + (len1 / dr)
        endY = endY + (len1 / dr)
        n1_p = Vector(d0x, d0y)
        n2_p = Vector(endX, endY)
        uv = (n2_p - n1_p).unit()
        d = distance(n1_p, n2_p)
        r = self.link.target.get_radius()
        arrow_head_pos = n2_p
        d = distance(n1_p, arrow_head_pos)
        uv_arrow = (arrow_head_pos - n1_p).unit()
        arrow_base_pos = n1_p + uv_arrow * (d - 2 * 2)
        nv_arrow = uv_arrow.rotated(math.pi / 2)

        painter.setRenderHints(
            QtGui.QPainter.Antialiasing
            | QtGui.QPainter.TextAntialiasing
            | QtGui.QPainter.SmoothPixmapTransform
            | QtGui.QPainter.HighQualityAntialiasing,
            True,
        )
        if self.link.highlight:
            painter.setPen(QPen(link_color, 3, 3))
        elif option.state & QtWidgets.QStyle.State_Selected:
            painter.setPen(QPen(link_color, 2, 4))
        else:
            painter.setPen(QPen(link_color, self.link_width ,Qt.SolidLine))

        painter.setBrush(QBrush(link_color, Qt.SolidPattern))

        painter.drawPolygon(
            QPointF(*arrow_head_pos),
            QPointF(*(arrow_base_pos + nv_arrow * 2)),
            QPointF(*(arrow_base_pos - nv_arrow * 2)),
        )

        painter.drawLine(QPointF(d0x, d0y), QPointF(endX, endY))

        painter.setPen(QtGui.QPen(link_color, 1))
        
        # text
        if endX - d0x > 0:
            link_paint = QLineF(QPointF(d0x, d0y), QPointF(endX, endY))
        else:
            link_paint = QLineF(QPointF(endX, endY), QPointF(d0x, d0y))
        mid = (arrow_base_pos + n1_p) / 2
        if self.show_latency:
            w_len = (
                len(str(self.link.metric) + str(self.link.latency) + "------") / 3 * r
                + r / 3
            )
        else:
            w_len = len(str(self.link.metric)) / 3 * r + r / 3
        weight_v = Vector(w_len, 2)
        weight_rectangle = QRectF(*(mid - weight_v), *(2 * weight_v))
        painter.save()
        center_of_rec_x = weight_rectangle.center().x()
        center_of_rec_y = weight_rectangle.center().y()
        painter.translate(center_of_rec_x, center_of_rec_y)
        rx = -(weight_v[0] * 0.5)
        ry = -(weight_v[1])
        painter.rotate(-link_paint.angle())
        new_rec = QRect(rx, ry, weight_v[0], 2 * weight_v[1])

        if self.link._failed:
            painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))

        elif option.state & QtWidgets.QStyle.State_Selected:
            pass

        painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))

        painter.setPen(QtGui.QPen(Qt.black, Qt.SolidLine))
        painter.drawRect(QRect(rx, ry, weight_v[0], 2 * weight_v[1]))

        painter.setFont(QFont(self.font_family, self.font_size / 3.3))
        painter.setPen(QPen(Qt.white, Qt.SolidLine))
        if self.show_latency:
            painter.drawText(
                new_rec,
                Qt.AlignCenter,
                str(self.link.metric) + " -- " + str(self.link.latency) + "/ms",
            )
        else:
            painter.drawText(new_rec, Qt.AlignCenter, str(self.link.metric))

        painter.restore()

        painter.restore()

    def mousePressEvent(self, event):
        self.update()
        super(Link, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.update()
        super(Link, self).mouseReleaseEvent(event)

    def hoverEnterEvent(self, event):
        util = str(self.link.utilization())
        self.setToolTip("Load:" + util + "%")

    def hoverLeaveEvent(self, event):
        pass

    def contextMenuEvent(self, event):
        if not self.show_context:
            return
        scene = self.scene()
        cmenu = QMenu()
        if not self.link._failed:
            fail_interface = cmenu.addAction("Interface Down")
        else:
            unfail_interface = cmenu.addAction("Interface Up")
        change_metric = cmenu.addAction("Edit Interface ")
        delete_interface = cmenu.addAction("Delete Interface ")
        action = cmenu.exec_(event.screenPos())

        if not self.link._failed and action == fail_interface:
            self.link._failed = True
            if scene is not None:
                scene.handleInterfaceActionDown(
                    self, "this is a message from Node Down GraphicsItem "
                )
        elif self.link._failed and action == unfail_interface:
            self.link._failed = False
            if scene is not None:
                scene.handleInterfaceActionUp(
                    self, "this is a message from Node Up GraphicsItem"
                )
        elif action == change_metric:
            if scene is not None:
                scene.handleInterfaceActionChange(
                    self, "this is a message from Node Down GraphicsItem "
                )
        elif action == delete_interface:
            if scene is not None:
                scene.handleInterfaceActionDelete(
                    self, "this is a message from Node Down GraphicsItem "
                )

        self.update()
        super(Link, self).contextMenuEvent(event)

    def _generate_bounding_rect(self):
        if self.link.link_num % 2 == 0:
            targetDistance = self.link.link_num * 5
        else:
            targetDistance = (-self.link.link_num + 1) * 5
        # hours of calculation and still can't figure out where it's wrong
        n1_p = Vector(*self.source_node.get_position())
        n2_p = Vector(*self.link.target.get_position())
        x1_x0 = n2_p[0] - n1_p[0]
        y1_y0 = n2_p[1] - n1_p[1]

        if y1_y0 == 0:
            x2_x0 = 0
            y2_y0 = targetDistance
        else:

            angle = math.atan((x1_x0) / (y1_y0))
            x2_x0 = -targetDistance * math.cos(angle)
            y2_y0 = targetDistance * math.sin(angle)

        d0x = n1_p[0] + (1 * x2_x0)
        d0y = n1_p[1] + (1 * y2_y0)
        d1x = n2_p[0] + (1 * x2_x0)
        d1y = n2_p[1] + (1 * y2_y0)

        dx = (d1x - d0x,)
        dy = (d1y - d0y,)

        dr = math.sqrt(dx[0] * dx[0] + dy[0] * dy[0])

        endX = (d1x + d0x) / 2
        endY = (d1y + d0y) / 2

        len1 = dr - ((dr / 2) * math.sqrt(3))
        endX = endX + (len1 / dr)
        endY = endY + (len1 / dr)

        n1_p = Vector(d0x, d0y)
        n2_p = Vector(endX, endY)

        uv = (n2_p - n1_p).unit()
        d = distance(n1_p, n2_p)
        r = self.link.target.get_radius()
        arrow_head_pos = n2_p
        d = distance(n1_p, arrow_head_pos)
        uv_arrow = (arrow_head_pos - n1_p).unit()
        arrow_base_pos = n1_p + uv_arrow * (d - 2 * 2)
        nv_arrow = uv_arrow.rotated(math.pi / 2)
        # text
        if endX - d0x > 0:
            link_paint = QLineF(QPointF(d0x, d0y), QPointF(endX, endY))
        else:
            link_paint = QLineF(QPointF(endX, endY), QPointF(d0x, d0y))

        mid = (arrow_base_pos + n1_p) / 2
        w_len = len(str(self.link.metric)) / 3 * r + r / 3
        weight_v = Vector(w_len, 2)
        weight_rectangle = QRectF(*(mid - weight_v), *(2 * weight_v))
        center_of_rec_x = weight_rectangle.center().x()
        center_of_rec_y = weight_rectangle.center().y()

        new_rec = QRectF(
            center_of_rec_x - 10, center_of_rec_y - 10, 20, 20
        ).normalized()
        return new_rec
