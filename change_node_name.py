from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_nameNode(QtWidgets.QDialog):
    node_change = QtCore.pyqtSignal(str)

    def change(self):
        new_label = str(self.node_name_txt.text())
        if new_label in self.graph.get_nodes_label() and self.node.label != new_label:
            QtWidgets.QMessageBox.critical(
                self.changeNodeLabel,
                "Error!",
                "A node with same label existis in the model.",
            )
        else:
            self.node.label = new_label
            self.node_change.emit("update me")
            self.changeNodeLabel.accept()

    def setupUi(self, changeNodeLabel, node, graph):
        self.node = node
        self.graph = graph
        self.changeNodeLabel = changeNodeLabel
        self.changeNodeLabel.setObjectName("changeNodeLabel")
        self.changeNodeLabel.resize(250, 150)

        self.gridLayout_2 = QtWidgets.QGridLayout(self.changeNodeLabel)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.gridLayout = QtWidgets.QGridLayout(self.changeNodeLabel)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.node_name_lbl = QtWidgets.QLabel(self.changeNodeLabel)
        self.node_name_lbl.setObjectName("node_name_lbl")
        self.gridLayout.addWidget(self.node_name_lbl, 0, 0, 1, 1)

        self.node_name_txt = QtWidgets.QLineEdit(self.changeNodeLabel)
        self.node_name_txt.setObjectName("node_name_txt")
        self.gridLayout.addWidget(self.node_name_txt, 0, 1, 1, 1)

        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.save_btn = QtWidgets.QPushButton(changeNodeLabel)
        self.save_btn.setGeometry(QtCore.QRect(150, 150, 101, 32))
        self.save_btn.setObjectName("save_btn")

        self.gridLayout_2.addWidget(self.save_btn, 1, 0, 1, 1)

        self.retranslateUi(changeNodeLabel)
        self.save_btn.clicked.connect(self.change)
        QtCore.QMetaObject.connectSlotsByName(self.changeNodeLabel)

    def retranslateUi(self, changeNodeLabel):
        _translate = QtCore.QCoreApplication.translate
        changeNodeLabel.setWindowTitle(_translate("changeNodeLabel", "Node Edit"))
        self.save_btn.setText(_translate("changeNodeLabel", "Save"))
        self.node_name_lbl.setText(_translate("changeNodeLabel", "Node Label"))
        self.node_name_txt.setText(str(self.node.label))
        self.node_name_txt.selectAll()
