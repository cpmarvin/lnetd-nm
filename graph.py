from __future__ import annotations
from dataclasses import dataclass
from typing import Set, List
import networkx as nx

class Demand:
    """A class for demand"""

    def __init__(self,source:Node,target:Node,demand:float):
        self.source = source
        self.target = target
        self.demand = demand

class Circuit:
    "A class for L1 circuit"
    def __init__(self, label : str , target: L1Node, linknum: int = 1):
        self.label = label
        self.target = target
        self.linknum = linknum
        self.interfaces = []
        self._failed = False

    def __repr__(self):
        return self.label

    def _fail(self):
        for interface in self.interfaces:
            interface.failInterface()
        self._failed = True


class Interface:
    """A class for interface model"""

    def __init__(self, target: Node , metric: int , local_ip: str , util : float, capacity: int , remote_ip: str = None,linknum: int = 1):
        self.target = target
        self.metric = metric
        self.util = 0 #util
        self.capacity = capacity
        self.local_ip = local_ip
        self.remote_ip = remote_ip
        self._failed = False
        self._on_spf = False
        self.link_num = linknum

    def __repr__(self):
        return self.local_ip

    def _networkX(self):
        return {"metric":self.metric}

    def utilization(self):
        """Returns utilization percent = (self.traffic/self.capacity)*100 """
        return (self.util / self.capacity)*100

    def get_label(self):
        return str(self.local_ip)

    def failInterface(self):
        """TODO fail the other end of the interafce ? """
        self._failed = True
        self.util = 0
        for interface in self.target.interfaces:
            if interface.remote_ip == self.local_ip:
                interface._failed = True
                interface.util = 0

    def unfailInterface(self):
        """TODO fail the other end of the interafce ? """
        self._failed = False
        self.util = 0
        for interface in self.target.interfaces:
            if interface.remote_ip == self.local_ip:
                interface._failed = False
                interface.util = 0
class L1Node():
    "A class to hold L1Node"

    def __init__(self, position: Vector, radius: float, label: str = None):
        #super(self.Node).__init__()
        self.circuits = []
        self._failed = False

    def get_circuits(self):
        return self.circuits

    def failNode(self):
        for circuit in self.circuits:
            circuit.failCircuit()
        self._failed = True

