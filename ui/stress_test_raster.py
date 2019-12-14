from sys  import exit as sysExit

from PyQt5.QtCore    import *
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *
import sys
sys.path.append("../")
import qdarkstyle

from l1_model import L1Model
from topology import TreeVisualizer
from objects.graph import Graph

import json
from utilities import *
from objects.graph import Graph
from objects.node import Node

class Win1Disply(QFrame):
    def __init__(self, parent):
        QFrame.__init__(self)

        self.setFrameShape(QFrame.StyledPanel)
        self.setLineWidth(0.2)
        # -------
        self.Cntnr = QVBoxLayout()
        self.Cntnr.addWidget(QTextEdit('This is Window 1 with whatever contents you want'))
        self.Win1Btn = QPushButton('>>')
        self.Win1Btn.clicked.connect(parent.RightArrow)
        self.Cntnr.addWidget(self.Win1Btn)
        self.Cntnr.addStretch(1)
        # -------
        self.setLayout(self.Cntnr)

class Win2Disply(QFrame):
    def __init__(self, parent):
        QFrame.__init__(self)

        self.setFrameShape(QFrame.StyledPanel)
        self.setLineWidth(0.2)
        # -------
        self.Cntnr = QVBoxLayout()
        self.Cntnr.addWidget(QTextEdit('This is Window 2 with whatever contents you want'))
        self.Win1Btn = QPushButton('>>')
        self.Win1Btn.clicked.connect(parent.RightArrow)
        self.Cntnr.addWidget(self.Win1Btn)
        self.Cntnr.addStretch(1)
        # -------
        self.setLayout(self.Cntnr)

class OptionButtons(QToolButton):
# Class OptionButtons ("Text", Connector) inherits from QToolButton
    def __init__(self, Text, Connector):
        QToolButton.__init__(self)

        self.setText(Text)
        self.setStyleSheet("font: bold;color: blue;height: 55px;width: 55px;")
        self.setIconSize(QSize(32,32))
        self.clicked.connect(Connector)

