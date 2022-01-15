import random
import sys
import os
import json

from PyQt5 import QtCore, QtGui, QtWidgets

from support import (
    load_graph,
    generate_link_number,
    load_graph_web,
    generate_path_config,
)

from change_interface import Ui_changeLink
from show_path import Ui_ShowPath
from change_node_name import Ui_nameNode
from lnetd_web_settings import Ui_LnetdSettings

from graph import Graph
from node import Node
from interface import Interface
from demand import Demand
from l1node import L1Node
from circuit import Circuit

from utilities import Vector
from lnetd_scene import GraphicsScene
from lnetd_view import GraphicsView
from lnetd_link import Link
from lnetd_node import Rectangle
from lnetd_group import LnetdGroup
from adjust_demands import Ui_adjustDemands
# L1 Model
from l1_widget import Ui_L1_Widget
from lnetd_l1node import L1NodeItem
from lnetd_l1circuit import L1CircuitItem
# Group topology
from group_widget import Ui_Group_Widget

from PyQt5.QtCore import (
    Qt,
    QSize,
    QTimer,
    QPointF,
    QRectF,
    QMetaObject,
    QRect,
    QCoreApplication,
    QPoint,
    QLineF,
    pyqtSlot,
    QFileInfo
)
from PyQt5.QtGui import (
    QPainter,
    QBrush,
    QPen,
    QFont,
    QIcon,
    QTransform,
    QPalette,
    QColor,
)
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
    QSpacerItem,
    QMainWindow,
    QMenuBar,
    QOpenGLWidget,
)

import resources

import configparser

file_path = generate_path_config()

config = configparser.ConfigParser()
config.read(file_path)

blue_threshold = config.get("threshold", "blue_threshold")
green_threshold = config.get("threshold", "green_threshold")
yellow_threshold = config.get("threshold", "yellow_threshold")
orange_threshold = config.get("threshold", "orange_threshold")


