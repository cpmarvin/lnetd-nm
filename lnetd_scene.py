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


class GraphicsScene(QtWidgets.QGraphicsScene):
    # nodeDown = QtCore.Signal(object)
    nodeDown = QtCore.pyqtSignal(object, object)
    nodeUp = QtCore.pyqtSignal(object, object)
    interfaceDown = QtCore.pyqtSignal(object, object)
    interfaceUp = QtCore.pyqtSignal(object, object)
    interfaceChange = QtCore.pyqtSignal(object, object)
    interfaceDelete = QtCore.pyqtSignal(object, object)
    addNode = QtCore.pyqtSignal(object, object, object)
    changeNodeName = QtCore.pyqtSignal(object, object)
    interfaceAdd = QtCore.pyqtSignal(object, object)
    showPath = QtCore.pyqtSignal(object, object)
    nodeDelete = QtCore.pyqtSignal(object, object)
    nodeSource = QtCore.pyqtSignal(object, object)
    nodeTarget = QtCore.pyqtSignal(object, object)
    nodeGroup = QtCore.pyqtSignal(object, object)

    def __init__(self, parent=None):
        super(GraphicsScene, self).__init__(parent)
        self.bluebrush = QtGui.QBrush(QtCore.Qt.blue)
        self.selected_item = None
        self.setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)

    def mousePressEvent(self, event):
        self.update()
        super(GraphicsScene, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.update()
        super(GraphicsScene, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.update()
        super(GraphicsScene, self).mouseReleaseEvent(event)

    # --->Handle Item actions, links them to signal for mainwindow
    def handleNodeActionDown(self, nodeItem, message):
        """to handle node changes"""
        self.nodeDown.emit(self, nodeItem)

    def handleNodeActionUp(self, nodeItem, message):
        """to handle node changes"""
        self.nodeUp.emit(self, nodeItem)

    def handleInterfaceActionDown(self, interfaceItem, message):
        """to handle node changes"""
        self.interfaceDown.emit(self, interfaceItem)

    def handleInterfaceActionUp(self, interfaceItem, message):
        """to handle node changes"""
        self.interfaceUp.emit(self, interfaceItem)

    def handleInterfaceActionChange(self, interfaceItem, message):

        self.interfaceChange.emit(self, interfaceItem)

    def handleInterfaceAdd(self, interfaceItem, message):

        self.interfaceAdd.emit(self, interfaceItem)

    def handleShowPath(self, interfaceItem, message):
        self.showPath.emit(self, interfaceItem)

    def handleInterfaceActionDelete(self, interfaceItem, message):

        self.interfaceDelete.emit(self, interfaceItem)

    def handlechangeNodeName(self, nodeItem, message):

        self.changeNodeName.emit(self, nodeItem)

    def handleNodeActionDelete(self, nodeItem, message):

        self.nodeDelete.emit(self, nodeItem)

    def handleNodeActionSetAsSource(self, nodeItem, message):
        self.nodeSource.emit(self, nodeItem)

    def handleNodeActionSetAsTarget(self, nodeItem, message):
        self.nodeTarget.emit(self, nodeItem)

    def handleNodeActionSetAsGroup(self, nodeItem, message):
        self.nodeGroup.emit(self, nodeItem)


    def contextMenuEvent(self, event):
        item = self.itemAt(
            event.scenePos().x(), event.scenePos().y(), QtGui.QTransform()
        )
        if item:
            try:
                item.contextMenuEvent(event)
                return
            except:
                pass
        else:
            cmenu = QMenu()
            add_node = cmenu.addAction("Add Node")
            action = cmenu.exec_(event.screenPos())
            if action == add_node:
                self.addNode.emit(self, event, event.screenPos())
        # dont propagate event
        # super(GraphicsScene, self).contextMenuEvent(event)