############################## Settings Class ##############################
class OptionSettings(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        self.btnWin1 = OptionButtons('Win One', self.ShowWindow1)
        self.btnWin2 = OptionButtons('Win Two', self.ShowWindow2)
      # Vertical Box for Buttons *************************************
        self.UpLeft  = QVBoxLayout()
        self.UpLeft.addWidget(self.btnWin1)
        self.UpLeft.addWidget(self.btnWin2)
        self.UpLeft.addStretch(1)
  # Display Area on Right
      # Widget Flip Display ******************************************
        self.UpRite   = QHBoxLayout()
        self.Contents = QStackedWidget()
        self.Contents.addWidget(QTextEdit('Nothing Selected'))
        self.Contents.addWidget(Win1Disply(self))
        self.Contents.addWidget(Win2Disply(self))
        self.Contents.addWidget(QTextEdit('Settings Saved'))
        self.Contents.setCurrentIndex(0)
        self.UpRite.addWidget(self.Contents)

  # Button and Display Area on Top
        self.Upper = QHBoxLayout()
        self.Upper.addLayout(self.UpLeft)
        self.Upper.addLayout(self.UpRite)
  # Save and Cancel Area on Bottom
        self.btnSave = QPushButton("Save")
        self.btnSave.clicked.connect(self.SaveSettings)
        self.btnCncl = QPushButton("Cancel")
        self.btnCncl.clicked.connect(self.close)
        self.Lower   = QHBoxLayout()
        self.Lower.addStretch(1)
        self.Lower.addWidget(self.btnSave)
        self.Lower.addWidget(self.btnCncl)
  # Entire Options Window Layout
        self.OuterBox = QVBoxLayout()
        self.OuterBox.addLayout(self.Upper)
        self.OuterBox.addLayout(self.Lower)
        self.setLayout(self.OuterBox)
        self.setWindowTitle('Settings')
        #Geometry(Left, Top, Width, Hight)
        self.setGeometry(250, 250, 550, 450)
        self.setModal(True)
        self.exec()

    def ShowWindow1(self):
        self.Contents.setCurrentIndex(1)

    def ShowWindow2(self):
        self.Contents.setCurrentIndex(2)

    def SaveSettings(self):
        self.Contents.setCurrentIndex(3)

    def RightArrow(self):
        if self.Contents.currentIndex() == 1:
           self.Contents.setCurrentIndex(2)
        else:
           self.Contents.setCurrentIndex(1)


class CenterPanel1(QWidget):
    def __init__(self, MainWin):
        QWidget.__init__(self)

        CntrPane = QTextEdit('Center Panel is Placed Here')

        vbox = QVBoxLayout(self)
        lnetd_topology = TreeVisualizer()
        vbox.addWidget(lnetd_topology)

        self.setLayout(vbox)

class CenterPanel(QWidget):
    def __init__(self, MainWin):
        QWidget.__init__(self)

        self.graph = Graph()
        self.node_radius: float = 15
        # --- General options

        self.layout_margins: float = 8
        self.layout_item_spacing: float = 2 * self.layout_margins

        # ---Widget objects

        self.network_info_btn =  QPushButton(text="Network Info")
        self.forces_checkbox = QCheckBox(text="forces", checked=False)
        self.l1_model_btn = QPushButton(text="L1 Model")
        self.reset_all_demands_btn = QPushButton(text="Reset Demands",clicked=self.reset_all_demands)
        self.labels_checkbox = QCheckBox(text="labels", checked=True)
        self.input_line_edit = QLineEdit(enabled=self.labels_checkbox.isChecked())
        self.input_line_source = QLineEdit(
            placeholderText = "Source"
        )
        self.input_line_target = QLineEdit(
            placeholderText = "Target"
        )
        self.additive_checkbox = QCheckBox(text="Additive", checked=True)

        self.input_line_demand = QLineEdit(
            placeholderText = "Demand in Mbps"
        )
        self.demand_unit_select = QComboBox(
            sizeAdjustPolicy = QComboBox.AdjustToContents,
            )
        self.demand_unit_select.addItems(["Mbps", "Gbps", "Tbps"])

        self.input_demand_slider = QSlider(
                    orientation=Qt.Horizontal,
                    tickPosition=QSlider.TicksBelow,
                    maximum = 1000,
                    pageStep = 500, #defines how far apart the ticks are
                    singleStep = 10,
                    value = 100,
                )
        self.import_graph_button = QPushButton(text="Load Topology",clicked=self.import_graph_lnetd)
        self.import_demands_button = QPushButton(text="Load Demands",clicked=self.load_netflow_demands)
        self.export_graph_button = QPushButton(text="Export")
        self.deploy_button = QPushButton(
            text="Add Demand",
        )
        self.about_button = QPushButton(
            text="?",
            #clicked=self.show_help,
            sizePolicy=QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed),
        )
        # --Layouts

        #->add Main vertical box
        self.vbox = QVBoxLayout(self)
        #create lnetd_topology_widget
        self.lnetd_topology = TreeVisualizer(self)
        #self.lnetd_topology.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        #self.lnetd_topology.setStyleSheet("background-color:transparent;");
        self.lnetd_topology.setObjectName('StyledButton')
        self.lnetd_topology.setProperty('Test', True)

        #self.lnetd_topology.setStyleSheet("QFrame { border: 1px solid black }")
        self.lnetd_topology.graph = Graph()
        #append lnetd_topology to vertical box
        self.vbox.addWidget(self.lnetd_topology)

        #-->create options layout
        self.option_h_layout = QHBoxLayout(self, margin=self.layout_margins)
        self.option_h_layout.addWidget(self.l1_model_btn)
        self.option_h_layout.addWidget(self.network_info_btn)
        self.option_h_layout.addSpacing(self.layout_item_spacing)
        self.option_h_layout.addWidget(self.reset_all_demands_btn)
        self.option_h_layout.addSpacing(self.layout_item_spacing)
        self.option_h_layout.addWidget(self.labels_checkbox)
        self.option_h_layout.addSpacing(self.layout_item_spacing)
        self.option_h_layout.addWidget(self.forces_checkbox)
        self.option_h_layout.addSpacing(self.layout_item_spacing)
        self.option_h_layout.addWidget(self.input_line_edit)


        #-->create demand layout
        self.demand_h_layout = QHBoxLayout(self, margin=self.layout_margins)
        #self.demand_h_layout.addSpacing(self.layout_item_spacing)
        self.demand_h_layout.addWidget(self.input_line_source)
        self.demand_h_layout.addWidget(self.input_line_target)
        self.demand_h_layout.addWidget(self.additive_checkbox)
        self.demand_h_layout.addWidget(self.input_line_demand)
        self.demand_h_layout.addWidget(self.demand_unit_select)
        self.demand_h_layout.addWidget(self.input_demand_slider)

        #-->create io layout
        self.io_h_layout = QHBoxLayout(self, margin=self.layout_margins)
        self.io_h_layout.addWidget(self.import_graph_button)
        self.io_h_layout.addWidget(self.import_demands_button)
        self.io_h_layout.addSpacing(self.layout_item_spacing)
        self.io_h_layout.addWidget(self.export_graph_button)
        self.io_h_layout.addSpacing(self.layout_item_spacing)
        self.io_h_layout.addWidget(self.deploy_button)
        self.io_h_layout.addWidget(self.about_button)


        #add layout
        self.vbox.addLayout(self.option_h_layout)
        self.vbox.addLayout(self.demand_h_layout)
        self.vbox.addLayout(self.io_h_layout)
        self.setLayout(self.vbox)
        with open('style.css', 'r') as file:
            data = file.read()
            self.setStyleSheet(data)
        print(self.lnetd_topology.styleSheet())
    def reset_all_demands(self):
        print('reset')
        print(self.lnetd_topology.graph.get_nodes())

    def load_netflow_demands(self):
        path = QFileDialog.getOpenFileName()[0]
        if path != "":
            try:
                if len(self.lnetd_topology.graph.nodes) == 0:
                    raise Exception("Demands must be loaded after Network Topology")
                with open(path, "r") as file:
                    demands = json.load(file)
                    #print(demands)
                    for demand in demands:
                        source = demand['source']
                        target = demand['target']
                        demand_value = int(demand['demand'])
                        self.lnetd_topology.graph.add_demand(source=source,target=target,demand=demand_value)
                    self.lnetd_topology.graph.redeploy_demands()
                    #self.demand_report()
                    #self.graph.redeploy_demands()
            except UnicodeDecodeError:
                QMessageBox.critical(self, "Error!", "Can't read binary files!")
            except ValueError:
                QMessageBox.critical(
                        self, "Error!", "The demand file cannot be imported!"
                    )
            except Exception as e:
                print('this is the error when importing netflow', e)
                QMessageBox.critical(
                        self,
                        "Error!",
                        str(e),
                    )

    def import_graph_lnetd(self):
            """Is called when the import button is clicked; imports a graph from a file."""
            path = QFileDialog.getOpenFileName()[0]

            if path != "":
                try:
                    with open(path, "r") as file:
                        lnetd_graph = json.load(file)
                        #generate_link_number add a link_num to json
                        #TODO mode this to graph as a method , it's needed when adding new links
                        data = generate_link_number(lnetd_graph['links'])
                        host_data = lnetd_graph['nodes']

                        # set the properties of the graph
                        directed = True
                        weighted = True
                        #graph Object
                        graph = Graph(directed=directed, weighted=weighted)

                        node_dictionary = {}
                        # add each of the nodes of the vertex to the graph
                        for vertex in data:
                            vertex_components = vertex
                            nodes = [
                                vertex_components['source'],
                                vertex_components['target'],
                                ]

                            metric = int(vertex_components['metric'])
                            util = 0 #vertex_components['util']
                            l_ip = vertex_components['local_ip']
                            linknum = vertex_components['linknum']
                            capacity = vertex_components['capacity']
                            #print(vertex_components.get('remote_ip'))
                            for node in nodes:
                                import_coordinates = False
                                if node not in node_dictionary:
                                    #TODO improve this , maybe a dict instead of list ?!
                                    for node_json in host_data:
                                        #
                                        if node_json.get('name') == node:
                                            x1 = node_json.get('x')
                                            y1 = node_json.get('y')
                                            import_coordinates = True
                                            break

                                    # try to get the (x,y) and if not slightly randomize the coordinates, so the graph
                                    # doesn't stay in one place
                                    if import_coordinates:
                                        x = x1
                                        y = y1
                                    else:

                                        x = self.canvas.width() / 2 + (random() - 0.5) + randint(1,600)
                                        y = self.canvas.height() / 2 + (random() - 0.5) + randint(1,600)

                                    # add it to graph with default values
                                    node_dictionary[node] = graph.add_node(
                                        Vector(x, y), self.node_radius, node
                                    )
                            # get the node objects from the names
                            n1, n2 = node_dictionary[nodes[0]], node_dictionary[nodes[1]]
                            graph.add_vertex(
                                n1=n1,
                                n2=n2,
                                metric = metric,
                                util = util,
                                local_ip = vertex_components['local_ip'],
                                linknum= linknum,
                                capacity= capacity,
                                remote_ip = (vertex_components.get('remote_ip') if vertex_components.get('remote_ip') else 'None')
                            )
                    # if everything was successful, override the current graph
                    self.lnetd_topology.graph = graph

                except UnicodeDecodeError:
                    QMessageBox.critical(self, "Error!", "Can't read binary files!")
                except ValueError as e:
                    print(e)
                    QMessageBox.critical(
                        self, "Error!", "The weights of the graph are not numbers!"
                    )
                except Exception as e:
                    QMessageBox.critical(
                        self,
                        "Error!",
                        str(e),
                    )
