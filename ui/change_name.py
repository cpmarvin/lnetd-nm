# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'change_name.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ChangeName(object):
    update_demands = QtCore.pyqtSignal(str)

    def change_name(self):
        #check if node name not in used
        new_label = self.lineEdit.text()
        node_labels = [ node.get_label() for node in self.graph.nodes ]
        if new_label in node_labels:
            #raise Exception
            QtWidgets.QMessageBox.critical(
                    self.horizontalLayoutWidget, "Error!", "There is a node with this name already !!!"
                )
        else:
            self.node.label = self.name_txt.text()
            self.update_demands.emit('oh well run the reports if you must')

    def setupUi(self, Form,node, graph):
        Form.setObjectName("Form")
        Form.resize(377, 199)
        self.node = node
        self.graph = graph
        self.save_btn = QtWidgets.QPushButton(Form)
        self.save_btn.setGeometry(QtCore.QRect(70, 130, 113, 32))
        self.save_btn.setObjectName("save_btn")
        self.close_btn = QtWidgets.QPushButton(Form)
        self.close_btn.setGeometry(QtCore.QRect(210, 130, 113, 32))
        self.close_btn.setObjectName("close_btn")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(70, 40, 251, 81))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.name_lbl = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.name_lbl.setObjectName("name_lbl")
        self.horizontalLayout.addWidget(self.name_lbl)
        self.name_txt = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.name_txt.setObjectName("name_txt")
        self.horizontalLayout.addWidget(self.name_txt)

        self.retranslateUi(Form)
        self.close_btn.clicked.connect(Form.close)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.save_btn.setText(_translate("Form", "Save"))
        self.close_btn.setText(_translate("Form", "Close"))
        self.name_lbl.setText(_translate("Form", "Name:"))
        self.name_txt.setText(str(self.node.label))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

