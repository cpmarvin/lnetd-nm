import sys
sys.path.append("../")

from utilities import *
from typing import Tuple,List,Generic,Any,Dict,Callable

Node = Callable
Interface = Callable

class Node:
    """A class for working with of nodes in a graph."""

    def __init__(self, position: Vector, radius: float, label: str = None):
        self.position = position
        self.radius = radius
        self.label = label
        self.interfaces: List[Interface] = []
        self.forces: List[Vector] = []
        self._failed = False

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

    def get_neighbours(self) -> List[Node]:
        """Returns the neighbours of the node."""
        neigh_list = [ interface.target for interface in self.interfaces ]
        return neigh_list

    def get_neighbours1(self) -> Dict[Node, float]:
        """Returns the neighbours of the node."""
        neighbours = {}
        for n in self.neighbours:
            neighbours[n['neighbour']] = n['metric']

        return neighbours

    def get_interfaces(self) -> List[Interface]:
        """Returns the interfaces of a node"""
        return self.interfaces

    def get_label(self) -> str:
        """Returns the label of the node."""
        return self.label

    def set_x(self, value: float):
        """Sets the x coordinate of the node to the specified value."""
        self.position[0] = value

    def set_y(self, value):
        """Sets the y coordinate of the node to the specified value."""
        self.position[1] = value

    def set_position(self, value: Vector):
        """Sets the position of the node to the specified value."""
        self.position = value

    def set_label(self, label: str):
        """Sets the label of the node to the specified value."""
        self.label = label

    def add_force(self, force: Vector):
        """Adds a force that is acting upon the node to the force list."""
        self.forces.append(force)

    def evaluate_forces(self):
        """Evaluates all of the forces acting upon the node and moves it accordingly."""
        while len(self.forces) != 0:
            self.position += self.forces.pop()

    def export_links(self):
        exported_links = []
        for link in self.interfaces:
            exported_links.append({"source":self.label,
                    "target":link.target.label,
                    "metric":link.metric,
                    "util":link.util,
                    "capacity":link.capacity,
                    "local_ip":link.local_ip,
                    "remote_ip":link.remote_ip})
        return exported_links

    def failNode(self):
        self._failed = True
        for interface in self.interfaces:
            interface.failInterface()

    def unfailNode(self):
        self._failed = False
        for interface in self.interfaces:
            interface.unfailInterface()

    def removeInterface(self,interface):
        self.get_interfaces().remove(interface)

    def get_interface_by_ip(self,local_ip):
        for interface in self.interfaces:
            if interface.local_ip == local_ip:
                return interface
