
import json
import math
from random import randrange

from PyQt5 import QtCore, QtGui, QtWidgets,sip

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
    QGraphicsItemGroup,
    QGraphicsItem
)

from lnetd_node import Rectangle
from utilities import Vector

class LnetdGroup(QGraphicsItemGroup):
    def __init__(self,node,scene):
        super(LnetdGroup, self).__init__()
        self.setFlag(QGraphicsItemGroup.ItemIsMovable)
        #self.setFlag(QGraphicsItemGroup.ItemIsSelectable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)
        #self.setFlag(QtWidgets.QGraphicsItem.ItemSendsScenePositionChanges)
        #self.setZValue(0)
        self.scene = scene
        self.hide = False
        #self.setHandlesChildEvents(false)
        #self.setFlag(QGraphicsItemGroup.ItemClipsChildrenToShape)
    def boundingRect(self):
        #return self.childrenBoundingRect()
        return self.childrenBoundingRect().adjusted(0, 0, 0, 0)

    def shape1(self):
        """this is the selection area and colision detection"""
        path = QtGui.QPainterPath()
        path.addRect(
            10,10,10,10
        )
        return path


    def paint(self,
              painter: QtGui.QPainter,
              option: QtWidgets.QStyleOptionGraphicsItem,
              widget: QtWidgets.QWidget = None):
        img_png = QtGui.QPixmap(":/icons/router.png")
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        painter.setBrush(QtGui.QBrush(QtCore.Qt.gray))
        r = self.boundingRect();
        #print(r)
        #painter.drawRect(QRect(10,10,10,10))
        #painter.drawRect(QRect(r.x(), r.y(), r.width(), r.height()))
        if self.hide:
            painter.setOpacity(1)
            painter.drawRect(QRect(r.x(), r.y(), r.width(), r.height()))
        else:
            painter.setOpacity(0.5)
            painter.drawRect(QRect(r.x(), r.y(), r.width(), r.height()))



    def itemChange(self, change, value):
        #print('group_change',change)
        # change 9 == positionchange
        if change == 9:
            for item in self.childItems():
                pos_br = item.sceneBoundingRect().center()
                item.node.set_position(Vector(pos_br.x(), pos_br.y()))
                item.prepareGeometryChange()
                item.update()
                self.scene.update()
        # update scene matrix
        self.prepareGeometryChange()
        #self.scene.update()
        #return super(LnetdGroup, self).itemChange(change, value)
        return value

    def contextMenuEvent(self, event):
        self.cmenu = QMenu()
        un_group = self.cmenu.addAction("Un-Group")
        if self.hide:
            un_hide = self.cmenu.addAction("Un-Hide")
            un_hide.setText('Un-hide Nodes')
        else:
            hide = self.cmenu.addAction("Hide")
            hide.setText('Hide Nodes')
        action = self.cmenu.exec_(event.screenPos())
        if action.text() == 'Un-hide Nodes':
            for item in self.childItems():
                item.show()
            self.hide = False
        elif action == hide:
            for item in self.childItems():
                item.hide()
            self.hide = True
        elif action == un_group:
            for item in self.childItems():
                self.removeFromGroup(item)
                self.scene.removeItem(item)
                self.scene.addItem(item)
                item.show()
                item.prepareGeometryChange()
            self.scene.destroyItemGroup(self)
        self.scene.update()
        # dont propagate event
        super(LnetdGroup, self).contextMenuEvent(event)
