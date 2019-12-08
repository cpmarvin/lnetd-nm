import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt

from PyQt5.QtCore import Qt, QSize, QTimer, QPointF, QRectF, QMetaObject, QRect , QCoreApplication, QPoint, QLineF
from PyQt5.QtGui import QPainter, QBrush, QPen, QFont, QIcon, QTransform
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
    QSpacerItem
)

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.text = "Лев Николаевич Толстой\nАнна Каренина"

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Drawing text')
        self.show()


    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHints(qp.Antialiasing)

        contents = self.contentsRect()
        # draw a line from the top left to the bottom right of the widget
        line2 = QLineF(contents.topLeft(), contents.bottomRight())
        line = QLineF(contents.bottomLeft(), contents.topRight())
        qp.drawLine(line)
        qp.drawLine(line2)

        # save the current state of the painter
        qp.save()
        # translate to the center of the painting rectangle
        qp.translate(contents.center())
        # apply an inverted rotation, since the line angle is counterclockwise
        qp.rotate(-line.angle())

        # create a rectangle that is centered at the origin point
        rect = QRect(-40, -10, 80, 20)
        qp.setPen(Qt.white)
        qp.setBrush(Qt.black)
        qp.drawRect(rect)
        qp.drawText(rect, Qt.AlignCenter, '{:.05f}'.format(line.angle()))
        qp.restore()
        # save the current state of the painter
        qp.save()
        # translate to the center of the painting rectangle
        qp.translate(contents.center())
        # apply an inverted rotation, since the line angle is counterclockwise
        qp.rotate(-line2.angle())

        # create a rectangle that is centered at the origin point
        rect = QRect(-40, -10, 80, 20)
        qp.setPen(Qt.white)
        qp.setBrush(Qt.black)
        qp.drawRect(rect)
        qp.drawText(rect, Qt.AlignCenter, '{:.05f}'.format(line2.angle()))
        qp.restore()


    def drawText(self, event, qp):

        qp.setPen(QColor(168, 34, 3))
        qp.setFont(QFont('Decorative', 10))
        qp.drawText(event.rect(), Qt.AlignCenter, self.text)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
