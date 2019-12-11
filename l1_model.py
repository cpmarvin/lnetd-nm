import sys
sys.path.append("../")

#Vector
from utilities import *

#Network graph
from objects.graph import Graph
from objects.l1node import L1Node
from objects.circuit import Circuit

from typing import Tuple

# math
from math import sqrt, cos, sin, radians, pi
from random import random, randint

# PyQt5
from PyQt5.QtCore import Qt, QSize, QTimer, QPointF, QRectF, QMetaObject, QRect , QCoreApplication, QPoint, QLineF
from PyQt5.QtGui import QPainter, QBrush, QPen, QFont, QIcon, QTransform, QPalette, QColor
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
    QSpacerItem
)

class L1Model(QWidget):

    def deselect_vertex(self):
        """Sets the selected vertex to None and disables the input line edit."""
        self.selected_vertex = None
        #self.input_line_edit.setEnabled(False)

    def select_node(self, node: L1Node):
        """Sets the selected node to the specified node, sets the input line edit to
        its label and enables it."""
        self.selected_node = node


    def deselect_node(self):
        """Sets the selected node to None and disables the input line edit."""
        self.selected_node = None


    def select_vertex(self, vertex):
        """Sets the selected vertex to the specified vertex, sets the input line edit to
        its weight and enables it."""
        self.selected_vertex = vertex

    def mousePressEvent(self, event):
        """Is called when a mouse button is pressed; creates and moves
        nodes/vertices."""
        pos = self.get_mouse_position(event)

        # if we are not on canvas, don't do anything
        if pos is None:
            return

        # sets the focus to the window (for the keypresses to register)
        self.setFocus()

        # (potentially) find a node that has been pressed
        pressed_node = None
        for node in self.graph.l1nodes:
            if distance(pos, node.get_position()) <= node.get_radius():
                pressed_node = node

        # (potentially) find a vertex that has been pressed
        pressed_vertex = None
        #print('this is the vertex_positions',self.vertex_positions)

        for vertex in self.vertex_positions:
            if (
                # TODO: finish the selecting of vertices
                #abs(vertex[0][0] - pos[0]) < self.weight_rectangle_size
                #and abs(vertex[0][1] - pos[1]) < self.weight_rectangle_size
                abs(vertex[0][0] - pos[0]) < 1
                and abs(vertex[0][1] - pos[1]) < 1
            ):

                #pressed_vertex = vertex[1]
                pressed_vertex = vertex

        if event.button() == Qt.LeftButton:
            # nodes have the priority in selection before vertices
            if pressed_node is not None:
                self.deselect_vertex()
                self.select_node(pressed_node)

                self.mouse_drag_offset = pos - self.selected_node.get_position()
                self.mouse_position = pos

            elif pressed_vertex is not None:
                self.deselect_node()
                self.select_vertex(pressed_vertex)

            else:
                self.deselect_node()
                self.deselect_vertex()

        elif event.button() == Qt.RightButton:
            if pressed_node is not None:
                self.node_click(pressed_node,event)
            pass

    def adjust_canvas_translation(self, event):
        """Is called when the canvas widget is resized; changes translation so the
        center stays in the center."""
        size = Vector(event.size().width(), event.size().height())

        if self.canvas_size is not None:
            self.translation += self.scale * (size - self.canvas_size) / 2

        self.canvas_size = size

    def show_help(self):
        """Is called when the help button is clicked; displays basic information about
        the application."""
        message = """
        """

        QMessageBox.information(self, "About", message)

    def mouseReleaseEvent(self, event):
        """Is called when a mouse button is released; stops node drag."""
        self.mouse_drag_offset = None

    def mouseMoveEvent(self, event):
        """Is called when the mouse is moved across the window; updates mouse
        coordinates."""
        self.mouse_position = self.get_mouse_position(event, scale_down=True)

    def wheelEvent(self, event):
        """Is called when the mouse wheel is moved; node rotation and zoom."""
        # positive/negative for scrolling away from/towards the user
        scroll_distance = radians(event.angleDelta().y() / 8)

        if QApplication.keyboardModifiers() == Qt.ShiftModifier:
            if self.selected_node is not None:
                self.rotate_nodes_around(
                    self.selected_node.get_position(),
                    scroll_distance * self.node_rotation_coefficient,
                )
        else:
            mouse_coordinates = self.get_mouse_position(event)
            # only do something, if we're working on canvas
            if mouse_coordinates is None:
                return

            prev_scale = self.scale
            self.scale *= 2 ** (scroll_distance)

            # adjust translation so the x and y of the mouse stay in the same spot
            self.translation -= mouse_coordinates * (self.scale - prev_scale)

    def rotate_nodes_around(self, point: Vector, angle: float):
        """Rotates coordinates of all of the nodes in the same component as the selected
        node by a certain angle (in radians) around it."""
        for node in self.graph.get_nodes():
            if self.graph.share_component(node, self.selected_node):
                node.set_position((node.position - point).rotated(angle) + point)

    def get_mouse_position(self, event, scale_down=False) -> Vector:
        """Returns mouse coordinates if they are within the canvas and None if they are
        not. If scale_down is True, the function will scale down the coordinates to be
        within the canvas (useful for dragging) and return them instead."""
        x = event.pos().x()
        y = event.pos().y()

        x_on_canvas = 0 <= x <= self.canvas.width()
        y_on_canvas = 0 <= y <= self.canvas.height()

        # scale down the coordinates if scale_down is True, or return None if we are
        # not on canvas
        if scale_down:
            x = x if x_on_canvas else 0 if x <= 0 else self.canvas.width()
            y = y if y_on_canvas else 0 if y <= 0 else self.canvas.height()
        elif not x_on_canvas or not y_on_canvas:
            return None

        # return the mouse coordinates, accounting for canvas translation and scale
        return (Vector(x, y) - self.translation) / self.scale

    def perform_simulation_iteration(self):
        """Performs one iteration of the simulation."""
        # drag the selected node
        if self.selected_node is not None and self.mouse_drag_offset is not None:
            prev_node_position = self.selected_node.get_position()

            self.selected_node.set_position(
                self.mouse_position - self.mouse_drag_offset
            )

            # move the rest of the nodes that are connected to the selected node if
            # shift is pressed
            if QApplication.keyboardModifiers() == Qt.ShiftModifier:
                pos_delta = self.selected_node.get_position() - prev_node_position

                for node in self.graph.l1nodes:
                    if node is not self.selected_node:
                        #MOVE ALL , don't care
                        #and self.graph.share_component(
                        #node, self.selected_node

                        node.set_position(node.get_position() + pos_delta)

        self.update()


    def load_dummy(self):
        all_intefaces = self.graph.get_all_interface()
        print(all_intefaces)

        uk_a = L1Node(Vector(-220,60),radius=15,label='DWDM-UK-A')
        nl_a = L1Node(Vector(-30,60),radius=15,label='DWDM-NL-A')
        fr_a = L1Node(Vector(-10,180),radius=15,label='DWDM-FR-A')
        ke_a = L1Node(Vector(-180,180),radius=15,label='DWDM-KE-A')


        uk_a_nl_a_1 = Circuit(label='SEGMENT-1',target=nl_a,link_num=1)
        uk_a_nl_a_1.interfaces.append(all_intefaces[0])
        uk_a_nl_a_1.interfaces.append(all_intefaces[1])


        uk_a_nl_a_2 = Circuit(label='SEGMENT-2',target=nl_a,link_num=2)
        #uk_a_nl_a_2.interfaces.append(self.graph.get_node_by_interface_ip('10.11.13.11'))

        nl_a_fr_a = Circuit(label='SEGMENT-1',target=fr_a,link_num=1)
        #nl_a_fr_a.interfaces.append(self.graph.get_node_by_interface_ip('10.111.13.11'))
        #nl_a_fr_a.interfaces.append(self.graph.get_node_by_interface_ip('10.11.13.11'))

        fr_a_ke_a = Circuit(label='SEGMENT-2',target=ke_a,link_num=1)
        #fr_a_ke_a.interfaces.append(self.graph.get_node_by_interface_ip('10.6.7.7'))


        uk_a.circuits.append(uk_a_nl_a_1)
        uk_a.circuits.append(uk_a_nl_a_2)
        nl_a.circuits.append(nl_a_fr_a)
        fr_a.circuits.append(fr_a_ke_a)

        self.graph.l1nodes.append(uk_a)
        self.graph.l1nodes.append(nl_a)
        self.graph.l1nodes.append(fr_a)
        self.graph.l1nodes.append(ke_a)

    def node_click(self,pressed_node,event):
        cmenu = QMenu(self)
        if pressed_node._failed:
            unfail_node = cmenu.addAction("Node UP")
        else:
            fail_node = cmenu.addAction("Node DOWN")
        action = cmenu.exec_(self.mapToGlobal(event.pos()))
        if not pressed_node._failed and action == fail_node:
            print('l1node - action fail_node',pressed_node)
            pressed_node.failNode()
            all_node_circuits = self.graph.get_circuits_l1_node(pressed_node)
            for circuit in all_node_circuits:
                circuit.failCircuit()
            self.graph.redeploy_demands()
        elif pressed_node._failed and action == unfail_node:
            print('l1node - action unfail_node',pressed_node)
            pressed_node.unfailNode()
            all_node_circuits = self.graph.get_circuits_l1_node(pressed_node)
            for circuit in all_node_circuits:
                circuit.unfailCircuit()
            self.graph.redeploy_demands()

    def __init__(self,graph):
        """Initial configuration."""
        super().__init__()
        #graph is common
        self.graph = graph
        self.load_dummy()
        self.selected_node: Node = None

        self.vertex_positions: List[Tuple[Vector, Tuple[Node, Node]]] = []
        self.selected_vertex: Tuple[Node, Node] = None

        # offset of the mouse from the position of the currently dragged node
        self.mouse_drag_offset: Vector = None

        # position of the mouse; is updated when the mouse moves
        self.mouse_position: Vector = Vector(-1, -1)

        # variables for visualizing the graph
        self.node_radius: float = 20

        self.weight_rectangle_size: float = 2

        self.arrowhead_size: float = 2
        self.arrow_separation: float = pi / 7

        self.selected_color = Qt.gray
        self.regular_node_color = Qt.white
        self.regular_vertex_weight_color = Qt.black

        # limit the displayed length of labels for each node
        self.node_label_limit: int = 10

        # UI variables
        self.font_family: str = "Times New Roman"
        self.font_size: int = 18

        self.layout_margins: float = 8
        self.layout_item_spacing: float = 2 * self.layout_margins

        # canvas positioning (scale and translation)
        self.scale: float = 1
        self.scale_coefficient: float = 2  # by how much the scale changes on scroll
        self.translation: float = Vector(0, 0)

        # by how much the rotation of the nodes changes
        self.node_rotation_coefficient: float = 0.7

        # TIMERS
        # timer that runs the simulation (60 times a second... once every ~= 16ms)
        self.simulation_timer = QTimer(
            interval=16, timeout=self.perform_simulation_iteration
        )

        # WIDGETS
        self.canvas = QFrame(self, minimumSize=QSize(400, 400))
        self.canvas_size: Vector = None
        self.canvas.resizeEvent = self.adjust_canvas_translation

        #Layouts
        ##Main Layout with Canvas
        self.main_v_layout = QVBoxLayout(self, margin=0 )
        self.main_v_layout.addWidget(self.canvas)

        self.option_h_layout = QHBoxLayout(self, margin=self.layout_margins)
        self.main_v_layout.addLayout(self.option_h_layout)


        #set Qwidget Layout
        self.setLayout(self.main_v_layout)
        self.setWindowTitle("LnetD - L1 Model")
        self.setFont(QFont(self.font_family, self.font_size))
        self.show()
        # start the simulation
        self.simulation_timer.start()


    def draw_vertex(self, n1: L1Node, n2: L1Node, label: str , link_num: float, painter, circuit):
        """Draw the specified vertex."""

        n1_p = Vector(*n1.get_position())
        n2_p = Vector(*n2.get_position())
        uv = (n2_p - n1_p).unit()

        start = n1_p + uv * n1.get_radius()
        end = n2_p - uv * n2.get_radius()

        #if multiple links ( always )
        if link_num % 2 ==0:
            targetDistance = link_num * 3
        else:
            targetDistance = (-link_num +1 ) * 3

        start = start.rotated_new(self.arrow_separation * targetDistance, n1_p)
        end = end.rotated_new(-self.arrow_separation * targetDistance, n2_p)

        if circuit._failed:
            link_color = Qt.red
        else:
            link_color = Qt.green

        painter.setPen(QPen(link_color, Qt.SolidLine))
        painter.drawLine(QPointF(*start), QPointF(*end))

        if self.graph :
            # set color according to whether the vertex is selected or not
            painter.setPen(QPen(Qt.black, Qt.SolidLine))
            painter.setBrush(
                QBrush(
                    Qt.black,
                    Qt.SolidPattern,
                )
            )

            #rect calculation
            r = self.weight_rectangle_size

            mid = (start + end) / 2

            w_len = len(str(label)) * 4

            weight_v = Vector(r if w_len <= r else w_len, r)

            weight_rectangle = QRectF(*(mid - weight_v), *(2 * weight_v))

            painter.save()

            if end.unit()[0] - start.unit()[0] > 0:
                link_paint = QLineF(QPointF(*start), QPointF(*end))
            else:
                link_paint = QLineF(QPointF(*end), QPointF(*start))

            center_of_rec_x = weight_rectangle.center().x()
            center_of_rec_y  = weight_rectangle.center().y()

            painter.translate(center_of_rec_x, center_of_rec_y)

            rx = -(weight_v[0] * 0.5)
            ry = -(weight_v[1] )

            painter.rotate(- link_paint.angle());
            new_rec = QRect(rx , ry, weight_v[0], 2 * weight_v[1])
            painter.drawRect(QRect(rx , ry, weight_v[0] , 2 * weight_v[1] ))
            painter.setFont(QFont(self.font_family, self.font_size / 3))

            painter.setPen(QPen(Qt.white, Qt.SolidLine))

            painter.drawText(new_rec, Qt.AlignCenter, str(label))

            painter.restore()
            painter.setPen(QPen(Qt.black, Qt.SolidLine))
            painter.setFont(QFont(self.font_family, self.font_size / 3))


    def draw_node(self, node: L1Node, painter):
        """Draw the specified node."""
        if node._failed:
                painter.setBrush(QBrush(Qt.red,Qt.SolidPattern))
        else:
            painter.setBrush(
            QBrush(
                self.selected_color
                if node is self.selected_node
                else self.regular_node_color,
                Qt.SolidPattern,
            )
        )

        node_position = node.get_position()
        node_radius = Vector(node.get_radius()).repeat(2)
        #based on node position and radius create qrect
        #TODO mode this to Vector , lame to redo calculation
        top_left_x = node_position[0] - node_radius[0]
        top_lef_y = node_position[1] - node_radius[1]
        rec_width = node_radius[0] * 2
        rec_height = node_radius[0] * 2

        node_rec = QRect(top_left_x,top_lef_y,rec_width,rec_height)
        painter.drawRect(top_left_x,top_lef_y,rec_width,rec_height)

        label = node.label
        # scale font down, depending on the length of the label of the node
        painter.setFont(QFont(self.font_family, self.font_size / len(label)))
        #painter.setFont(QFont(self.font_family, self.font_size / 3 ))

        # draw the node label within the node dimensions
        painter.drawText(
            QRect(top_left_x,top_lef_y,rec_width,rec_height),
            Qt.AlignCenter,
            label,
        )

    def paintEvent(self, event):

        """Paints the board."""
        painter = QPainter(self)

        painter.setRenderHint(QPainter.Antialiasing, True)

        painter.setPen(QPen(Qt.black, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.lightGray, Qt.SolidPattern))

        painter.setClipRect(0, 0, self.canvas.width(), self.canvas.height())

        # background
        #painter.drawRect(0, 0, self.canvas.width(), self.canvas.height())

        painter.translate(*self.translation)
        painter.scale(self.scale, self.scale)

        #save (x,y) for each link
        self.vertex_positions = []



        #Draw Nodes
        #TODO Base on type draw different shapes
        #DWDM - round
        #repeater - Square

        for node1 in self.graph.l1nodes:
            for circuit in node1.circuits:
                #print('this is the circuit',circuit)
                node2 = circuit.target
                #Draw Links
                self.draw_vertex(node1, node2, circuit.label, circuit.link_num,  painter, circuit)

        for node in self.graph.l1nodes:
            self.draw_node(node, painter)




'''
#load
import sys
app = QApplication(sys.argv)
graph = Graph(directed=True,weighted=True)
#position: Vector, radius: float, label: str = None)
node1 = L1Node(Vector(10,20),radius=15,label='DWDM1')
node2 = L1Node(Vector(20,30),radius=15,label='DWDM2')


circuit1 = Circuit(label='ID1',target=node2,link_num=1)
circuit11 = Circuit(label='ID2',target=node2,link_num=2)
circuit111 = Circuit(label='ID3',target=node2,link_num=3)
circuit1111 = Circuit(label='ID4',target=node2,link_num=4)

node1.circuits.append(circuit1)
#node1.circuits.append(circuit11)
#node1.circuits.append(circuit111)
#node1.circuits.append(circuit1111)
graph.l1nodes.append(node1)
graph.l1nodes.append(node2)

ex = L1Model(graph)
sys.exit(app.exec_())
'''
