from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ShowPath(object):
    def setupUi(self, ShowPath, target_node, source_node, graph):
        ShowPath.setObjectName("ShowPath")
        # ShowPath.resize(465, 243)
        self.showPath = QtWidgets.QTreeWidget(ShowPath)
        self.showPath.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents
        )
        self.showPath.setWordWrap(False)
        self.showPath.expandAll()

        self.showPath.setGeometry(QtCore.QRect(30, 20, 450, 200))
        self.showPath.setObjectName("showPath")
        n1, n2, n3 = graph.ShowSpfPath(source_node, target_node)
        items = [f"{source_node.label}", f"{target_node.label}", f"{n1}", f"{n2}"]
        l1 = QtWidgets.QTreeWidgetItem(items)
        for path in n3:
            string_output = []
            string_output.append(f"{path[0]}")
            string_output.append(f"{path[1]}")
            string_output.append(f"{path[2]}")
            string_output.append(f"{path[3]}")
            l1_1 = QtWidgets.QTreeWidgetItem(string_output)
            l1.addChild(l1_1)
        self.showPath.addTopLevelItem(l1)

        self.retranslateUi(ShowPath)
        QtCore.QMetaObject.connectSlotsByName(ShowPath)

    def retranslateUi(self, ShowPath):
        _translate = QtCore.QCoreApplication.translate
        ShowPath.setWindowTitle(_translate("ShowPath", "ShowPath"))
        self.showPath.headerItem().setText(0, _translate("ShowPath", "source"))
        self.showPath.headerItem().setText(1, _translate("ShowPath", "target"))
        self.showPath.headerItem().setText(2, _translate("ShowPath", "metric"))
        self.showPath.headerItem().setText(3, _translate("ShowPath", "latency"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ShowPath = QtWidgets.QShowPath()
    ui = Ui_ShowPath()
    ui.setupUi(ShowPath)
    ShowPath.show()
    sys.exit(app.exec_())