from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_changeLink(QtWidgets.QDialog):
    interface_change = QtCore.pyqtSignal(str)

    def change(self):
        metric = None
        capacity = None
        try:
            metric = int(self.metric_txt.text())
            capacity = float(self.capacity_txt.text()) * 1000
        except ValueError:
            QtWidgets.QMessageBox.critical(
                self.changeLinkMetric,
                "Error!",
                "The metric and capacity MUST be an integer !",
            )
        if metric is not None or capacity is not None:
            self.interface.change_metric(metric)
            self.interface.capacity = capacity
            # if peer update is checked
            if self.update_peer_link.isChecked():
                self.peer_interface.change_metric(metric)
                self.peer_interface.capacity = capacity
            self.interface_change.emit("update me")
            self.changeLinkMetric.accept()

    def setupUi(self, changeLinkMetric, interface, peer_interface=None):
        self.interface = interface
        self.peer_interface = peer_interface
        self.changeLinkMetric = changeLinkMetric
        self.changeLinkMetric.setObjectName("changeLinkMetric")
        self.changeLinkMetric.resize(291, 196)

        self.gridLayout_2 = QtWidgets.QGridLayout(self.changeLinkMetric)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.metric_txt = QtWidgets.QLineEdit(self.changeLinkMetric)
        self.metric_txt.setObjectName("metric_txt")
        self.gridLayout.addWidget(self.metric_txt, 3, 1, 1, 1)
        self.remote_ip_lbl = QtWidgets.QLabel(self.changeLinkMetric)
        self.remote_ip_lbl.setObjectName("remote_ip_lbl")
        self.gridLayout.addWidget(self.remote_ip_lbl, 1, 0, 1, 1)
        self.remote_ip_txt = QtWidgets.QLineEdit(self.changeLinkMetric)
        self.remote_ip_txt.setReadOnly(True)
        self.remote_ip_txt.setObjectName("remote_ip_txt")
        self.gridLayout.addWidget(self.remote_ip_txt, 1, 1, 1, 1)
        self.capacity_lbl = QtWidgets.QLabel(self.changeLinkMetric)
        self.capacity_lbl.setObjectName("capacity_lbl")
        self.gridLayout.addWidget(self.capacity_lbl, 2, 0, 1, 1)
        self.local_ip_txt = QtWidgets.QLineEdit(self.changeLinkMetric)
        self.local_ip_txt.setReadOnly(True)
        self.local_ip_txt.setObjectName("local_ip_txt")
        self.gridLayout.addWidget(self.local_ip_txt, 0, 1, 1, 1)
        self.metric_lbl = QtWidgets.QLabel(self.changeLinkMetric)
        self.metric_lbl.setObjectName("metric_lbl")
        self.gridLayout.addWidget(self.metric_lbl, 3, 0, 1, 1)
        self.capacity_txt = QtWidgets.QLineEdit(self.changeLinkMetric)
        self.capacity_txt.setObjectName("capacity_txt")
        self.gridLayout.addWidget(self.capacity_txt, 2, 1, 1, 1)
        self.local_ip_lbl = QtWidgets.QLabel(self.changeLinkMetric)
        self.local_ip_lbl.setObjectName("local_ip_lbl")
        self.gridLayout.addWidget(self.local_ip_lbl, 0, 0, 1, 1)

        self.update_peer_link = QtWidgets.QCheckBox(self.changeLinkMetric)
        self.update_peer_link.setObjectName("update_peer_link")
        self.update_peer_link.setChecked(1)
        self.gridLayout.addWidget(self.update_peer_link)

        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.save_btn = QtWidgets.QPushButton(self.changeLinkMetric)
        self.save_btn.setObjectName("save_btn")

        self.gridLayout_2.addWidget(self.save_btn, 1, 0, 1, 1)

        self.retranslateUi(changeLinkMetric)
        self.save_btn.clicked.connect(self.change)
        QtCore.QMetaObject.connectSlotsByName(self.changeLinkMetric)

    def retranslateUi(self, changeLinkMetric):
        _translate = QtCore.QCoreApplication.translate
        changeLinkMetric.setWindowTitle(
            _translate("changeLinkMetric", "Interface Edit")
        )
        self.save_btn.setText(_translate("changeLinkMetric", "Save"))
        self.local_ip_lbl.setText(_translate("changeLinkMetric", "Local IP:"))
        self.local_ip_txt.setText(str(self.interface.local_ip))
        self.remote_ip_lbl.setText(_translate("changeLinkMetric", "Remote IP:"))
        self.remote_ip_txt.setText(str(self.interface.remote_ip))
        self.capacity_lbl.setText(_translate("changeLinkMetric", "Capacity(Gbps):"))
        self.capacity_txt.setText(str(self.interface.capacity / 1000))
        self.metric_lbl.setText(_translate("changeLinkMetric", "Metric: "))
        self.metric_txt.setText(str(self.interface.metric))
        self.update_peer_link.setText(
            _translate("changeLinkMetric", "update peer link")
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    changeLinkMetric = QtWidgets.QDialog()
    ui = Ui_changeLinkMetric()
    ui.setupUi(changeLinkMetric)
    changeLinkMetric.show()
    sys.exit(app.exec_())