class Node:
    """A class for working with of nodes in a graph."""

    def __init__(self, position: Vector, radius: float, label: str = None):
        self.position = position
        self.radius = radius
        self.label = label

        #self.neighbours: Dict[Node, float] = {}
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
class Graph:
    """A class for working with graphs."""

    def __init__(self, directed=False, weighted=False):
        self.directed = directed
        self.weighted = weighted

        self.nodes: List[Node] = []
        self.components: Set[Node] = []
        self.demands: List[Demand] = []

    def reset_spf1(self,demand=False):
        for node in self.nodes:
            for interface in node.interfaces:
                interface._on_spf = False
                if demand:
                    interface.util = 0

    def calculate_components(self):
        """Calculate the components of the graph.
        MAJOR TODO: make component calculation faster when only removing a Vertex."""
        self.components = []

        for node in self.nodes:
            # the current set of nodes that we know are reachable from one another
            working_set = set( [node] + node.get_neighbours() )

            set_index = None

            i = 0
            while i < len(self.components):
                existing_set = self.components[i]

                # if an intersection exists, perform set union
                if len(existing_set.intersection(working_set)) != 0:
                    # if this is the first set to be merged, don't pop it from the list
                    # if we have already merged a set, it means that the working set
                    # joined two already existing sets
                    if set_index is None:
                        existing_set |= working_set
                        set_index = i
                        i += 1
                    else:
                        existing_set |= self.components.pop(set_index)
                        set_index = i - 1
                else:
                    i += 1

            # if we haven't performed any set merges, add the set to the continuity sets
            if set_index is None:
                self.components.append(working_set)
    def share_component(self, n1: Node, n2: Node) -> bool:
        """Returns True if both of the nodes are in the same component, else False."""

        for component in self.components:
            n1_in_s, n2_in_s = n1 in component, n2 in component
            # if both are in one set, we know for certain that they share a set
            # if only one is in a set, we know for certain that they can't share a set
            # otherwise, we can't be sure and have to check additional sets
            if n1_in_s and n2_in_s:
                return True
            elif n1_in_s or n2_in_s:
                return False

    def is_directed(self) -> bool:
        """Returns True if the graph is directed, else False."""
        return self.directed

    def set_directed(self, value: bool):
        """Sets, whether the graph is directed or not."""
        if not value:
            # make all vertexes go both ways
            for node in self.get_nodes():
                for neighbour in node.get_neighbours():
                    self.add_vertex(neighbour, node, weight=0)

        self.directed = value

    def is_weighted(self) -> bool:
        """Returns True if the graph is weighted and False otherwise."""
        return self.weighted

    def set_weighted(self, value: bool):
        """Sets, whether the graph is weighted or not."""
        self.weighted = value

    def get_weight(self, n1: Node, n2: Node):
        """Returns the weight of the specified vertex and None if it doesn't exist."""
        for n in n1.get_neighbours():
            if n2 == n['neighbour']:
                return 'test'
                #return True
        '''
        return (
            None
            if not self.does_vertex_exist(n1, n2)
            else self.nodes[self.nodes.index(n1)].neighbours[n2]
        )
        '''

    def get_nodes(self) -> List[Node]:
        """Returns a list of nodes of the graph."""
        return self.nodes

    def export_nodes(self):
        exported_nodes = []
        for node in self.nodes:
            exported_nodes.append(
                {"name":node.label,"x":node.position[0],"y":node.position[1]}
                )
        return exported_nodes

    def get_nodes_label(self) -> List[str]:
        """Returns a list of nodes label of the graph."""
        labels = []
        for node in self.nodes:
            labels.append(node.label)
        return labels

    def get_node_based_on_label(self,label) ->Node:
        for node in self.nodes:
            if node.label == label:
                return node


    def generate_label(self) -> str:
        """Returns a node label, based on the number of nodes in the tree in the form of
        A, B, C, ..., AA, AB, AC ...; note that the label is not meant to be a unique
        identifier!"""
        return "A" * (len(self.nodes) // 26) + chr(65 + len(self.nodes) % 26)

    def add_node(self, position: Vector, radius: float, label=None) -> Node:
        """Adds a new node to the graph and returns it."""
        if label is None:
            label = self.generate_label()

        node = Node(position, radius, label)
        self.nodes.append(node)

        #self.calculate_components()
        return node

    def add_demand(self,source:str,target:str,demand:float):
        source_node = self.get_node_based_on_label(source)
        target_node = self.get_node_based_on_label(target)
        if source_node not in self.nodes or target_node not in self.nodes:
            raise Exception(f'{source} or {target} not in the Graph')
        demand_object = Demand(source_node,target_node,demand)
        self.demands.append(demand_object)
        self.deploy_demands()
        #self.reset_spf(demand=True)

    def check_if_demand_exists_or_add(self,source_label:str,target_label:str,demand:float):
        source_node = self.get_node_based_on_label(source_label)
        target_node = self.get_node_based_on_label(target_label)
        damand_exists = False
        for existing_demand in self.demands:
            if source_node == existing_demand.source and target_node == existing_demand.target:
                existing_demand.demand += demand
                damand_exists = True
                self.redeploy_demands()
        if not damand_exists:
            self.add_demand(source=source_label,target=target_label,demand=demand)


    def remove_all_demands(self):
        self.demands = []
        for node in self.nodes:
            for interface in node.interfaces:
                interface._on_spf = False
                interface.util = 0

    def redeploy_demands(self):
        for node in self.nodes:
            for interface in node.interfaces:
                interface._on_spf = False
                interface.util = 0
        self.deploy_demands()

    def remove_node(self, node_to_be_removed: Node):
        """Deletes a node and all of the vertices that point to it from the graph."""
        # remove the actual node from the node list
        self.get_nodes().remove(node_to_be_removed)

        # remove all of its vertices
        for node in self.get_nodes():
            if node_to_be_removed in node.neighbours:
                del node.get_neighbours()[node_to_be_removed]

        self.calculate_components()

    def add_vertex(self, n1: Node, n2: Node, metric: float = 0, util: float = 0, local_ip: str = 'None', linknum: int = 0, spf: str = '0', capacity: int = 0 , remote_ip: str = 'Node'):
        """Adds a vertex from node n1 to node n2 (and vice versa, if it's not directed).
        Only does so if the given vertex doesn't already exist."""
        # from n1 to n2
        #n1.neighbours.append({n2:weight})
        #(self, target: Node , metric: int , local_ip: str , util : float, capacity: int , r_ip: str = None):
        interface = Interface(target=n2,metric=metric,util=util,local_ip=local_ip,capacity=capacity,remote_ip=remote_ip,linknum=linknum)
        n1.interfaces.append(interface)


        self.calculate_components()

    def does_vertex_exist(self, n1: Node, n2: Node, ignore_direction=False) -> bool:
        """Returns True if a vertex exists between the two nodes and False otherwise."""
        return n2 in n1.get_neighbours() or (
            (not self.directed or ignore_direction) and n1 in n2.get_neighbours()
            )

    def toggle_vertex(self, n1: Node, n2: Node):
        """Toggles a connection between to vertexes."""
        if self.does_vertex_exist(n1, n2):
            self.remove_vertex(n1, n2)
        else:
            self.add_vertex(n1, n2)

    def remove_vertex(self, n1: Node, n2: Node):
        """Removes a vertex from node n1 to node n2 (and vice versa, if it's not
        directed). Only does so if the given vertex exists."""
        # from n1 to n2
        if n2 in n1.neighbours:
            del n1.neighbours[n2]

        # from n2 to n1
        if not self.directed and n1 in n2.neighbours:
            del n2.neighbours[n1]

        self.calculate_components()

    def GetSpfPath(self, source: Node, target: Node, demand: int):
        G = nx.MultiDiGraph()
        node_list = self.get_nodes()
        for node in node_list:
            for interface in node.interfaces:
                if not interface._failed:
                    G.add_edge(node,interface.target,**interface._networkX(),data=interface)

        paths = list(nx.all_shortest_paths(G, source, target, weight='metric'))
        num_ecmp_paths = len(paths)
        demand_path = demand / num_ecmp_paths
        for p in paths:
            u=p[0]
            for v in p[1:]:
                values_u_v = G[u][v].values()
                min_weight = min(d['metric'] for d in values_u_v)
                ecmp_links = [k for k, d in G[u][v].items() if d['metric'] == min_weight]
                num_ecmp_links = len(ecmp_links)
                for d in ecmp_links:
                    G[u][v][d]['data'].util += int(demand_path)/int(num_ecmp_links)
                    G[u][v][d]['data']._on_spf = True
                u=v
    def get_interface_by_ip(self,label):
        for node in self.nodes:
            for interface in node.interfaces:
                if interface.local_ip == label:
                    return interface
    def get_demands(self):
        return self.demands

    def deploy_demands(self):
        for demand in self.demands:
            self.GetSpfPath(demand.source,demand.target,demand.demand)

    def get_number_of_links(self):
        nr_of_links = 0
        for node in self.nodes:
            nr_of_links += len(node.interfaces)
        return nr_of_links

    def get_all_interface(self):
        interface_list = []
        for node in self.nodes:
            interface_list += node.interfaces
        return interface_list

