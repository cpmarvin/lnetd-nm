#Vector

from utilities import Vector

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

    def adjust_canvas_translation(self, event):
        """Is called when the canvas widget is resized; changes translation so the
        center stays in the center."""
        size = Vector(event.size().width(), event.size().height())

        if self.canvas_size is not None:
            self.translation += self.scale * (size - self.canvas_size) / 2

        self.canvas_size = size

    def repulsion_force(self, distance: float) -> float:
        """Calculates the strength of the repulsion force at the specified distance."""
        return 1 / distance * 10 if self.forces_checkbox.isChecked() else 0

    def attraction_force(self, distance: float, leash_length=80) -> float:
        """Calculates the strength of the attraction force at the specified distance
        and leash length."""
        return (
            -(distance - leash_length) / 10 if self.forces_checkbox.isChecked() else 0
        )

    def show_help(self):
        """Is called when the help button is clicked; displays basic information about
        the application."""
        message = """
            <p><strong>LnetD QT5 Application</strong>.</p>
            <p>Traffic Model Example.
            It is powered by PyQt5 &ndash; a set of Python bindings for the C++ library Qt.</p>
            <hr />
            <p>The controls are as follows:</p>
            <ul>
            <li><em>Left Mouse Button</em> &ndash; selects nodes and moves them</li>
            <li><em>Mouse Wheel</em> &ndash; zooms in/out</li>
            <li><em>Select Node + Shift + Left Mouse Button</em> &ndash; moves graph</li>
            <li><em>Shift + Mouse Wheel</em> &ndash; rotates nodes around the selected node</li>
            <li><em>For traffic demands , add a source/target node and choose the demand value </em> &ndash; if you want additive demands , check the box</li>
            <li><em>Click on link metric</em> &ndash; will show link information</li>
            </ul>
            <hr />
            <p>Source Code and more information at
            <a href="https://github.com/cpmarvin/lnetd_qt">GitHub repository</a>.</p>
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
        # evaluate forces that act upon each pair of nodes
        for i, n1 in enumerate(self.graph.get_nodes()):
            for j, n2 in enumerate(self.graph.get_nodes()[i + 1 :]):
                # if they are not in the same component, no forces act on them
                if not self.graph.share_component(n1, n2):
                    continue

                # if the nodes are right on top of each other, no forces act on them
                d = distance(n1.get_position(), n2.get_position())
                if n1.get_position() == n2.get_position():
                    continue

                uv = (n2.get_position() - n1.get_position()).unit()

                # the size of the repel force between the two nodes
                fr = self.repulsion_force(d)

                # add a repel force to each of the nodes, in the opposite directions
                n1.add_force(-uv * fr)
                n2.add_force(uv * fr)

                # if they are also connected, add the attraction force
                if self.graph.does_vertex_exist(n1, n2, ignore_direction=True):
                    fa = self.attraction_force(d)

                    n1.add_force(-uv * fa)
                    n2.add_force(uv * fa)

            # since this node will not be visited again, we can evaluate the forces
            n1.evaluate_forces()

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

                for node in self.graph.get_nodes():
                    if node is not self.selected_node and self.graph.share_component(
                        node, self.selected_node
                    ):
                        node.set_position(node.get_position() + pos_delta)

        self.update()

    def __init__(self,graph):
        """Initial configuration."""
        super().__init__()
        #graph is common
        self.graph = graph
        self.selected_node: Node = None

        self.vertex_positions: List[Tuple[Vector, Tuple[Node, Node]]] = []
        self.selected_vertex: Tuple[Node, Node] = None

        # offset of the mouse from the position of the currently dragged node
        self.mouse_drag_offset: Vector = None

        # position of the mouse; is updated when the mouse moves
        self.mouse_position: Vector = Vector(-1, -1)

        # variables for visualizing the graph
        self.node_dwdm_radius: float = 15
        self.node_repetear_radius: float = 5

        self.weight_rectangle_size: float = 15

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
        self.canvas = QFrame(self, minimumSize=QSize(0, 300))
        self.canvas_size: Vector = None
        self.canvas.resizeEvent = self.adjust_canvas_translation


        # for showing the labels of the nodes
        self.labels_checkbox = QCheckBox(text="labels", checked=True)

        # sets, whether the graph is weighted or not
        self.weighted_checkbox = QCheckBox(
            text="weighted", clicked=self.set_weighted_graph
        )

        # enables/disables forces (True by default - they're fun!)
        self.forces_checkbox = QCheckBox(text="forces", checked=False)


        # input of the labels and vertex weights
        self.input_line_edit = QLineEdit(
            enabled=self.labels_checkbox.isChecked(),
            textChanged=self.input_line_edit_changed,
        )

        # displays information about the app
        self.about_button = QPushButton(
            text="?",
            clicked=self.show_help,
            sizePolicy=QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed),
        )
        #Layouts
        ##Main Layout with Canvas
        self.main_v_layout = QVBoxLayout(self, margin=0)
        self.main_v_layout.addWidget(self.canvas)

        #set Qwidget Layout
        self.setLayout(self.main_v_layout)
        self.setWindowTitle("LnetD - L1 Model")
        self.setFont(QFont(self.font_family, self.font_size))
        self.setWindowIcon(QIcon("icon.ico"))
        self.show()

    def paintEvent(self, event):
        pass
