# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/network_info.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NetworkInfoForm(object):

    def number_of_nodes(self):
        return len(self.graph.nodes)

    def number_of_links(self):
        return self.graph.get_number_of_links()

    def number_of_demands(self):
        return len(self.graph.demands)

    def load_demands(self):
        self.DemandTable.setRowCount(0)
        #TODO fix this , should be dynamic
        self.DemandTable.setHorizontalHeaderLabels(['Source', 'Target', 'Demand (Mbps)',])

        for row_number , row_data in enumerate(self.graph.demands):
            self.DemandTable.insertRow(row_number)
            for column_number, data in enumerate(row_data.__dict__.values()):
                self.DemandTable.setItem(row_number,column_number,QtWidgets.QTableWidgetItem(str(data)))

    def load_links(self):
        self.LinkTable.setRowCount(0)
        #TODO fix this , should be dynamic
        self.LinkTable.setHorizontalHeaderLabels(['Target', 'Metric', 'Util', 'Capacity', 'Local IP', 'Remote IP', 'DOWN', 'ON SPF', 'LINK NR'])
        for row_number , row_data in enumerate(self.graph.get_all_interface()):
            self.LinkTable.insertRow(row_number)
            for column_number, data in enumerate( row_data.__dict__.values() ):
                self.LinkTable.setItem(row_number,column_number,QtWidgets.QTableWidgetItem(str(data)))

    def setupUi(self, NetworkInfoForm,graph):
        self.graph = graph
        NetworkInfoForm.setObjectName("NetworkInfoForm")
        NetworkInfoForm.resize(509, 391)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NetworkInfoForm.sizePolicy().hasHeightForWidth())
        NetworkInfoForm.setSizePolicy(sizePolicy)
        NetworkInfoForm.setMinimumSize(QtCore.QSize(509, 391))
        NetworkInfoForm.setMaximumSize(QtCore.QSize(509, 391))
        self.NetworkInforTab = QtWidgets.QTabWidget(NetworkInfoForm)
        self.NetworkInforTab.setGeometry(QtCore.QRect(10, 120, 491, 261))
        self.NetworkInforTab.setTabPosition(QtWidgets.QTabWidget.South)
        self.NetworkInforTab.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.NetworkInforTab.setElideMode(QtCore.Qt.ElideRight)
        self.NetworkInforTab.setObjectName("NetworkInforTab")
        self.DemandTab = QtWidgets.QWidget()
        self.DemandTab.setObjectName("DemandTab")
        self.DemandTable = QtWidgets.QTableWidget(self.DemandTab)
        self.DemandTable.setGeometry(QtCore.QRect(10, 30, 481, 181))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DemandTable.sizePolicy().hasHeightForWidth())
        self.DemandTable.setSizePolicy(sizePolicy)
        self.DemandTable.setMaximumSize(QtCore.QSize(481, 16777215))
        self.DemandTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.DemandTable.setGridStyle(QtCore.Qt.DashDotLine)
        self.DemandTable.setWordWrap(False)
        self.DemandTable.setRowCount(3)
        self.DemandTable.setColumnCount(3)
        self.DemandTable.setObjectName("DemandTable")
        self.DemandTable.horizontalHeader().setVisible(True)
        self.DemandTable.horizontalHeader().setCascadingSectionResizes(True)
        self.DemandTable.horizontalHeader().setMinimumSectionSize(480/1.1/3)
        self.DemandTable.verticalHeader().setVisible(False)
        self.DemandTable_lbl = QtWidgets.QLabel(self.DemandTab)
        self.DemandTable_lbl.setGeometry(QtCore.QRect(10, 10, 131, 16))
        self.DemandTable_lbl.setObjectName("DemandTable_lbl")
        self.NetworkInforTab.addTab(self.DemandTab, "")
        self.LinkTab = QtWidgets.QWidget()
        self.LinkTab.setObjectName("LinkTab")
        self.LinkTable_lbl = QtWidgets.QLabel(self.LinkTab)
        self.LinkTable_lbl.setGeometry(QtCore.QRect(10, 10, 131, 16))
        self.LinkTable_lbl.setObjectName("LinkTable_lbl")
        self.LinkTable = QtWidgets.QTableWidget(self.LinkTab)
        self.LinkTable.setGeometry(QtCore.QRect(10, 30, 481, 181))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LinkTable.sizePolicy().hasHeightForWidth())
        self.LinkTable.setSizePolicy(sizePolicy)
        self.LinkTable.setMaximumSize(QtCore.QSize(481, 16777215))
        self.LinkTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.LinkTable.setGridStyle(QtCore.Qt.DashDotLine)
        self.LinkTable.setWordWrap(False)
        self.LinkTable.setRowCount(3)
        self.LinkTable.setColumnCount(9)
        self.LinkTable.setObjectName("LinkTable")
        self.LinkTable.horizontalHeader().setVisible(True)
        self.LinkTable.horizontalHeader().setCascadingSectionResizes(True)
        self.LinkTable.horizontalHeader().setMinimumSectionSize(20)
        self.LinkTable.verticalHeader().setVisible(False)
        self.NetworkInforTab.addTab(self.LinkTab, "")
        self.verticalLayoutWidget = QtWidgets.QWidget(NetworkInfoForm)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 141, 80))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.NetworkInfoLayout_lbl = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.NetworkInfoLayout_lbl.setContentsMargins(0, 0, 0, 0)
        self.NetworkInfoLayout_lbl.setObjectName("NetworkInfoLayout_lbl")
        self.NumberOfLinks_lbl = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.NumberOfLinks_lbl.setObjectName("NumberOfLinks_lbl")
        self.NetworkInfoLayout_lbl.addWidget(self.NumberOfLinks_lbl)
        self.NumberOfNodes_lbl = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.NumberOfNodes_lbl.setObjectName("NumberOfNodes_lbl")
        self.NetworkInfoLayout_lbl.addWidget(self.NumberOfNodes_lbl)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(NetworkInfoForm)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(160, 20, 71, 82))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.NetworkInfoLayout_txt = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.NetworkInfoLayout_txt.setContentsMargins(0, 0, 0, 0)
        self.NetworkInfoLayout_txt.setObjectName("NetworkInfoLayout_txt")
        self.NumberOfLinks_txt = QtWidgets.QLCDNumber(self.verticalLayoutWidget_2)
        self.NumberOfLinks_txt.setObjectName("NumberOfLinks_txt")
        self.NetworkInfoLayout_txt.addWidget(self.NumberOfLinks_txt)
        self.NumberOfNodes_txt = QtWidgets.QLCDNumber(self.verticalLayoutWidget_2)
        self.NumberOfNodes_txt.setObjectName("NumberOfNodes_txt")
        self.NetworkInfoLayout_txt.addWidget(self.NumberOfNodes_txt)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(NetworkInfoForm)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(260, 20, 160, 80))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.NetworkDemandsLayout_lbl = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.NetworkDemandsLayout_lbl.setContentsMargins(0, 0, 0, 0)
        self.NetworkDemandsLayout_lbl.setObjectName("NetworkDemandsLayout_lbl")
        self.NumberOfDemands_lbl = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.NumberOfDemands_lbl.setObjectName("NumberOfDemands_lbl")
        self.NetworkDemandsLayout_lbl.addWidget(self.NumberOfDemands_lbl)
        self.NumberOfLSPs_lbl = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.NumberOfLSPs_lbl.setObjectName("NumberOfLSPs_lbl")
        self.NetworkDemandsLayout_lbl.addWidget(self.NumberOfLSPs_lbl)
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(NetworkInfoForm)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(430, 20, 71, 82))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.NetworkDemandsLayout_txt = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.NetworkDemandsLayout_txt.setContentsMargins(0, 0, 0, 0)
        self.NetworkDemandsLayout_txt.setObjectName("NetworkDemandsLayout_txt")
        self.NumberOfDemands_txt = QtWidgets.QLCDNumber(self.verticalLayoutWidget_4)
        self.NumberOfDemands_txt.setObjectName("NumberOfDemands_txt")
        self.NetworkDemandsLayout_txt.addWidget(self.NumberOfDemands_txt)
        self.NumberOfLSPs_txt = QtWidgets.QLCDNumber(self.verticalLayoutWidget_4)
        self.NumberOfLSPs_txt.setObjectName("NumberOfLSPs_txt")
        self.NetworkDemandsLayout_txt.addWidget(self.NumberOfLSPs_txt)

        self.retranslateUi(NetworkInfoForm)
        self.NetworkInforTab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(NetworkInfoForm)

    def retranslateUi(self, NetworkInfoForm):
        _translate = QtCore.QCoreApplication.translate
        NetworkInfoForm.setWindowTitle(_translate("NetworkInfoForm", "Form"))
        self.DemandTable.setSortingEnabled(True)
        self.DemandTable_lbl.setText(_translate("NetworkInfoForm", "Demands Table"))
        self.NetworkInforTab.setTabText(self.NetworkInforTab.indexOf(self.DemandTab), _translate("NetworkInfoForm", "Demands"))
        self.LinkTable_lbl.setText(_translate("NetworkInfoForm", "Links Table"))
        self.LinkTable.setSortingEnabled(True)
        self.NetworkInforTab.setTabText(self.NetworkInforTab.indexOf(self.LinkTab), _translate("NetworkInfoForm", "Links"))
        self.NumberOfLinks_lbl.setText(_translate("NetworkInfoForm", "Number Of Links"))
        self.NumberOfNodes_lbl.setText(_translate("NetworkInfoForm", "Number Of Nodes"))
        self.NumberOfDemands_lbl.setText(_translate("NetworkInfoForm", "Number Of Demands"))
        self.NumberOfLSPs_lbl.setText(_translate("NetworkInfoForm", "Number Of LSPs"))
        #populate values
        self.NumberOfNodes_txt.display(self.number_of_nodes())
        self.NumberOfLinks_txt.display(self.number_of_links())
        self.NumberOfDemands_txt.display(self.number_of_demands())
        self.load_demands()
        self.load_links()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    NetworkInfoForm = QtWidgets.QWidget()
    ui = Ui_NetworkInfoForm()
    ui.setupUi(NetworkInfoForm)
    NetworkInfoForm.show()
    sys.exit(app.exec_())