class Ui_MainWindow(object):
    def deploy_static_demand(self):
        """This is infact deploy demands"""
        # TODO change name and redo
        source_label = self.source_txt.text()
        source_node = self.graph.get_node_based_on_label(source_label)
        target_label = self.target_txt.text()
        target_node = self.graph.get_node_based_on_label(target_label)
        demand_value = self.input_line_demand.text()
        demand_unit_text = self.unit_selector.currentText()
        if demand_unit_text == "Mbps":
            demand_unit_multiplicate = 1
        elif demand_unit_text == "Gbps":
            demand_unit_multiplicate = 1000
        elif demand_unit_text == "Tbps":
            demand_unit_multiplicate = 1000000

        graph_nodes = self.graph.get_nodes_label()

        can_spf_be_ran = False
        if (
            source_label in graph_nodes
            and target_label in graph_nodes
            and source_label != target_label
            and len(demand_value) > 0
        ):
            can_spf_be_ran = True

        else:
            message = f"Source or Node not found in Graph , SPF will not run"
            QtWidgets.QMessageBox.information(self.centralwidget, "Info", message)

        if can_spf_be_ran:
            if not self.additive.isChecked():
                self.graph.remove_all_demands()
            # get new spf path
            demand = float(demand_value) * demand_unit_multiplicate
            self.graph.add_demand(source_label, target_label, demand)
            self.demand_report()

    def demand_report(self):
        self.scene.update()
        self.graph.redeploy_demands()

        if self.actionWarningsON.isChecked():
            if len(self.graph.get_unrouted_demands()) > 0:
                message = (
                    "there are demands that cannot be deployed in the current model"
                )
                QMessageBox.information(self.centralwidget, "About", message)

        self.update_linktable()
        self.update_demandtable()
        self.network_info_update_values()

    def adjust_demand_trigger(self,value,flag):
        if flag == 1:
            self.graph.update_all_demands(value,active_only=True)
        else:
            self.graph.update_all_demands(value,active_only=False)
        self.demand_report()
    def update_demand_value(self, valueOfSlider):
        """Update the edit with the slider value"""
        text = str(valueOfSlider)
        self.input_line_demand.setText(text)

    def update_linktable(self):

        self.LinkTable.clear()
        self.LinkTable.setRowCount(0)
        # TODO fix this , should be dynamic
        self.LinkTable.setHorizontalHeaderLabels(
            [
                "Source",
                "Target",
                "Metric",
                "Util(Mbps)",
                "Capacity(Mbps)",
                "Local IP",
                "Remote IP",
                "DOWN",
                "ON SPF",
                "LINK NR",
                "LATENCY",
                "HIGHLIGHT",
            ]
        )

        for row_number, row_data in enumerate(self.graph.nodes, 0):
            for interface in row_data.interfaces:

                self.LinkTable.insertRow(row_number)
                self.LinkTable.setItem(
                    row_number, 0, QtWidgets.QTableWidgetItem(str(row_data.label))
                )
                for column_number, data in enumerate(interface.__dict__.values(), 1):
                    self.LinkTable.setItem(
                        row_number, column_number, QtWidgets.QTableWidgetItem(str(data))
                    )

    def update_demandtable(self):
        self.DemandTable.clear()
        # self.DemandTable.setRowCount(0)
        # TODO fix this , should be dynamic
        """
        self.DemandTable.setHorizontalHeaderLabels(
            ["Source", "Target", "Demand (Gbps)", "Fail to Deploy"]
        )
        """
        self.DemandTable.setHeaderLabels(
            # ["Source", "Target", "Demand (Gbps)", "Fail to Deploy",]
            [
                "Source",
                "Target",
                "Metric",
                "Latency",
                "Demand(Gbps)",
                "Fail",
                "Degraded",
                "Active"
            ]
        )

        for row_number, row_data in enumerate(self.graph.demands):
            # self.DemandTable.insertRow(row_number)
            items = []
            for column_number, data in enumerate(row_data.__dict__.values()):
                """
                self.DemandTable.setItem(
                    row_number,
                    column_number,
                    QtWidgets.QTableWidgetItem(str(data)),
                )
                """
                if column_number == 4:
                    data = round(data / 1000, 2)
                items.append(str(data))
            l1 = QtWidgets.QTreeWidgetItem(items)
            for path in row_data.demand_path:
                string_output = []
                string_output.append(f"{path[0]}")
                string_output.append(f"{path[1]}")
                string_output.append(f"{path[2]}")
                string_output.append(f"{path[3]}")
                l1_1 = QtWidgets.QTreeWidgetItem(string_output)
                l1.addChild(l1_1)
            self.DemandTable.addTopLevelItem(l1)

    def network_info_update_values(self):
        """This is run when tab change is 2,
        updates the network information"""
        self.lcdNumberNetworkNodes.display(len(self.graph.nodes))
        self.lcdNumberNetworkDemands.display(len(self.graph.demands))
        self.lcdNumberNetworkDemandsFail.display(len(self.graph.get_unrouted_demands()))
        self.lcdNumberNetworkLinks.display(self.graph.get_number_of_links() / 2)

    def tab_change_static_demands(self):
        """This is run when tab change is 1,
        updates the completer"""
        router_list = self.graph.get_nodes_label()
        completer = QtWidgets.QCompleter(router_list)

        self.source_txt.setCompleter(completer)
        self.target_txt.setCompleter(completer)

    def tab_change(self, event):
        # print('Tab change',event)
        if event == 0:
            """1st Tab is Static Demand"""
            self.tab_change_static_demands()
        elif event == 1:
            """3rd Tab is Model Info"""
            self.network_info_update_values()
        elif event == 2:
            self.update_linktable()
        elif event == 3:
            self.update_demandtable()

    def load_topology_json(self):
        path = QFileDialog.getOpenFileName()[0]
        if path != "":
            try:
                # with open(path, "r") as file:
                # lnetd_graph = json.load(file)
                self.graph = load_graph(path)
                node_list = self.graph.get_nodes()
                # print(node_list)
                self.scene.clear()
                for node in node_list:
                    for n in node.interfaces:
                        custom_link = Link(node, n)
                        self.scene.addItem(custom_link)
                    custome_rect = Rectangle(node)
                    self.scene.addItem(custome_rect)
                self.update_demandtable()
                self.demand_report()
                MainWindow.setWindowTitle("LnetD - Network Model" + ": " + QFileInfo(path).fileName() )
            except UnicodeDecodeError:
                QMessageBox.critical(
                    self.centralwidget, "Error!", "Can't read binary files!"
                )
            except ValueError as e:
                print(e)
                QMessageBox.critical(
                    self.centralwidget,
                    "Error!",
                    "The weights of the graph are not numbers!",
                )
            except Exception as e:
                QMessageBox.critical(
                    self.centralwidget,
                    "Error!",
                    str(e),
                )

    def load_topology_lnetd(self):
        if (
            not self.lnetd_web_url
            or not self.lnetd_web_user
            or not self.lnetd_web_password
        ):
            QMessageBox.critical(
                self.centralwidget,
                "Error!",
                "LnetD WEB url,user and password must be set before importing, WIP",
            )
        else:
            try:
                self.graph = load_graph_web(
                    self.lnetd_web_url, self.lnetd_web_user, self.lnetd_web_password
                )
                node_list = self.graph.get_nodes()
                self.scene.clear()
                for node in node_list:
                    for n in node.interfaces:
                        custom_link = Link(node, n)
                        self.scene.addItem(custom_link)
                    custome_rect = Rectangle(node)
                    self.scene.addItem(custome_rect)
                self.update_demandtable()
                self.demand_report()
            except UnicodeDecodeError:
                QMessageBox.critical(
                    self.centralwidget, "Error!", "Can't read binary files!"
                )
            except Exception as e:
                QMessageBox.critical(
                    self.centralwidget,
                    "Error!",
                    str(e),
                )

    def load_demands_json(self):
        """Load Demand from Json File
        This is called when load demands button from main app is clicked"""
        path = QFileDialog.getOpenFileName()[0]
        if path != "":
            try:
                with open(path, "r") as file:
                    # clear existing demand if additive is not checked
                    if not self.additive.isChecked():
                        self.graph.remove_all_demands()
                    demands = json.load(file)
                    for demand in demands["demands"]:
                        source_node = demand["source"]
                        target_target = demand["target"]
                        demand_value = float(demand["value"])
                        self.graph.add_demand(
                            source=source_node,
                            target=target_target,
                            demand=demand_value,
                        )
            except Exception as e:
                message = f"Demands cannot be added\n" + str(e)
                QtWidgets.QMessageBox.information(self.centralwidget, "Error", message)
        self.demand_report()

    def export_topology_json(self):
        path = QFileDialog.getSaveFileName()[0]

        if path != "":
            try:
                with open(path, "w") as file:
                    # TODO redo this
                    graph = {}
                    graph["links"] = []
                    graph["nodes"] = self.graph.export_nodes()
                    # look at every pair of nodes and examine the vertices
                    for i, n1 in enumerate(self.graph.get_nodes()):
                        # print(n1.export_links())
                        graph["links"] += n1.export_links()
                    json.dump(graph, file, sort_keys=True, indent=4)
            except Exception as e:
                QMessageBox.critical(
                    self.centralwidget,
                    "Error!",
                    "An error occurred when exporting the graph. Make sure that you "
                    "have permission to write to the specified file and try again!",
                )

    def export_demands_json(self):
        path = QFileDialog.getSaveFileName()[0]
        if path != "":
            try:
                with open(path, "w") as file:
                    # TODO redo this
                    demands_json = {}
                    demands_json["demands"] = []
                    # look at every pair of nodes and examine the vertices
                    for i, n1 in enumerate(self.graph.demands):
                        demands_json["demands"].append(
                            {
                                "source": n1.source.label,
                                "target": n1.target.label,
                                "value": n1.demand,
                            }
                        )
                    json.dump(demands_json, file, sort_keys=True, indent=4)
            except Exception as e:
                QMessageBox.critical(
                    self.centralwidget,
                    "Error!",
                    "An error occurred when exporting demands. Make sure that you "
                    "have permission to write to the specified file and try again!",
                )

    # -->handle action from emit in scene
    def sceneNodeDown(self, scene, nodeItem):
        # print('sceneNodeDown',nodeItem)
        node_down = nodeItem.node
        node_down.failNode()
        self.demand_report()
        # self.scene.update()

    def sceneNodeUp(self, scene, nodeItem):
        # print('sceneNodeUp',nodeItem)
        node_down = nodeItem.node
        node_down.unfailNode()
        self.demand_report()
        # self.scene.update()

    def sceneAddNode(self, scene, event):
        rtr_label = (
            "RTR-"
            + "" * (len(self.graph.nodes) // 26)
            + chr(65 + len(self.graph.nodes) % 26)
        )
        node = Node(Vector(event.scenePos().x(), event.scenePos().y()), 15, rtr_label)
        nodeItem = Rectangle(node)
        self.graph.nodes.append(node)
        if self.icons.isChecked():
            nodeItem.icons = True
        self.scene.addItem(nodeItem)
        self.demand_report()

    def scenedeleteNode(self, scene, nodeItem):
        # print('scenedeleteNode with',nodeItem)
        node = nodeItem.node
        # find all scene link items that have a link with this node item
        all_scene_links = [
            item for item in self.scene.items() if isinstance(item, Link)
        ]
        # all_scene_links1 = copy.copy(all_scene_links)
        for linkitem in all_scene_links:
            if linkitem.link.target == node or linkitem.source_node == node:
                # linkitem.update_position()
                # ßprint('remove Link ', linkitem)
                self.scene.removeItem(linkitem)
        self.graph.remove_node(node)
        self.scene.removeItem(nodeItem)
        self.demand_report()
        # self.scene.update()
        # remove all scene elements

    def scenechangeNodeName(self, scene, nodeItem):
        node = nodeItem.node
        self.change_node = QDialog()
        self.change_node.ui = Ui_nameNode()
        self.change_node.ui.setupUi(self.change_node, node, self.graph)
        self.change_node.show()
        self.change_node.ui.node_change.connect(self.demand_report)

    def scenechangeNodeSource(self, scene, nodeItem):
        node = nodeItem.node
        self.source_txt.setText(str(node.label))

    def scenechangeNodeTarget(self, scene, nodeItem):
        node = nodeItem.node
        self.target_txt.setText(str(node.label))

    def scenechangeNodeGroup(self, scene, nodeItem):
        #print(event.scenePos().x(), event.scenePos().y())
        group1 = LnetdGroup(nodeItem,scene)
        for n in self.scene.selectedItems():
            if isinstance(n, Rectangle):
                #n.hide()
                n.setSelected(False)
                n.setParentItem(group1)
        self.scene.addItem(group1)

    def scenechangeGroupTopology(self,scene,item):
        # Group Topology
        self.group_model = QDialog()
        self.group_model.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.group_model.ui = Ui_Group_Widget()
        self.group_model.ui.setupUi(self.group_model)
        for node_item in item.childItems():
            for n in node_item.node.interfaces:
                custom_link = Link(node_item.node, n)
                custom_link.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
                custom_link.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, False)
                custom_link.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, False)
                custom_link.show_context = False
                self.group_model.ui.scene.addItem(custom_link)
            entry = Rectangle(node_item.node)
            entry.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
            entry.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, False)
            entry.show_context = False
            if node_item.icons:
                entry.icons=True
            self.group_model.ui.scene.addItem(entry)
        self.group_model.show()


    def sceneInterfaceDown(self, scene, InterfaceItem):
        interface_down = InterfaceItem
        interface_down.link.failInterface()
        self.demand_report()

    def sceneInterfaceUp(self, scene, InterfaceItem):
        interface_up = InterfaceItem
        interface_up.link.unfailInterface()
        self.demand_report()

    def sceneInterfaceChange(self, scene, interfaceItem):
        # find the peer interface in the graph
        self.peer_interface = self.graph.get_peer_interface(interfaceItem.link)
        self.change_link = QDialog()
        self.change_link.setWindowFlags(Qt.Tool)  # tool so far
        self.change_link.ui = Ui_changeLink()
        self.change_link.ui.setupUi(
            self.change_link, interfaceItem.link, self.peer_interface
        )
        self.change_link.show()
        self.change_link.ui.interface_change.connect(self.demand_report)

    def sceneShowPath(self, scene, nodeItem):
        self.show_path_error = QDialog()
        if len(self.scene.selectedItems()) == 2:
            source_node = nodeItem.node
            target_item = [
                item for item in self.scene.selectedItems() if item != nodeItem
            ]
            target_node = target_item[
                0
            ].node  # self.graph.get_node_based_on_label('nl-p13-ams')
            # self.show_path = QDialog()
            # self.show_path.setWindowFlags(Qt.Tool)
            try:
                self.graph.ShowSpfPath(source_node, target_node, set_highlight=False)
                self.show_path = Ui_ShowPath()
                self.show_path.setupUi(
                    self.show_path, source_node, target_node, self.graph
                )
                self.show_path.show()
            except:
                QtWidgets.QMessageBox.critical(
                    self.show_path_error,
                    "Error!",
                    "No path between the nodes !",
                )
                return

    def sceneAddInterface(self, scene, nodeItem):
        if len(self.scene.selectedItems()) == 2:
            source_node = nodeItem.node
            target_item = [
                item for item in self.scene.selectedItems() if item != nodeItem
            ]
            target_node = target_item[
                0
            ].node  # self.graph.get_node_based_on_label('nl-p13-ams')
            subnet = random.sample(range(0, 210), 3)
            ip1 = "{}.{}.{}.{}".format(*subnet + [1])
            ip2 = "{}.{}.{}.{}".format(*subnet + [2])
            metric=10
            capacity=1000
            existing_link,existing_link_exists = self.graph.return_vertex_ifexist(source_node,target_node)
            if existing_link_exists:
                metric=existing_link[0].metric
                capacity=existing_link[0].capacity
            interface_source_target = Interface(
                target=target_node,
                metric=metric,
                local_ip=ip1,
                util=0,
                capacity=capacity,
                remote_ip=ip2,
                linknum=1,
            )
            interface_target_source = Interface(
                target=source_node,
                metric=metric,
                local_ip=ip2,
                util=0,
                capacity=capacity,
                remote_ip=ip1,
                linknum=1,
            )
            # append to graph
            source_node.interfaces.append(interface_source_target)
            target_node.interfaces.append(interface_target_source)
            # create qgraphic item
            new_link1 = Link(source_node, interface_source_target)
            new_link2 = Link(target_node, interface_target_source)
            # append to scene
            self.graph.update_linknum(source_node, target_node)
            self.scene.addItem(new_link1)
            self.scene.addItem(new_link2)
            self.demand_report()

    def sceneDeleteInterface(self, scene, interfaceItem):
        interface = interfaceItem.link
        source_node = self.graph.get_node_by_interface_ip(str(interface.local_ip))
        target_node = interface.target

        all_scene_links = [
            item for item in self.scene.items() if isinstance(item, Link)
        ]
        for linkitem in all_scene_links:
            if linkitem.link.remote_ip == interface.local_ip:
                self.scene.removeItem(linkitem)
        self.graph.remove_interface(interface)
        self.scene.removeItem(interfaceItem)
        self.graph.update_linknum(source_node, target_node)
        self.demand_report()

    def l1sceneCircuitDown(self, scene, InterfaceItem):
        circuit = InterfaceItem.link
        circuit.failCircuit()
        self.demand_report()

    def l1sceneCircuitUp(self, scene, InterfaceItem):
        circuit = InterfaceItem.link
        circuit.unfailCircuit()
        self.demand_report()

    def l1sceneNodeDown(self, scene, nodeItem):
        node = nodeItem.node
        node.failNode()
        all_node_circuits = self.graph.get_circuits_l1_node(node)
        for circuit in all_node_circuits:
            circuit.failCircuit()
        self.demand_report()

    def l1sceneNodeUp(self, scene, nodeItem):
        node = nodeItem.node
        node.unfailNode()
        all_node_circuits = self.graph.get_circuits_l1_node(node)
        for circuit in all_node_circuits:
            circuit.unfailCircuit()
        self.demand_report()

    def setupUi(self, MainWindow):
        self.lnetd_web_url = config.get("web", "url")
        self.lnetd_web_user = config.get("web", "user")
        self.lnetd_web_password = config.get("web", "password")

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(995, 715)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)

        self.centralwidget = QtWidgets.QWidget(MainWindow)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.centralwidget.sizePolicy().hasHeightForWidth()
        )

        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(995, 715))

        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.legend_widget = QtWidgets.QWidget(self.centralwidget)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.legend_widget.sizePolicy().hasHeightForWidth()
        )

        self.legend_widget.setSizePolicy(sizePolicy)
        self.legend_widget.setAutoFillBackground(True)
        self.legend_widget.setObjectName("legend_widget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.legend_widget)
        self.gridLayout_3.setContentsMargins(0, -1, 0, -1)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.legend_grid = QtWidgets.QGridLayout()
        self.legend_grid.setContentsMargins(10, -1, -1, -1)
        self.legend_grid.setObjectName("legend_grid")

        self.magenta_legend = QtWidgets.QPushButton(self.legend_widget)
        self.magenta_legend.setEnabled(False)
        self.magenta_legend.setAutoFillBackground(True)
        self.magenta_legend.setStyleSheet("background-color: magenta ; color: black")
        self.magenta_legend.setFlat(True)
        self.magenta_legend.setObjectName("magenta_legend")
        self.legend_grid.addWidget(self.magenta_legend, 0, 5, 1, 1)

        self.orange_legend = QtWidgets.QPushButton(self.legend_widget)
        self.orange_legend.setEnabled(False)
        self.orange_legend.setAutoFillBackground(True)
        self.orange_legend.setStyleSheet("background-color: orange ; color: black")
        self.orange_legend.setFlat(True)
        self.orange_legend.setObjectName("orange_legend")
        self.legend_grid.addWidget(self.orange_legend, 0, 4, 1, 1)

        self.blue_legend = QtWidgets.QPushButton(self.legend_widget)
        self.blue_legend.setEnabled(False)
        self.blue_legend.setAutoFillBackground(True)
        self.blue_legend.setStyleSheet("background-color: blue ; color: black")
        self.blue_legend.setFlat(True)
        self.blue_legend.setObjectName("blue_legend")
        self.legend_grid.addWidget(self.blue_legend, 0, 1, 1, 1)

        self.gray_legend = QtWidgets.QPushButton(self.legend_widget)
        self.gray_legend.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gray_legend.sizePolicy().hasHeightForWidth())
        self.gray_legend.setSizePolicy(sizePolicy)
        self.gray_legend.setAutoFillBackground(True)
        self.gray_legend.setStyleSheet("background-color : #A9A9A9 ; color : black; ")
        self.gray_legend.setFlat(False)
        self.gray_legend.setObjectName("gray_legend")
        self.legend_grid.addWidget(self.gray_legend, 0, 0, 1, 1)

        self.yellow_legend = QtWidgets.QPushButton(self.legend_widget)
        self.yellow_legend.setEnabled(False)
        self.yellow_legend.setAutoFillBackground(True)
        self.yellow_legend.setStyleSheet("background-color: yellow ; color: black")
        self.yellow_legend.setFlat(True)
        self.yellow_legend.setObjectName("orange_legend")
        self.legend_grid.addWidget(self.yellow_legend, 0, 3, 1, 1)

        self.green_legend = QtWidgets.QPushButton(self.legend_widget)
        self.green_legend.setEnabled(False)
        self.green_legend.setAutoFillBackground(True)
        self.green_legend.setStyleSheet("background-color: green ; color: black")
        self.green_legend.setFlat(True)
        self.green_legend.setObjectName("green_legend")
        self.legend_grid.addWidget(self.green_legend, 0, 2, 1, 1)

        self.gridLayout_3.addLayout(self.legend_grid, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.legend_widget)

        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(50)
        sizePolicy.setVerticalStretch(50)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())

        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.splitter.setLineWidth(4)
        self.splitter.setMidLineWidth(4)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setOpaqueResize(False)
        self.splitter.setHandleWidth(10)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")

        self.graph = Graph()
        self.scene = GraphicsScene()

        # L1 Model
        self.l1_model = QDialog()
        self.l1_model.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.l1_model.ui = Ui_L1_Widget()
        self.l1_model.ui.setupUi(self.l1_model)
        # Link slots to l1scene (This will be pain to managed)
        self.l1_model.ui.scene.circuitUp.connect(self.l1sceneCircuitUp)
        self.l1_model.ui.scene.circuitDown.connect(self.l1sceneCircuitDown)
        self.l1_model.ui.scene.l1nodeUp.connect(self.l1sceneNodeUp)
        self.l1_model.ui.scene.l1nodeDown.connect(self.l1sceneNodeDown)
        self.l1_model.ui.scene.load_l1_dummy_topology.connect(
            self.load_l1_topology_dummy
        )
        self.l1_model.ui.scene.load_l1_topology.connect(self.load_l1_topology)

        # End L1 Model

        self.graphicsView = GraphicsView(self.scene)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())

        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setFrameShape(QtWidgets.QFrame.Box)
        self.graphicsView.setFrameShadow(QtWidgets.QFrame.Plain)
        self.graphicsView.setLineWidth(1)
        self.graphicsView.setMidLineWidth(-1)
        self.graphicsView.setObjectName("graphicsView")

        self.splitter.addWidget(self.graphicsView)

        # -->TabWidget
        self.tabWidget = QtWidgets.QTabWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(0, 120))
        self.tabWidget.setMaximumSize(QtCore.QSize(16777215, 800))
        self.tabWidget.setBaseSize(QtCore.QSize(0, 0))
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.South)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setIconSize(QtCore.QSize(0, 0))
        self.tabWidget.setElideMode(QtCore.Qt.ElideRight)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setObjectName("tabWidget")

        # -->Tab1 Load Data
        self.load_data_tab = QtWidgets.QWidget()
        self.load_data_tab.setObjectName("load_data_tab")

        self.load_data_layout = QtWidgets.QWidget(self.load_data_tab)
        self.load_data_layout.setGeometry(QtCore.QRect(0, 10, 971, 32))
        self.load_data_layout.setObjectName("layoutWidget_2")

        self.show_btn_layout = QtWidgets.QGridLayout(self.load_data_layout)
        self.show_btn_layout.setContentsMargins(0, 0, 0, 0)
        self.show_btn_layout.setObjectName("show_btn_layout")

        self.show_interfaces = QtWidgets.QPushButton(self.load_data_layout)
        self.show_interfaces.setObjectName("show_interfaces")
        self.show_btn_layout.addWidget(self.show_interfaces, 0, 0, 1, 1)

        self.show_network_demands = QtWidgets.QPushButton(self.load_data_layout)
        self.show_network_demands.setObjectName("show_network_demands")
        self.show_btn_layout.addWidget(self.show_network_demands, 0, 1, 1, 1)

        self.show_network_paths = QtWidgets.QPushButton(self.load_data_layout)
        self.show_network_paths.setObjectName("show_network_paths")
        self.show_btn_layout.addWidget(self.show_network_paths, 0, 2, 1, 1)

        self.widget = QtWidgets.QWidget(self.load_data_tab)
        self.widget.setGeometry(QtCore.QRect(0, 50, 971, 32))
        self.widget.setObjectName("widget")

        self.load_btn_layout = QtWidgets.QGridLayout(self.widget)
        self.load_btn_layout.setContentsMargins(0, 0, 0, 0)
        self.load_btn_layout.setObjectName("load_btn_layout")

        self.load_topology = QtWidgets.QPushButton(
            text="Load Topology", clicked=self.load_topology_json
        )
        self.load_btn_layout.addWidget(self.load_topology, 0, 0, 1, 1)

        self.load_demands = QtWidgets.QPushButton(
            text="Load Demands", clicked=self.load_demands_json
        )  # self.widget)
        self.load_demands.setObjectName("load_demands")
        self.load_btn_layout.addWidget(self.load_demands, 0, 1, 1, 1)

        # self.load_l1_topology = QtWidgets.QPushButton(self.widget)
        # self.load_l1_topology.setObjectName("load_l1_topology")
        # self.load_btn_layout.addWidget(self.load_l1_topology, 0, 2, 1, 1)
        # No Need , moved to file menu
        # self.load_data_layout.addWidget(self.widget)
        # Add to tabWidget this tab
        # self.tabWidget.addTab(self.load_data_tab, "")

        # -->Second tab
        self.static_demands_tab = QtWidgets.QWidget()
        self.static_demands_tab.setObjectName("static_demands_tab")

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.static_demands_tab)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.static_demands_layout = QtWidgets.QHBoxLayout()
        self.static_demands_layout.setObjectName("static_demands_layout")
        self.source_lbl = QtWidgets.QLabel(self.static_demands_tab)
        self.source_lbl.setObjectName("source_lbl")
        self.source_lbl.setFixedHeight(20)
        self.static_demands_layout.addWidget(self.source_lbl)
        self.source_txt = QtWidgets.QLineEdit(self.static_demands_tab)
        self.source_txt.setObjectName("source_txt")
        self.static_demands_layout.addWidget(self.source_txt)
        self.target_lbl = QtWidgets.QLabel(self.static_demands_tab)
        self.target_lbl.setObjectName("target_lbl")
        self.target_lbl.setFixedHeight(20)
        self.static_demands_layout.addWidget(self.target_lbl)
        self.target_txt = QtWidgets.QLineEdit(self.static_demands_tab)
        self.target_txt.setObjectName("target_txt")
        self.static_demands_layout.addWidget(self.target_txt)

        self.input_line_demand = QtWidgets.QLineEdit(placeholderText="Mbps")
        self.input_line_demand.setFixedWidth(80)
        self.static_demands_layout.addWidget(self.input_line_demand)

        self.additive = QtWidgets.QCheckBox(self.static_demands_tab)
        self.additive.setObjectName("additive")
        self.additive.setChecked(1)
        self.static_demands_layout.addWidget(self.additive)

        # self.demand_warning = QtWidgets.QCheckBox(self.static_demands_tab)
        # self.demand_warning.setText("Warning ON")

        # self.static_demands_layout.addWidget(self.demand_warning)

        self.slider = QtWidgets.QSlider(
            self.static_demands_tab,
            tickPosition=QSlider.TicksBelow,
            maximum=1000,
            pageStep=500,
            singleStep=10,
            value=100,
            valueChanged=self.update_demand_value,
        )

        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setObjectName("slider")

        self.static_demands_layout.addWidget(self.slider)

        self.unit_selector = QtWidgets.QComboBox(self.static_demands_tab)
        self.unit_selector.setObjectName("unit_selector")
        self.unit_selector.addItems(["Mbps", "Gbps", "Tbps"])

        self.static_demands_layout.addWidget(self.unit_selector)
        self.horizontalLayout_2.addLayout(self.static_demands_layout)
        # self.reset_demands_btn = QtWidgets.QPushButton(self.static_demands_tab)
        # self.reset_demands_btn.setObjectName("reset_demands_btn")
        # self.horizontalLayout_2.addWidget(self.reset_demands_btn)

        self.add_demads_btn = QtWidgets.QPushButton(
            self.static_demands_tab, clicked=self.deploy_static_demand
        )
        self.add_demads_btn.setObjectName("add_demads_btn")
        self.horizontalLayout_2.addWidget(self.add_demads_btn)

        self.tabWidget.addTab(self.static_demands_tab, "")

        # 3rd tab
        self.model_inf_tab = QtWidgets.QWidget()
        self.model_inf_tab.setObjectName("model_inf_tab")

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.model_inf_tab)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.model_info_layout = QtWidgets.QGridLayout()
        self.model_info_layout.setObjectName("model_info_layout")

        self.label_4 = QtWidgets.QLabel(self.model_inf_tab)
        self.label_4.setObjectName("label_4")
        self.model_info_layout.addWidget(self.label_4, 0, 0, 1, 1)
        self.lcdNumberNetworkNodes = QtWidgets.QLCDNumber(self.model_inf_tab)
        self.lcdNumberNetworkNodes.setObjectName("lcdNumberNetworkNodes")
        self.model_info_layout.addWidget(self.lcdNumberNetworkNodes, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.model_inf_tab)
        self.label_3.setObjectName("label_3")
        self.model_info_layout.addWidget(self.label_3, 0, 2, 1, 1)

        self.lcdNumberNetworkDemands = QtWidgets.QLCDNumber(self.model_inf_tab)
        self.lcdNumberNetworkDemands.setObjectName("lcdNumberNetworkDemands")
        self.model_info_layout.addWidget(self.lcdNumberNetworkDemands, 0, 3, 1, 1)

        self.label_5 = QtWidgets.QLabel(self.model_inf_tab)
        self.label_5.setObjectName("label_5")
        self.model_info_layout.addWidget(self.label_5, 1, 0, 1, 1)

        self.lcdNumberNetworkLinks = QtWidgets.QLCDNumber(self.model_inf_tab)
        self.lcdNumberNetworkLinks.setObjectName("lcdNumberNetworkLinks")
        self.model_info_layout.addWidget(self.lcdNumberNetworkLinks, 1, 1, 1, 1)

        self.label_6 = QtWidgets.QLabel(self.model_inf_tab)
        self.label_6.setObjectName("label_6")
        self.model_info_layout.addWidget(self.label_6, 1, 2, 1, 1)

        self.lcdNumberNetworkDemandsFail = QtWidgets.QLCDNumber(self.model_inf_tab)
        self.lcdNumberNetworkDemandsFail.setObjectName("lcdNumberNetworkDemandsFail")
        self.model_info_layout.addWidget(self.lcdNumberNetworkDemandsFail, 1, 3, 1, 1)

        self.horizontalLayout_3.addLayout(self.model_info_layout)
        self.tabWidget.addTab(self.model_inf_tab, "")

        # self.tab_3 = QtWidgets.QWidget()
        # self.tab_3.setObjectName("tab_3")
        # self.tabWidget.addTab(self.tab_3, "")

        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")

        # add layout to tab_5
        self.link_table_layout = QtWidgets.QGridLayout(self.tab_5)
        self.link_table_layout.setContentsMargins(2, 2, 2, 2)
        self.link_table_layout.setObjectName("model_info_layout")
        # create table
        self.LinkTable = QtWidgets.QTableWidget()
        self.LinkTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.LinkTable.customContextMenuRequested.connect(self.LinkTableMenu)
        # self.LinkTable.setGeometry(QtCore.QRect(-5, 1, 951, 201))
        self.LinkTable.setObjectName("LinkTable")
        self.LinkTable.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents
        )
        self.LinkTable.setGridStyle(QtCore.Qt.DashDotLine)
        self.LinkTable.setWordWrap(False)
        self.LinkTable.setRowCount(0)
        self.LinkTable.setColumnCount(12)
        self.LinkTable.setObjectName("LinkTable")
        self.LinkTable.setSortingEnabled(False)
        self.LinkTable.horizontalHeader().setVisible(True)
        self.LinkTable.horizontalHeader().setCascadingSectionResizes(True)
        self.LinkTable.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        self.LinkTable.verticalHeader().setVisible(False)
        # add widget table to layout
        self.link_table_layout.addWidget(self.LinkTable)

        self.tabWidget.addTab(self.tab_5, "")

        self.demand_tab = QtWidgets.QWidget()
        self.demand_tab.setObjectName("demand_tab")

        # add layout to tab_5
        self.demand_tab_layout = QtWidgets.QGridLayout(self.demand_tab)
        self.demand_tab_layout.setContentsMargins(2, 2, 2, 2)
        self.demand_tab_layout.setObjectName("model_info_layout")
        # add demandTable
        self.DemandTable = QtWidgets.QTreeWidget() #demandTable() # QtWidgets.QTreeWidget()
        self.DemandTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.DemandTable.customContextMenuRequested.connect(self.DemandTableMenu)
        self.DemandTable.setObjectName("DemandTable")
        self.DemandTable.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents
        )
        self.DemandTable.setWordWrap(False)
        self.DemandTable.setObjectName("DemandTable")
        self.DemandTable.expandAll()
        # add demandTable to layout
        self.demand_tab_layout.addWidget(self.DemandTable)
        self.tabWidget.addTab(self.demand_tab, "")

        self.verticalLayout.addWidget(self.splitter)

        self.tabWidget.currentChanged.connect(self.tab_change)

        MainWindow.setCentralWidget(self.centralwidget)

        # -->Menu
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 995, 22))
        self.menuBar.setObjectName("menuBar")
        self.menuBar.setNativeMenuBar(False)

        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuFile.setTitle("File")

        self.menuSettings = QtWidgets.QMenu(self.menuBar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuSettings.setTitle("Settings")

        self.menuView = QtWidgets.QMenu(self.menuBar)
        self.menuView.setObjectName("view")
        self.menuView.setTitle("View")

        self.menuAbout = QtWidgets.QMenu(self.menuBar)
        self.menuAbout.setObjectName("About")
        self.menuAbout.setTitle("About")

        MainWindow.setMenuBar(self.menuBar)
        self.actionLoadTopology = QtWidgets.QAction(MainWindow)
        self.actionLoadTopology.setObjectName("actionLoadTopology")
        self.actionLoadTopology.setText("Load Topology JSON")
        self.actionLoadTopology.triggered.connect(self.load_topology_json)

        self.actionLoadDemands = QtWidgets.QAction(MainWindow)
        self.actionLoadDemands.setObjectName("actionLoadDemands")
        self.actionLoadDemands.setText("Load Demands JSON")
        self.actionLoadDemands.triggered.connect(self.load_demands_json)

        self.actionLoadTopologyLnetD = QtWidgets.QAction(MainWindow)
        self.actionLoadTopologyLnetD.setObjectName("actionLoadTopology")
        self.actionLoadTopologyLnetD.setText("Import Topology WEB")
        self.actionLoadTopologyLnetD.triggered.connect(self.load_topology_lnetd)

        self.actionExportTopology = QtWidgets.QAction(MainWindow)
        self.actionExportTopology.setObjectName("actionLoadDemands")
        self.actionExportTopology.setText("Export Topology JSON")
        self.actionExportTopology.triggered.connect(self.export_topology_json)

        self.actionExportDemands = QtWidgets.QAction(MainWindow)
        self.actionExportDemands.setObjectName("actionExportDemands")
        self.actionExportDemands.setText("Export Demands JSON")
        self.actionExportDemands.triggered.connect(self.export_demands_json)

        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionQuit.setText("Quit")
        self.actionQuit.triggered.connect(app.quit)

        self.actionWarningsON = QtWidgets.QAction(MainWindow, checkable=True)
        self.actionWarningsON.setObjectName("actionWarningsON")
        self.actionWarningsON.setText("Warnings ON")
        self.actionWarningsON.setChecked(True)

        self.actionTheme = QtWidgets.QAction(MainWindow, checkable=True)
        self.actionTheme.setObjectName("actionTheme")
        self.actionTheme.setText("Dark Theme")
        self.actionTheme.setChecked(False)
        self.actionTheme.triggered.connect(self.apply_theme)

        self.icons = QtWidgets.QAction(MainWindow, checkable=True)
        self.icons.setObjectName("icons")
        self.icons.setText("Node Icons")
        self.icons.setChecked(False)
        self.icons.triggered.connect(self.apply_icons)

        self.lnetd_web = QtWidgets.QAction(MainWindow, checkable=False)
        self.lnetd_web.setObjectName("icons")
        self.lnetd_web.setText("LnetD Web Settings")
        self.lnetd_web.triggered.connect(self.set_lnetd_web)

        self.show_latency = QtWidgets.QAction(MainWindow, checkable=True)
        self.show_latency.setObjectName("show_latency")
        self.show_latency.setText("Show link latency")
        self.show_latency.setChecked(False)
        self.show_latency.triggered.connect(self.apply_latency)

        self.adjust_demands = QtWidgets.QAction(MainWindow, checkable=False)
        self.adjust_demands.setObjectName("adjust_demands")
        self.adjust_demands.setText("Adjust Demands")
        self.adjust_demands.triggered.connect(self.adjust_demands_ui)

        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionLoadTopology)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionLoadDemands)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionLoadTopologyLnetD)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExportTopology)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExportDemands)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuFile.addSeparator()

        self.menuSettings.addSeparator()
        self.menuSettings.addAction(self.actionWarningsON)

        self.menuSettings.addSeparator()
        self.menuSettings.addAction(self.icons)

        self.menuSettings.addSeparator()
        self.menuSettings.addAction(self.actionTheme)
        self.menuSettings.addSeparator()
        self.menuSettings.addAction(self.lnetd_web)
        self.menuSettings.addSeparator()
        self.menuSettings.addAction(self.show_latency)
        self.menuSettings.addSeparator()
        self.menuSettings.addAction(self.adjust_demands)

        self.l1topology = QtWidgets.QAction(MainWindow)
        self.l1topology.setObjectName("l1topology")
        self.l1topology.setText("View L1 Topology")
        self.l1topology.triggered.connect(self.l1_model_show)  # fixme

        self.menuView.addSeparator()
        self.menuView.addAction(self.l1topology)

        self.aboutInfo = QtWidgets.QAction(MainWindow)
        self.aboutInfo.setObjectName("About")
        self.aboutInfo.setText("Info")
        self.aboutInfo.triggered.connect(self.about_show)  # fixme

        self.menuAbout.addSeparator()
        self.menuAbout.addAction(self.aboutInfo)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuSettings.menuAction())
        self.menuBar.addAction(self.menuView.menuAction())
        self.menuBar.addAction(self.menuAbout.menuAction())

        # --> Slots
        self.scene.nodeDown.connect(self.sceneNodeDown)
        self.scene.nodeUp.connect(self.sceneNodeUp)
        self.scene.addNode.connect(self.sceneAddNode)
        self.scene.nodeDelete.connect(self.scenedeleteNode)
        self.scene.changeNodeName.connect(self.scenechangeNodeName)
        self.scene.nodeSource.connect(self.scenechangeNodeSource)
        self.scene.nodeTarget.connect(self.scenechangeNodeTarget)
        self.scene.nodeGroup.connect(self.scenechangeNodeGroup)
        self.scene.groupTopology.connect(self.scenechangeGroupTopology)

        self.scene.interfaceDown.connect(self.sceneInterfaceDown)
        self.scene.interfaceUp.connect(self.sceneInterfaceUp)
        self.scene.interfaceChange.connect(self.sceneInterfaceChange)
        self.scene.interfaceAdd.connect(self.sceneAddInterface)
        self.scene.interfaceDelete.connect(self.sceneDeleteInterface)
        self.scene.showPath.connect(self.sceneShowPath)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def LinkTableMenu(self,point):
        '''Custome Context menu for Link Table
        used to modify interface attribute'''
        index = self.LinkTable.indexAt(point)
        if not index.isValid():
            return
        item = self.LinkTable.itemAt(point)
        menu = QtWidgets.QMenu()
        if item is not None:
            editAction = menu.addAction('Edit Interface')
            action = menu.exec_(self.LinkTable.mapToGlobal(point))
            if action == editAction:
                self.LinkTableEditAction(item)

    def LinkTableEditAction(self,item):
        row = item.row()
        local_ip = self.LinkTable.item(row,5).data(0)
        all_linksItems = [ n for n in self.scene.items() if isinstance(n, Link)] # this is costly need a better way
        interfaceItem = [ n for n in all_linksItems if n.link.local_ip == local_ip ][0]
        peer_interface = self.graph.get_peer_interface(interfaceItem.link)
        self.table_change_link = QDialog()
        self.table_change_link.setWindowFlags(Qt.Tool)  # tool so far
        self.table_change_link.ui = Ui_changeLink()
        self.table_change_link.ui.setupUi(
            self.table_change_link, interfaceItem.link, peer_interface
        )
        self.table_change_link.show()
        self.table_change_link.ui.interface_change.connect(self.demand_report)

    def DemandTableMenu(self,point):
        '''Custom Context menu for Demand table
        used to delete and modify demands'''
        index = self.DemandTable.indexAt(point)
        if not index.isValid():
            return
        item = self.DemandTable.itemAt(point)
        menu = QtWidgets.QMenu()
        if item is not None and item.childCount() != 0:
            removeAction = menu.addAction('Remove')
            #TODO editAction = menu.addAction('Edit')
            if item.data(7,0)=='True': #active
                deactivateAction = menu.addAction('Deactivate')
            else:
                activateAction = menu.addAction('Activate')
            action = menu.exec_(self.DemandTable.mapToGlobal(point))
            if action == removeAction:
                self.DemandTableRemoveAction(item)
            elif item.data(7,0)=='False':
                if action == activateAction:
                    self.DemandTableActivateAction(item)
            elif item.data(7,0)=='True':
                if action == deactivateAction:
                    self.DemandTableDeactivateAction(item)

    def DemandTableRemoveAction(self,item):
        node_source = item.data(0,0)
        node_target = item.data(1,0)
        self.graph.edit_demand(node_source,node_target,0,delete=True)
        self.demand_report()

    def DemandTableDeactivateAction(self,item):
        node_source = item.data(0,0)
        node_target = item.data(1,0)
        self.graph.enableDemand(node_source,node_target,enable=False)
        self.demand_report()

    def DemandTableActivateAction(self,item):
        node_source = item.data(0,0)
        node_target = item.data(1,0)
        self.graph.enableDemand(node_source,node_target,enable=True)
        self.demand_report()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "LnetD - Network Model"))
        self.gray_legend.setText(_translate("MainWindow", "0%"))
        self.blue_legend.setText(_translate("MainWindow", blue_threshold + "%"))
        self.green_legend.setText(_translate("MainWindow", green_threshold + "%"))
        self.yellow_legend.setText(_translate("MainWindow", yellow_threshold + "%"))
        self.orange_legend.setText(_translate("MainWindow", orange_threshold + "%"))
        self.magenta_legend.setText(
            _translate("MainWindow", ">" + orange_threshold + "%")
        )

        self.show_interfaces.setText(
            _translate("MainWindow", "Show Network Interfaces")
        )
        self.show_network_demands.setText(
            _translate("MainWindow", "Show Network Demands")
        )
        self.show_network_paths.setText(_translate("MainWindow", "Show Network Paths"))

        self.load_demands.setText(_translate("MainWindow", "Load Demands"))
        # self.load_l1_topology.setText(_translate("MainWindow", "Load L1 Topology"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.load_data_tab),
            _translate("MainWindow", "Load Data"),
        )
        self.source_lbl.setText(_translate("MainWindow", "Source"))
        self.target_lbl.setText(_translate("MainWindow", "Target"))
        self.additive.setText(_translate("MainWindow", "Additive"))
        # self.reset_demands_btn.setText(_translate("MainWindow", "Reset Demand"))
        self.add_demads_btn.setText(_translate("MainWindow", "Add Demand"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.static_demands_tab),
            _translate("MainWindow", "Static Demands"),
        )
        self.label_4.setText(_translate("MainWindow", "Network Nodes"))
        self.label_3.setText(_translate("MainWindow", "Network Demands"))
        self.label_5.setText(_translate("MainWindow", "Network Links"))
        self.label_6.setText(_translate("MainWindow", "Network Failed Demands"))

        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.model_inf_tab),
            _translate("MainWindow", "Model Information"),
        )
        # self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Reports"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_5),
            _translate("MainWindow", "Network Links"),
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.demand_tab),
            _translate("MainWindow", "Network Demands"),
        )

    def apply_theme(self, state):

        if state:
            css_name = ":/theme/dark/style_dark.css"
        else:
            css_name = ":/theme/light/style_light.css"

        stream = QtCore.QFile(css_name)
        stream.open(QtCore.QIODevice.ReadOnly)
        app.setStyleSheet(QtCore.QTextStream(stream).readAll())
        stream.close()

    def adjust_demands_ui(self,state):
        self.adjust_demands_ui = QDialog()
        self.adjust_demands_ui.setWindowFlags(Qt.Tool)  # tool so far
        self.adjust_demands_ui.ui = Ui_adjustDemands()
        self.adjust_demands_ui.ui.setupUi(self.adjust_demands_ui)
        self.adjust_demands_ui.show()
        self.adjust_demands_ui.ui.demand_change.connect(self.adjust_demand_trigger)


    def apply_icons(self, state):

        all_scene_links = [
            item for item in self.scene.items() if isinstance(item, Rectangle)
        ]

        if state:
            for item in all_scene_links:
                item.icons = True
        else:
            for item in all_scene_links:
                item.icons = False

    def apply_latency(self, state):
        all_scene_links = [
            item for item in self.scene.items() if isinstance(item, Link)
        ]

        if state:
            for item in all_scene_links:
                item.show_latency = True
        else:
            for item in all_scene_links:
                item.show_latency = False

    def l1_model_show(self):
        self.l1_model.show()

    def about_show(self):
        message = (
                    "Quick how-to at: https://github.com/cpmarvin/lnetd_qt/blob/master/examples/LnetD-QT.pdf <a href='https://github.com/cpmarvin/lnetd_qt/blob/master/examples/LnetD-QT.pdf'>Here</a> "
                )
        QMessageBox.information(self.centralwidget, "About", message)

    def load_l1_topology(self):
        path = QFileDialog.getOpenFileName()[0]
        if path != "":
            try:
                with open(path, "r") as file:
                    self.graph.l1nodes = []
                    self.l1_model.ui.scene.clear()
                    # path = 'examples/l1_topology/lnetd_l1_topology.json'
                    # with open(path, "r") as file:
                    lnetd_graph = json.load(file)
                    data = generate_link_number(lnetd_graph["l1_links"])
                    host_data = lnetd_graph["l1_nodes"]
                    node_dictionary = {}
                    for circuit in data:
                        nodes = [
                            circuit["source"],
                            circuit["target"],
                        ]
                        interface_map = circuit["interfaces"]
                        link_num = circuit["linknum"]
                        label = circuit["label"]
                        for node in nodes:
                            import_coordinates = False
                            if node not in node_dictionary:
                                # TODO improve this , maybe a dict instead of list ?!
                                for node_json in host_data:
                                    #
                                    if node_json.get("name") == node:
                                        x1 = node_json.get("x")
                                        y1 = node_json.get("y")
                                        import_coordinates = True
                                        break
                                if import_coordinates:
                                    x = x1
                                    y = y1
                                else:
                                    x = random.randint(1, 5600)
                                    y = random.randint(1, 5600)

                                node_dictionary[node] = L1Node(Vector(x, y), 15, node)
                                self.graph.l1nodes.append(node_dictionary[node])

                        n1, n2 = node_dictionary[nodes[0]], node_dictionary[nodes[1]]
                        circuit_obj = Circuit(label=label, target=n2, link_num=link_num)
                        all_graph_interface = self.graph.get_all_interfaces_map()
                        for interface in interface_map:
                            if all_graph_interface.get(interface):
                                circuit_obj.interfaces.append(
                                    all_graph_interface.get(interface)
                                )

                        n1.circuits.append(circuit_obj)

                    for node in self.graph.l1nodes:
                        for n in node.circuits:
                            custom_link = L1CircuitItem(node, n)
                            self.l1_model.ui.scene.addItem(custom_link)
                        custome_rect = L1NodeItem(node)
                        self.l1_model.ui.scene.addItem(custome_rect)
                    self.update_demandtable()
                    self.demand_report()
            except Exception as e:
                message = f"L1 Topology Not Loaded \n" + str(e)
                QtWidgets.QMessageBox.information(self.centralwidget, "Error", message)

    def load_l1_topology_dummy(self):
        self.graph.l1nodes = []
        self.l1_model.ui.scene.clear()
        all_intefaces = self.graph.get_all_interface()

        uk_a = L1Node(Vector(40, 60), radius=15, label="DWDM-UK-A")
        nl_a = L1Node(Vector(180, 60), radius=15, label="DWDM-NL-A")
        fr_a = L1Node(Vector(160, 180), radius=15, label="DWDM-FR-A")
        ke_a = L1Node(Vector(40, 180), radius=15, label="DWDM-KE-A")

        uk_a_nl_a_1 = Circuit(label="SEGMENT-1", target=nl_a, link_num=1)
        uk_a_nl_a_2 = Circuit(label="SEGMENT-2", target=nl_a, link_num=2)
        nl_a_fr_a = Circuit(label="SEGMENT-1", target=fr_a, link_num=1)
        fr_a_ke_a = Circuit(label="SEGMENT-2", target=ke_a, link_num=1)

        try:
            uk_a_nl_a_1.interfaces.append(random.choice(all_intefaces))
            uk_a_nl_a_2.interfaces.append(random.choice(all_intefaces))
            nl_a_fr_a.interfaces.append(random.choice(all_intefaces))
            fr_a_ke_a.interfaces.append(random.choice(all_intefaces))
        except:
            pass

        uk_a.circuits.append(uk_a_nl_a_1)
        uk_a.circuits.append(uk_a_nl_a_2)
        nl_a.circuits.append(nl_a_fr_a)
        fr_a.circuits.append(fr_a_ke_a)

        self.graph.l1nodes.append(uk_a)
        self.graph.l1nodes.append(nl_a)
        self.graph.l1nodes.append(fr_a)
        self.graph.l1nodes.append(ke_a)

        for node in self.graph.l1nodes:
            for n in node.circuits:
                custom_link = L1CircuitItem(node, n)
                self.l1_model.ui.scene.addItem(custom_link)
            custome_rect = L1NodeItem(node)
            self.l1_model.ui.scene.addItem(custome_rect)
        self.update_demandtable()
        self.demand_report()

    def set_lnetd_web(self):
        self.lnetd_web = QDialog()
        self.lnetd_web.ui = Ui_LnetdSettings()
        self.lnetd_web.ui.setupUi(
            self.lnetd_web,
            self.lnetd_web_url,
            self.lnetd_web_password,
            self.lnetd_web_user,
        )
        self.lnetd_web.show()
        self.lnetd_web.ui.settings_change.connect(self.update_web_settings)

    def update_web_settings(self, url, password, username):
        self.lnetd_web_user = username
        self.lnetd_web_password = password
        self.lnetd_web_url = url


if __name__ == "__main__":

    css_name = ":/theme/light/style_light.css"

    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QtWidgets.QApplication(sys.argv)

    fontDB = QtGui.QFontDatabase()
    fontDB.addApplicationFont(":/fonts/Roboto-Regular.ttf")
    app.setFont(QFont("Roboto"))

    stream = QtCore.QFile(css_name)
    stream.open(QtCore.QIODevice.ReadOnly)
    app.setStyleSheet(QtCore.QTextStream(stream).readAll())
    stream.close()

    # allFonts = QtGui.QFontDatabase().families()
    # print(allFonts)

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
