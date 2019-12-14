# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/edit_label.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_EditLabel(QtCore.QObject):

    update_demands = QtCore.pyqtSignal(str)

    def change_metric(self):
        metric = None
        try:
            metric = int(self.lineEdit.text())
            #print(metric)
        except ValueError:
            QtWidgets.QMessageBox.critical(
                    self.horizontalLayoutWidget, "Error!", "The metric is not a number!"
                )
        if metric is not None:
            self.vertex.change_metric(metric)
            self.update_demands.emit('oh well run the reports if you must')

    def setupUi(self, EditLabel,vertex, graph):
        self.vertex = vertex
        self.graph = graph
        EditLabel.setObjectName("EditLabel")
        EditLabel.resize(281, 138)
        self.horizontalLayoutWidget = QtWidgets.QWidget(EditLabel)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(60, 40, 161, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.LabelLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.LabelLayout.setContentsMargins(0, 0, 0, 0)
        self.LabelLayout.setObjectName("LabelLayout")
        self.Label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.Label.setObjectName("Label")
        self.LabelLayout.addWidget(self.Label)
        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.LabelLayout.addWidget(self.lineEdit)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.LabelLayout.addItem(spacerItem)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(EditLabel)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(60, 71, 161, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Save_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.Save_btn.setObjectName("Save_btn")

        self.Save_btn.clicked.connect(self.change_metric)

        self.horizontalLayout_2.addWidget(self.Save_btn)
        '''
        self.Cancel_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.Cancel_btn.setObjectName("Cancel_btn")
        self.horizontalLayout_2.addWidget(self.Cancel_btn)
        '''

        self.retranslateUi(EditLabel)
        QtCore.QMetaObject.connectSlotsByName(EditLabel)

    def retranslateUi(self, EditLabel):
        _translate = QtCore.QCoreApplication.translate
        EditLabel.setWindowTitle(_translate("EditLabel", "Link Edit"))
        self.Label.setText(_translate("EditLabel", "Metric: "))
        self.Save_btn.setText(_translate("EditLabel", "Save"))
        '''
        self.Cancel_btn.setText(_translate("EditLabel", "Cancel"))
        '''
        self.lineEdit.setText(str(self.vertex.metric))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    EditLabel = QtWidgets.QWidget()
    ui = Ui_EditLabel()
    ui.setupUi(EditLabel)
    EditLabel.show()
    sys.exit(app.exec_())

