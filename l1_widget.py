# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'l1_widget.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from lnetd_l1scene import L1Scene
import math

class Ui_L1_Widget(QtWidgets.QDialog):

    def setupUi(self, L1_Widget):
        L1_Widget.setObjectName("L1_Widget")
        L1_Widget.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(L1_Widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(1,1,1,1)

        self.scene = L1Scene()

        self.L1_View = GraphicsView(self.scene)
        self.L1_View.setRenderHints(QtGui.QPainter.HighQualityAntialiasing|QtGui.QPainter.TextAntialiasing)
        self.L1_View.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.L1_View.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.L1_View.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)
        self.L1_View.setObjectName("L1_View")
        self.verticalLayout.addWidget(self.L1_View)

        self.retranslateUi(L1_Widget)
        QtCore.QMetaObject.connectSlotsByName(L1_Widget)

    def retranslateUi(self, L1_Widget):
        _translate = QtCore.QCoreApplication.translate
        L1_Widget.setWindowTitle(_translate("L1_Widget", "L1 Topology"))


class GraphicsView(QtWidgets.QGraphicsView):

    def __init__(self, parent=None):
        super(GraphicsView, self).__init__(parent)
        #see https://doc.qt.io/qt-5/qgraphicsview.html#renderHints-prop
        self.setRenderHint( QtGui.QPainter.Antialiasing )
        self.setRenderHint( QtGui.QPainter.TextAntialiasing )
        self.setRenderHint( QtGui.QPainter.SmoothPixmapTransform )

        #drag options
        #self.setDragMode(GraphicsView.ScrollHandDrag)
        #self.setDragMode(GraphicsView.RubberBandDrag)

        #selection , what do i select , see https://doc.qt.io/qt-5/qt.html#ItemSelectionMode-enum
        #self.setRubberBandSelectionMode(Qt.IntersectsItemBoundingRect)

        #postition the view on resize
        #self.setResizeAnchor(GraphicsView.AnchorUnderMouse)

        #position the view on transformation
        #self.setTransformationAnchor(GraphicsView.AnchorUnderMouse)

        # viewport see https://doc.qt.io/qt-5/qgraphicsview.html#ViewportUpdateMode-enum
        #self.setViewportUpdateMode(GraphicsView.SmartViewportUpdate)

        self.scale(0.8, 0.8)

    def mouseMoveEvent(self,event):
        #print('enterEvent inside view')
        #self.viewport().setCursor(Qt.ClosedHandCursor)
        super(GraphicsView, self).mouseMoveEvent(event)

    def mousePressEvent(self,event):
        #print('mousePressEvent inside view')
        #self.viewport().setCursor(Qt.ClosedHandCursor)
        super(GraphicsView, self).mousePressEvent(event)

    def mouseReleaseEvent(self,event):
        #print('mouseReleaseEvent inside view')
        #self.viewport().setCursor(Qt.ArrowCursor)
        super(GraphicsView, self).mouseReleaseEvent(event)

    def wheelEvent(self, event):
        """Zoom in/out"""
        self.scaleView(math.pow(2.0, -event.angleDelta().y() / 240.0))

    def scaleView(self, scaleFactor):
        """Transform function and zoom
        QrecF is the area visible"""
        factor = self.transform().scale(scaleFactor, scaleFactor).mapRect(QtCore.QRectF(0, 0, 50, 50)).width()
        if factor < 0.07 or factor > 100:
            return
        self.scale(scaleFactor, scaleFactor)
