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

class L1Scene(QtWidgets.QGraphicsScene):
    #nodeDown = QtCore.Signal(object)
    l1nodeDown = QtCore.pyqtSignal(object,object)
    l1nodeUp = QtCore.pyqtSignal(object,object)

    circuitUp =  QtCore.pyqtSignal(object,object)
    circuitDown = QtCore.pyqtSignal(object,object)

    load_l1_topology = QtCore.pyqtSignal(object)
    load_l1_dummy_topology = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(L1Scene, self).__init__(parent)
        self.setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)

    def mousePressEvent(self, event):
        self.update()
        super(L1Scene, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.update()
        super(L1Scene, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.update()
        super(L1Scene, self).mouseReleaseEvent(event)

    #--->Handle Item actions, links them to signal for mainwindow
    def handleNodeActionDown(self, nodeItem, message):
        """to handle node changes"""
        self.l1nodeDown.emit(self,nodeItem)

    def handleNodeActionUp(self, nodeItem, message):
        """to handle node changes"""
        self.l1nodeUp.emit(self,nodeItem)

    def handleInterfaceActionDown(self, interfaceItem, message):
        """to handle node changes"""
        self.circuitDown.emit(self,interfaceItem)

    def handleInterfaceActionUp(self, interfaceItem, message):
        """to handle node changes"""
        self.circuitUp.emit(self,interfaceItem)

    def contextMenuEvent(self,event):
        item = self.itemAt(event.scenePos().x(),event.scenePos().y(),QtGui.QTransform())
        if item:
            try:
                item.contextMenuEvent(event)
                return
            except:
                pass
        else:
            cmenu = QMenu()
            load_l1_topology = cmenu.addAction("Load L1 Topology")
            load_l1_dummy_topology = cmenu.addAction("Load Dummy L1 Topology")
            action = cmenu.exec_(event.screenPos())
            if action == load_l1_dummy_topology:
                self.load_l1_dummy_topology.emit(self)
            elif action == load_l1_topology:
                self.load_l1_topology.emit(self)
        #dont propagate event
        #super(GraphicsScene, self).contextMenuEvent(event)
