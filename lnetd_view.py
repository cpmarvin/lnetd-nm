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


class GraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super(GraphicsView, self).__init__(parent)
        # see https://doc.qt.io/qt-5/qgraphicsview.html#renderHints-prop
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setRenderHint(QtGui.QPainter.TextAntialiasing)
        self.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)

        # drag options
        # self.setDragMode(GraphicsView.ScrollHandDrag)
        self.setDragMode(GraphicsView.RubberBandDrag)

        # selection , what do i select , see https://doc.qt.io/qt-5/qt.html#ItemSelectionMode-enum
        self.setRubberBandSelectionMode(Qt.IntersectsItemBoundingRect)

        # postition the view on resize
        self.setResizeAnchor(GraphicsView.AnchorUnderMouse)

        # position the view on transformation
        self.setTransformationAnchor(GraphicsView.AnchorUnderMouse)

        # viewport see https://doc.qt.io/qt-5/qgraphicsview.html#ViewportUpdateMode-enum
        self.setViewportUpdateMode(GraphicsView.SmartViewportUpdate)

        self.scale(0.8, 0.8)

    def mouseMoveEvent(self, event):
        # print('enterEvent inside view')
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ShiftModifier:
            self.viewport().setCursor(Qt.ClosedHandCursor)
            self.setDragMode(GraphicsView.ScrollHandDrag)
        else:
            self.setDragMode(GraphicsView.RubberBandDrag)
            self.viewport().setCursor(Qt.ArrowCursor)
        super(GraphicsView, self).mouseMoveEvent(event)

    def mousePressEvent(self, event):
        # print('mousePressEvent inside view')

        super(GraphicsView, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        # print("mouseReleaseEvent inside view")
        super(GraphicsView, self).mouseReleaseEvent(event)

    def wheelEvent(self, event):
        """Zoom in/out"""
        self.scaleView(math.pow(2.0, event.angleDelta().y() / 240.0))

    def scaleView(self, scaleFactor):
        """Transform function and zoom
        QrecF is the area visible"""
        factor = (
            self.transform()
            .scale(scaleFactor, scaleFactor)
            .mapRect(QRectF(0, 0, 50, 50))
            .width()
        )
        if factor < 0.07 or factor > 100:
            return
        self.scale(scaleFactor, scaleFactor)
