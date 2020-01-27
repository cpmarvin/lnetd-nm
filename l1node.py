import sys
sys.path.append("../")

from utilities import *

class L1Node():
    "A class to hold L1Node"
    def __init__(self, position: Vector, radius: float, label: str = None):
        #super(self.Node).__init__()
        self.label = label
        self.position = position
        self.radius = radius
        self.circuits = []
        self._failed = False

    def get_circuits(self):
        return self.circuits

    def failNode(self):
        self._failed = True
        #TODO this is duplicate now as the get_circuits_l1_node return the same
        for circuit in self.circuits:
            circuit.failCircuit()

    def unfailNode(self):
        self._failed = False
        #TODO this is duplicate now as the get_circuits_l1_node return the same
        for circuit in self.circuits:
            circuit.unfailCircuit()

    def __repr__(self) -> str:
        return self.label

    def get_x(self) -> float:
        """Returns the x coordinate of the node."""
        return self.position[0]

    def get_y(self) -> float:
        """Returns the y coordinate of the node."""
        return self.position[1]

    def get_position(self) -> Vector:
        """Returns the y coordinate of the node."""
        return self.position

    def get_radius(self) -> float:
        """Returns the radius of the node."""
        return self.radius

    def get_circuits(self) -> list:
        """Returns all circuits"""
        return self.circuits

    def set_x(self, value: float):
        """Sets the x coordinate of the node to the specified value."""
        self.position[0] = value

    def set_y(self, value):
        """Sets the y coordinate of the node to the specified value."""
        self.position[1] = value

    def set_position(self, value: Vector):
        """Sets the position of the node to the specified value."""
        self.position = value
