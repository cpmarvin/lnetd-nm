from graph import Graph
from node import Node
from interface import Interface
from utilities import *

import json
import math

from PyQt5 import QtCore, QtGui, QtWidgets

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

from lnetd_link import Link


class Rectangle(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, node):
        super(Rectangle, self).__init__(parent=None)
        self.icons = False
        self.node = node
        self.node_position = self.node.get_position()
        self.node_radius = Vector(self.node.get_radius() + 8).repeat(2)

        x1 = self.node_position[0]
        y1 = self.node_position[1]
        self.setPos(x1,y1)
        self.setRect(-self.node.radius/2,-self.node.radius/2,self.node.radius,self.node.radius)

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)

        # node ontop
        self.setZValue(1)

        self.grayBrush = QtGui.QBrush(QtCore.Qt.gray)
        self.redBrush = QtGui.QBrush(QtCore.Qt.red)
        self.whiteBrush = QtGui.QBrush(QtCore.Qt.white)

        # self.font_family: str = "Times New Roman"
        self.font_family = "Roboto"
        self.font_size: int = 18
        self.show_context = True

    def shape(self):
        """this is the selection area and colision detection"""
        path = QtGui.QPainterPath()
        path.addRect(
            self.rect()
        )
        return path

    def boundingRect(self):
        #return QRectF(*(self.node_position - self.node_radius), *(2 * self.node_radius))
        return self.rect()

    def paint(self, painter, option, widget=None):
        # super(Rectangle, self).paint(painter, option, widget)
        external = False

        if "ASN" in self.node.label:
            external = True

        painter.save()
        painter.setRenderHints(
            QtGui.QPainter.Antialiasing
            | QtGui.QPainter.TextAntialiasing
            | QtGui.QPainter.SmoothPixmapTransform
            | QtGui.QPainter.HighQualityAntialiasing,
            True,
        )

        if external:
            # print('External true',self.node.label)
            if self.node._failed:
                painter.setBrush(self.redBrush)
                img_png = QtGui.QPixmap(":/icons/cloud_down.png")
            elif option.state & QtWidgets.QStyle.State_Selected:
                painter.setBrush(self.grayBrush)
                img_png = QtGui.QPixmap(":/icons/cloud_selected.png")
            else:
                painter.setBrush(self.whiteBrush)
                img_png = QtGui.QPixmap(":/icons/cloud.png")
        else:
            # print('External false',self.node.label)
            if self.node._failed:
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
            # FIX ME allow images instead via config option, find proper icons for router , router_selected , router_down
            painter.setFont(QFont(self.font_family, self.font_size / 3.2))
            painter.drawPixmap(
               QRect(-self.node.radius/2,-self.node.radius/2,self.node.radius,self.node.radius),
                img_png,
            )
            painter.drawText(
                QRect(-self.node.radius/2,self.node.radius/4,self.node.radius,self.node.radius),
                Qt.AlignCenter,
                self.node.label,
            )
        else:
            painter.setFont(QFont(self.font_family, self.font_size / 3.2))
            #painter.drawEllipse(QPointF(*self.node_position), *self.node_radius)
            painter.drawEllipse(self.rect())
            painter.drawText(self.rect(),Qt.AlignCenter,self.node.label)

        painter.restore()

    def itemChange(self, change, value):
        # change 9 == positionchange
        if change == 9:
            new_pos = self.boundingRect().center() + value
            self.node.set_position(Vector(new_pos.x(), new_pos.y()))
            for item in self.scene().items():
                if isinstance(item, Link):
                    if item.link.target == self.node or item.source_node == self.node:
                        item.updatePosition()
        # update scene matrix
        self.prepareGeometryChange()
        self.update()
        # return super(Rectangle, self).itemChange(change, value)
        return value

    def contextMenuEvent(self, event):
        if not self.show_context:
            return
        scene = self.scene()
        cmenu = QMenu()
        selected_nodes = [item for item in scene.selectedItems() if isinstance(item,Rectangle)]
        if not self.node._failed and len(scene.selectedItems()) <= 1:
            fail_node = cmenu.addAction("Node Down")
        elif self.node._failed and len(scene.selectedItems()) <= 1:
            unfail_node = cmenu.addAction("Node Up")
        if len(scene.selectedItems()) <= 1:
            delete_node = cmenu.addAction("Delete Node")
            changeName = cmenu.addAction("Change Name")
            setAsSource = cmenu.addAction("Set As Source")
            setAsTarget = cmenu.addAction("Set As Target")
        if len(selected_nodes) == 2:
            add_interface = cmenu.addAction("Add Interface")
            show_path = cmenu.addAction("Show Path Info")
            setAsGroup = cmenu.addAction("Group")
        if len(selected_nodes) > 2:
            setAsGroup = cmenu.addAction("Group")

        action = cmenu.exec_(event.screenPos())
        if len(scene.selectedItems()) <=1:
            if not self.node._failed and action == fail_node:
                self.node._failed = True
                #print('fail node')
                if scene is not None:
                    scene.handleNodeActionDown(
                    self, "this is a message from Node Down GraphicsItem "
                )
            elif self.node._failed and action == unfail_node:
                self.node._failed = False
                #print('unfail node')
                if scene is not None:
                    scene.handleNodeActionUp(
                    self, "this is a message from Node Up GraphicsItem"
                )
            elif action == changeName:
                #print('change name')
                scene.handlechangeNodeName(
                self, "this is a message from NodeNameChange GraphicsItem")

            elif action == delete_node:
                #print('delete node')
                scene.handleNodeActionDelete(
                self, "this is a message from Node Up GraphicsItem")
            elif action == setAsSource:
                #print('set as source')
                scene.handleNodeActionSetAsSource(
                self, "this is a message from Node Up GraphicsItem")
            elif action == setAsTarget:
                #print('set as target')
                scene.handleNodeActionSetAsTarget(
                self, "this is a message from Node Up GraphicsItem")
        elif len(scene.selectedItems()) == 2:
            if action == add_interface:
                #print('add interface')
                scene.handleInterfaceAdd(
                self, "this is a message from interfaceAdd GraphicsItem")
            elif  action == show_path:
                #print('show path')
                scene.handleShowPath(self, "message")
            elif action == setAsGroup:
                #print('group')
                scene.handleNodeActionSetAsGroup(
                 self, "message from setAsGroup")
        elif len(scene.selectedItems()) > 1:
            if action == setAsGroup:
                #print('group')
                scene.handleNodeActionSetAsGroup(
                 self, "message from setAsGroup")
        self.update()
        super(Rectangle, self).contextMenuEvent(event)
