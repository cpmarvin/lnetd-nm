'''
from PyQt5 import QtCore, QtGui, QtWidgets

class MyFirstGuiProgram(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent=parent)
        self.setupUi(self)
        scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(scene)
        pen = QtGui.QPen(QtCore.Qt.green)

        side = 20

        for i in range(16):
            for j in range(16):
                r = QtCore.QRectF(QtCore.QPointF(i*side, j*side), QtCore.QSizeF(side, side))
                scene.addRect(r, pen)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MyFirstGuiProgram()
    w.show()
    sys.exit(app.exec_())
'''

from PyQt5 import QtCore, QtGui, QtWidgets


#-->
class GraphicsScene(QtWidgets.QGraphicsScene):
    def __init__(self, parent=None):
        super(GraphicsScene, self).__init__(QtCore.QRectF(-500, -500, 1000, 1000), parent)
        self._start = QtCore.QPointF()
        self._current_rect_item = None

    def mousePressEvent(self, event):
        print('mouse press')

        if self.itemAt(event.scenePos(), QtGui.QTransform()) is None:
            self._current_rect_item = QtWidgets.QGraphicsRectItem()
            self._current_rect_item.setBrush(QtCore.Qt.red)
            self._current_rect_item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
            self.addItem(self._current_rect_item)
            self._start = event.scenePos()
            r = QtCore.QRectF(self._start, self._start)
            self._current_rect_item.setRect(r)
        else:
            print('something under the cursor')

        super(GraphicsScene, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        print('mouse move')

        if self._current_rect_item is not None:
            r = QtCore.QRectF(self._start, event.scenePos()).normalized()
            self._current_rect_item.setRect(r)
        else:
            print('something under mouse event')

        super(GraphicsScene, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        print('mouse release')
        self._current_rect_item = None
        super(GraphicsScene, self).mouseReleaseEvent(event)

    def wheelEvent(self, event):
        print('wheel event')


#-->
class RectItem(QtWidgets.QGraphicsRectItem):
    def paint(self, painter, option, widget=None):
        super(RectItem, self).paint(painter, option, widget)
        painter.save()
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(QtCore.Qt.red)
        painter.drawEllipse(option.rect)
        painter.restore()

class RectItem1(QtWidgets.QGraphicsRectItem):
    #overwrite paint method
    def paint(self, painter, option, widget):
        print('RectItem')
        super(RectItem, self).paint(painter, option, widget)
        painter.save()
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(QtCore.Qt.gray)
        painter.drawEllipse(option.rect)
        painter.restore()

    def boundingRect(self):
        return QRectF(0,0,300,300)

    def mousePressEvent(self, event):
        print('mouse press Evendt',pos)
        pos = event.pos()
        self.update()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.scene = QtWidgets.QGraphicsScene(self)
        self.scene = GraphicsScene(self)
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.setCentralWidget(self.view)
        color = [QtGui.QColor.red,QtGui.QColor.blue]
        from random import randint
        self.node1_x = 10
        self.node1_y = 10
        self.node2_x = 30
        self.node2_y = 30

        rect_item = RectItem(self.node1_x, self.node1_y, 100, 30);
        #rect_item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        #rect_item.setFlag(QtWidgets.QGraphicsItem.acceptedMouseButtons, True)
        #line =  QtWidgets.QGraphicsRectItem(self.node1_x, self.node1_y, 100, 1);
        #line.setParentItem(rect_item)
        self.scene.addItem(rect_item)

        self.simulation_timer = QtCore.QTimer(
            interval=60, timeout=self.simulation
        )
        #self.simulation_timer.start()

    def simulation(self):
        print('sim')
        self.scene.update()

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec_())

'''
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_test_app2(QtWidgets.QWidget):
    def __init__(self,parent):
        super(Ui_test_app2, self).__init__(parent)

class Ui_test_app(QtWidgets.QWidget):
    def __init__(self,parent):
        super(Ui_test_app, self).__init__(parent)

    def setupUi(self):
        test_app.setObjectName("test_app")
        test_app.resize(800, 600)
        self.main_widget = QtWidgets.QWidget(test_app)
        self.main_widget.setObjectName("main_widget")

        self.verticalLayoutWidget = QtWidgets.QWidget(self.main_widget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 480, 781, 71))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

        self.btn = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.btn.setContentsMargins(0, 0, 0, 0)
        self.btn.setObjectName("btn")

        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")

        self.btn.addWidget(self.pushButton)

        self.canvas = QtWidgets.QFrame(self.main_widget)
        self.canvas.setGeometry(QtCore.QRect(120, 30, 541, 331))
        self.canvas.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.canvas.setFrameShadow(QtWidgets.QFrame.Raised)
        self.canvas.setObjectName("canvas")

        test_app.setCentralWidget(self.main_widget)

        self.menubar = QtWidgets.QMenuBar(test_app)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        test_app.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(test_app)
        self.statusbar.setObjectName("statusbar")
        test_app.setStatusBar(self.statusbar)
        self.simulation_timer = QtCore.QTimer(
            interval=16, timeout=self.perform_simulation_iteration
        )
        self.simulation_timer.start()

        QtCore.QMetaObject.connectSlotsByName(test_app)

    def perform_simulation_iteration(self):
        print('run sim')
        #self.update()

    def paintEvent(self,event):
        print('run paint')
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtCore.Qt.red))
        n = 1
        while n<10000:
            painter.drawArc(QtCore.QRectF(20, 20, 10, 10), 10, 10)
            n+=1


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    test_app = QtWidgets.QMainWindow()
    ui = Ui_test_app(test_app)
    #ui.setupUi()
    ui2 = Ui_test_app2(test_app)
    #ui2.setupUi()
    test_app.show()
    sys.exit(app.exec_())
'''
