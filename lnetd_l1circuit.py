import math

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import Qt, QSize, QTimer, QPointF, QRectF, QMetaObject, QRect , QCoreApplication, QPoint, QLineF , pyqtSlot
from PyQt5.QtGui import QPainter, QBrush, QPen, QFont, QIcon, QTransform, QPalette, QColor
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
    QOpenGLWidget
)

from graph import Graph
from node import Node
from interface import Interface

from utilities import Vector,distance

class L1CircuitItem(QtWidgets.QGraphicsLineItem):
    def __init__(self, source_node, link):
        super(L1CircuitItem, self).__init__(parent=None)
        self.source_node = source_node
        self.link = link
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)
        self.setCursor(Qt.ArrowCursor)

        self.setAcceptHoverEvents(True)

        #self.font_family: str = "Times New Roman"
        self.font_family = "Roboto"
        self.font_size: int = 18

        self.arrow_separation = math.pi / 18
        self.weight_rectangle_size = 2

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
        result = super(L1CircuitItem, self).itemChange(change, value)
        if isinstance(result, QtWidgets.QGraphicsLineItem):
            result = sip.cast(result, QtWidgets.QGraphicsLineItem)
        self.prepareGeometryChange()
        return result

    def paint(self, painter, option, widget=None):
        super(L1CircuitItem, self).paint(painter, option, widget)

        painter.save()

        n1_p = Vector(*self.source_node.get_position())
        n2_p = Vector(*self.link.target.get_position())
        uv = (n2_p - n1_p).unit()

        start = n1_p + uv * self.source_node.get_radius()
        end = n2_p - uv * self.link.target.get_radius()

        #if multiple links ( always )
        if self.link.link_num % 2 == 0:
            targetDistance = self.link.link_num * 2
        else:
            targetDistance = (-self.link.link_num +1 ) * 2

        start = start.rotated_new(self.arrow_separation * targetDistance, n1_p)
        end = end.rotated_new(-self.arrow_separation * targetDistance, n2_p)

        if self.link._failed:
            link_color = Qt.red
        else:
            link_color = Qt.green

        painter.setPen(QPen(link_color, Qt.SolidLine))
        painter.drawLine(QPointF(*start), QPointF(*end))

        painter.setPen(QPen(Qt.black, Qt.SolidLine))
        painter.setBrush(
            QBrush(
                Qt.black,
                Qt.SolidPattern,
            )
        )
        #rect calculation
        r = self.weight_rectangle_size

        mid = (start + end) / 2

        w_len = len(str(self.link.label)) * 4

        weight_v = Vector(r if w_len <= r else w_len, r)

        weight_rectangle = QRectF(*(mid - weight_v), *(2 * weight_v))

        if end.unit()[0] - start.unit()[0] > 0:
            link_paint = QLineF(QPointF(*start), QPointF(*end))
        else:
            link_paint = QLineF(QPointF(*end), QPointF(*start))

        center_of_rec_x = weight_rectangle.center().x()
        center_of_rec_y  = weight_rectangle.center().y()

        painter.translate(center_of_rec_x, center_of_rec_y)

        rx = -(weight_v[0] * 0.5)
        ry = -(weight_v[1] )

        painter.rotate(- link_paint.angle());
        new_rec = QRect(rx , ry, weight_v[0], 2 * weight_v[1])
        painter.drawRect(QRect(rx , ry, weight_v[0] , 2 * weight_v[1] ))
        painter.setFont(QFont(self.font_family, self.font_size / 4))

        painter.setPen(QPen(Qt.white, Qt.SolidLine))

        painter.drawText(new_rec, Qt.AlignCenter, str(self.link.label))

        painter.restore()
        painter.setPen(QPen(Qt.black, Qt.SolidLine))
        painter.setFont(QFont(self.font_family, self.font_size / 3))
        #painter.restore()

    def mousePressEvent(self, event):
        self.update()
        super(L1CircuitItem, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.update()
        super(L1CircuitItem, self).mouseReleaseEvent(event)

    def hoverEnterEvent(self,event):
        links = self.link.interfaces
        message = "<p>L3 Interfaces:</p>"
        for entry in links:
            message += "<li>" + str(entry) +"</li>"
        self.setToolTip( message )

    def hoverLeaveEvent(self,event):
        pass

    def contextMenuEvent(self,event):
        scene = self.scene()
        cmenu = QMenu()
        if not self.link._failed:
            fail_interface = cmenu.addAction("Circuit Down")
        else:
            unfail_interface = cmenu.addAction("Circuit Up")

        action = cmenu.exec_(event.screenPos())

        if not self.link._failed and action == fail_interface:
            self.link._failed = True
            if scene is not None:
                scene.handleInterfaceActionDown(self, 'this is a message from Node Down GraphicsItem ')
        elif self.link._failed and action == unfail_interface :
            self.link._failed = False
            if scene is not None:
                scene.handleInterfaceActionUp(self,'this is a message from Node Up GraphicsItem')
        self.update()
        super(L1CircuitItem, self).contextMenuEvent(event)

    def _generate_bounding_rect(self):
        n1_p = Vector(*self.source_node.get_position())
        n2_p = Vector(*self.link.target.get_position())
        uv = (n2_p - n1_p).unit()

        start = n1_p + uv * self.source_node.get_radius()
        end = n2_p - uv * self.link.target.get_radius()

        #if multiple links ( always )
        if self.link.link_num % 2 == 0:
            targetDistance = self.link.link_num * 2
        else:
            targetDistance = (-self.link.link_num +1 ) * 2

        start = start.rotated_new(self.arrow_separation * targetDistance, n1_p)
        end = end.rotated_new(-self.arrow_separation * targetDistance, n2_p)

        if self.link._failed:
            link_color = Qt.red
        else:
            link_color = Qt.green

        #rect calculation
        r = self.weight_rectangle_size

        mid = (start + end) / 2

        w_len = len(str(self.link.label)) * 4

        weight_v = Vector(r if w_len <= r else w_len, r)

        weight_rectangle = QRectF(*(mid - weight_v), *(2 * weight_v))

        if end.unit()[0] - start.unit()[0] > 0:
            link_paint = QLineF(QPointF(*start), QPointF(*end))
        else:
            link_paint = QLineF(QPointF(*end), QPointF(*start))

        center_of_rec_x = weight_rectangle.center().x()
        center_of_rec_y  = weight_rectangle.center().y()

        rx = -(weight_v[0] * 0.5)
        ry = -(weight_v[1] )

        #new_rec = QRectF(rx , ry, weight_v[0], 2 * weight_v[1])

        new_rec = QRectF(center_of_rec_x - 10 ,center_of_rec_y - 10 ,15,15).normalized();
        return new_rec

