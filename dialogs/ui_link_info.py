# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../ui/link_info.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_link_info(object):
    def setupUi(self, link_info, vertex):
        link_info.setObjectName("link_info")
        link_info.setWindowModality(QtCore.Qt.WindowModal)
        link_info.resize(351, 300)
        link_info.setFocusPolicy(QtCore.Qt.ClickFocus)
        link_info.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        link_info.setWindowTitle("")
        self.verticalLayoutWidget = QtWidgets.QWidget(link_info)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 30, 151, 211))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.label_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.label_layout.setContentsMargins(0, 0, 0, 0)
        self.label_layout.setObjectName("label_layout")
        self.local_ip_lbl = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.local_ip_lbl.setObjectName("local_ip_lbl")
        self.label_layout.addWidget(self.local_ip_lbl)
        #self.souce_lbl = QtWidgets.QLabel(self.verticalLayoutWidget)
        #self.souce_lbl.setObjectName("souce_lbl")
        #self.label_layout.addWidget(self.souce_lbl)
        self.metric_lbl = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.metric_lbl.setObjectName("metric_lbl")
        self.label_layout.addWidget(self.metric_lbl)
        self.target_lbl = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.target_lbl.setObjectName("target_lbl")
        self.label_layout.addWidget(self.target_lbl)
        self.remote_ip = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.remote_ip.setObjectName("remote_ip")
        self.label_layout.addWidget(self.remote_ip)
        self.capacity_lbl = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.capacity_lbl.setObjectName("capacity_lbl")
        self.label_layout.addWidget(self.capacity_lbl)
        self.util_lb = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.util_lb.setObjectName("util_lb")
        self.label_layout.addWidget(self.util_lb)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(link_info)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(180, 30, 161, 211))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.text_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.text_layout.setContentsMargins(0, 0, 0, 0)
        self.text_layout.setObjectName("text_layout")
        self.local_ip_txt = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.local_ip_txt.setObjectName("local_ip_txt")
        self.text_layout.addWidget(self.local_ip_txt)
        #self.source_txt = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        #self.source_txt.setObjectName("source_txt")
        #self.text_layout.addWidget(self.source_txt)
        self.metric_txt = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.metric_txt.setObjectName("metric_txt")
        self.text_layout.addWidget(self.metric_txt)
        self.target_txt = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.target_txt.setObjectName("target_txt")
        self.text_layout.addWidget(self.target_txt)
        self.remote_ip_txt = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.remote_ip_txt.setObjectName("remote_ip_txt")
        self.text_layout.addWidget(self.remote_ip_txt)
        self.capacity_txt = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.capacity_txt.setObjectName("capacity_txt")
        self.text_layout.addWidget(self.capacity_txt)
        self.util_txt = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.util_txt.setObjectName("util_txt")
        self.text_layout.addWidget(self.util_txt)

        self.retranslateUi(link_info,vertex)
        QtCore.QMetaObject.connectSlotsByName(link_info)

    def retranslateUi(self, link_info, vertex):
        _translate = QtCore.QCoreApplication.translate
        self.local_ip_lbl.setText(_translate("link_info", "Local IP"))
        #self.souce_lbl.setText(_translate("link_info", "Local Node"))
        self.metric_lbl.setText(_translate("link_info", "Metric"))
        self.target_lbl.setText(_translate("link_info", "Remote Node"))
        self.remote_ip.setText(_translate("link_info", "Remote_IP"))
        self.capacity_lbl.setText(_translate("link_info", "Capacity"))
        self.util_lb.setText(_translate("link_info", "Util"))
        self.local_ip_txt.setText(_translate("link_info", str(vertex.local_ip)))
        #self.source_txt.setText(_translate("link_info", str(vertex.source)))
        self.metric_txt.setText(_translate("link_info", str(vertex.metric)))
        self.target_txt.setText(_translate("link_info", str(vertex.target)))
        self.remote_ip_txt.setText(_translate("link_info", str(vertex.remote_ip)))
        self.capacity_txt.setText(_translate("link_info", str(vertex.capacity)))
        self.util_txt.setText(_translate("link_info", str(vertex.util)))

'''
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    link_info = QtWidgets.QWidget()
    ui = Ui_link_info()
    ui.setupUi(link_info)
    link_info.show()
    sys.exit(app.exec_())
'''
