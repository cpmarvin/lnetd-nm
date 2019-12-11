# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/test_title_fix.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from edit_label import * 

class Ui_MainWindow(object):
    def show_form(self):
        self.EditLabel = QtWidgets.QWidget()
        self.EditLabel.setWindowTitle('Form Title')
        self.EditLabel.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setWindowTitle("MainWindow")
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setToolTip("")
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(80, 210, 113, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.pushButton_2.clicked.connect(self.show_form)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.pushButton_2.setText(_translate("MainWindow", "show"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

