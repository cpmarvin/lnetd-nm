

from graph import Graph
from node import Node
from interface import Interface
from utilities import *

import json
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

from lnetd_link import Link


class Rectangle(QtWidgets.QGraphicsItem):


    def __init__(self, node):
        super(Rectangle, self).__init__(parent=None)
        self.icons = False
        self.node = node
        self.node_position = self.node.get_position()
        self.node_radius = Vector(self.node.get_radius()).repeat(2)

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)

        #node ontop
        self.setZValue(1)

        self.grayBrush = QtGui.QBrush(QtCore.Qt.gray)
        self.redBrush = QtGui.QBrush(QtCore.Qt.red)
        self.whiteBrush = QtGui.QBrush(QtCore.Qt.white)

        #self.font_family: str = "Times New Roman"
        self.font_family = "Roboto"
        self.font_size: int = 18

    def shape(self):
        """this is the selection area and colision detection"""
        path = QtGui.QPainterPath()
        path.addRect(QRectF(*(self.node_position - self.node_radius), *(2 * self.node_radius)))
        return path

    def boundingRect(self):
        return QRectF(*(self.node_position - self.node_radius), *(2 * self.node_radius))

    def paint(self, painter, option, widget=None):
        #super(Rectangle, self).paint(painter, option, widget)
        external = False

        if "ASN" in self.node.label:
            external = True

        painter.save()
        painter.setRenderHints( QtGui.QPainter.Antialiasing
            | QtGui.QPainter.TextAntialiasing
            | QtGui.QPainter.SmoothPixmapTransform
            | QtGui.QPainter.HighQualityAntialiasing, True )

        if external:
            #print('External true',self.node.label)
            if  self.node._failed:
                painter.setBrush(self.redBrush)
                img_png = QtGui.QPixmap(":/icons/cloud_down.png")
            elif option.state & QtWidgets.QStyle.State_Selected:
                painter.setBrush(self.grayBrush)
                img_png = QtGui.QPixmap(":/icons/cloud_selected.png")
            else:
                painter.setBrush(self.whiteBrush)
                img_png = QtGui.QPixmap(":/icons/cloud.png")
        else:
            #print('External false',self.node.label)
            if  self.node._failed:
                painter.setBrush(self.redBrush)
                img_png = QtGui.QPixmap(":/icons/router_down.png")
            elif option.state & QtWidgets.QStyle.State_Selected:
                painter.setBrush(self.grayBrush)
                img_png = QtGui.QPixmap(":/icons/router_new.png")
            else:
                painter.setBrush(self.whiteBrush)
                img_png = QtGui.QPixmap(":/icons/router.png")

        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1))


        if self.icons:
        #
        #FIX ME allow images instead via config option, find proper icons for router , router_selected , router_down
            painter.setFont(QFont(self.font_family, self.font_size / 2.2))
            painter.drawPixmap(QRect(*(self.node_position - self.node_radius), *(2 * self.node_radius)),img_png)
            painter.drawText(
                        QRectF(*(self.node_position - self.node_radius + (-5,25) ), *(2 * self.node_radius + (10,0))),
                        Qt.AlignCenter,
                        self.node.label,
                    )
        else:
            painter.setFont(QFont(self.font_family, self.font_size / 3))
            painter.drawEllipse(QPointF(*self.node_position), *self.node_radius)
            painter.drawText(
                        QRectF(*(self.node_position - self.node_radius  ), *(2 * (self.node_radius) )),
                        Qt.AlignCenter,
                        self.node.label,)

        painter.restore()

    def itemChange(self, change, value):
        #change 9 == positionchange
        if change == 9:
            new_pos = self.boundingRect().center() + value
            self.node.set_position(Vector(new_pos.x(),new_pos.y() ))
            for item in self.scene().items():
                if isinstance(item, Link):
                    if item.link.target == self.node or item.source_node == self.node :
                        item.updatePosition()
        #update scene matrix
        self.prepareGeometryChange();
        self.update()
        #return super(Rectangle, self).itemChange(change, value)
        return value

    def contextMenuEvent(self,event):
        scene = self.scene()
        cmenu = QMenu()
        if not self.node._failed:
            fail_node = cmenu.addAction("Node Down")
        else:
            unfail_node = cmenu.addAction("Node Up")
        if len(scene.selectedItems()) == 2:
            add_interface = cmenu.addAction("Add Interface")
        delete_node = cmenu.addAction("Delete Node")
        changeName = cmenu.addAction("Change Name")
        setAsSource = cmenu.addAction("Set As Source")
        action = cmenu.exec_(event.screenPos())
        if not self.node._failed and action == fail_node:
            self.node._failed = True
            if scene is not None:
                scene.handleNodeActionDown(self, 'this is a message from Node Down GraphicsItem ')
        elif self.node._failed and action == unfail_node:
            self.node._failed = False
            if scene is not None:
                scene.handleNodeActionUp(self,'this is a message from Node Up GraphicsItem')
        elif action == changeName:
            scene.handlechangeNodeName(self,"this is a message from NodeNameChange GraphicsItem")
        elif len(scene.selectedItems()) > 1 and action == add_interface :
            scene.handleInterfaceAdd(self,"this is a message from interfaceAdd GraphicsItem")
        elif action == delete_node:
            scene.handleNodeActionDelete(self,'this is a message from Node Up GraphicsItem')
        elif action == setAsSource:
            scene.handleNodeActionSetAsSource(self,'this is a message from Node Up GraphicsItem')

        self.update()
        super(Rectangle, self).contextMenuEvent(event)

