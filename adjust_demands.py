from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_adjustDemands(QtWidgets.QDialog):
    demand_change = QtCore.pyqtSignal(int,int)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        return super().closeEvent(a0)

    def change(self):
        '''flag is 0 for unchecked 1 for checked'''
        metric = None
        flag = 0
        try:
            metric = int(self.metric_txt.text())
        except ValueError as e:
            QtWidgets.QMessageBox.critical(
                self.adjustDemandsMetric,
                "Error!",
                "The demand increase % MUST be a integer!",
            )
            return
        if self.update_peer_link.isChecked():
            flag = 1
        self.demand_change.emit(metric,flag)
        self.adjustDemandsMetric.accept()

    def setupUi(self, adjustDemandsMetric):

        self.adjustDemandsMetric = adjustDemandsMetric
        self.adjustDemandsMetric.setObjectName("changeLinkMetric")
        self.adjustDemandsMetric.resize(291, 196)

        self.gridLayout_2 = QtWidgets.QGridLayout(self.adjustDemandsMetric)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")

        self.metric_txt = QtWidgets.QLineEdit(self.adjustDemandsMetric)
        self.metric_txt.setObjectName("metric_txt")
        self.gridLayout.addWidget(self.metric_txt, 3, 1, 1, 1)

        self.metric_lbl = QtWidgets.QLabel(self.adjustDemandsMetric)
        self.metric_lbl.setObjectName("metric_lbl")
        self.gridLayout.addWidget(self.metric_lbl, 3, 0, 1, 1)

        self.update_peer_link = QtWidgets.QCheckBox(self.adjustDemandsMetric)
        self.update_peer_link.setObjectName("update_active_demands")
        self.update_peer_link.setChecked(0)
        self.gridLayout.addWidget(self.update_peer_link)

        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.save_btn = QtWidgets.QPushButton(self.adjustDemandsMetric)
        self.save_btn.setObjectName("save_btn")

        self.gridLayout_2.addWidget(self.save_btn, 1, 0, 1, 1)

        self.retranslateUi(adjustDemandsMetric)
        self.save_btn.clicked.connect(self.change)
        QtCore.QMetaObject.connectSlotsByName(self.adjustDemandsMetric)

    def retranslateUi(self, adjustDemandsMetric):
        _translate = QtCore.QCoreApplication.translate
        adjustDemandsMetric.setWindowTitle(
            _translate("adjustDemandsMetric", "Adjust all demands")
        )
        self.save_btn.setText(_translate("adjustDemandsMetric", "Save"))
        self.metric_lbl.setText(_translate("adjustDemandsMetric", "Value %: "))
        self.update_peer_link.setText(
            _translate("adjustDemandsMetric", "Apply to active only")
        )

'''
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    adjustDemandsMetric = QtWidgets.QDialog()
    ui = Ui_adjustDemandsMetric()
    ui.setupUi(adjustDemandsMetric)
    adjustDemandsMetric.show()
    sys.exit(app.exec_())
'''