class MenuToolBar(QDockWidget):
    def __init__(self, MainWin):
        QDockWidget.__init__(self)
        self.MainWin = MainWin
        self.MainMenu = MainWin.menuBar()

        self.WndowMenu  = self.MainMenu.addMenu('Windows')

        self.OptnAct = QAction('Options', self)
        self.OptnAct.setStatusTip('Open the Options Window')
        self.OptnAct.triggered.connect(MainWin.ShowOptions)

        self.WndowMenu.addAction(self.OptnAct)

        self.InitToolBar(MainWin)

    def InitToolBar(self, MainWin):
        self.mainToolBar = MainWin.addToolBar("Quick Access")

        self.mainToolBar.addAction(self.OptnAct)

class UI_LnetD(QMainWindow):
    def __init__(self):
        super(UI_LnetD, self).__init__()
        self.setWindowTitle('LnetD(qt) - Network Modelling')

      # Left, Top, Width, Height
        self.setGeometry(200, 200, 550, 550)


        self.CenterPane = CenterPanel(self)
        self.setCentralWidget(self.CenterPane)
        #self.MenuToolBar = MenuToolBar(self)


    #def ShowOptions(self):
        #self.Options = OptionSettings(self)

if __name__ == '__main__':
    MainApp = QApplication([])
    #MainApp.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    MainGui = UI_LnetD()
    MainGui.setUnifiedTitleAndToolBarOnMac(True)
    MainGui.show()

    sysExit(MainApp.exec_())
