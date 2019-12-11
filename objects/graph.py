from __future__ import annotations
from dataclasses import dataclass
from typing import Set, List
import networkx as nx

from objects.node import Node
from objects.l1node import L1Node
from objects.interface import Interface
from objects.demand import Demand


class Graph:
    """A class for working with graphs."""

    def __init__(self, directed=False, weighted=False):
        self.directed = directed
        self.weighted = weighted

        self.nodes: List[Node] = []
        self.l1nodes: List[L1Node] = []
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
        self.redeploy_demands()
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
            for interface in node.get_interfaces():
                print (interface.target)
                if node_to_be_removed  == interface.target:
                    #TODO
                    node.removeInterface(interface)
        self.redeploy_demands()
        self.calculate_components()


    def get_node_by_interface_ip(self,local_ip):
        all_nodes = self.get_nodes()
        interface_list = []
        for node in all_nodes:
            for interface in node.interfaces:
                #print(interface.local_ip)
                if interface.local_ip == local_ip:
                    return node

    def remove_interface(self,interface_to_be_removed:Interface):
        #find the other interface so we remove both
        #find the node that has this ip
        node_source = self.get_node_by_interface_ip(interface_to_be_removed.local_ip)
        # i already know the target node as it's in the Interface Object
        node_target = interface_to_be_removed.target
        # i know the remove ip
        remote_ip = interface_to_be_removed.remote_ip
        # find the interface based on ip
        remote_interface = node_target.get_interface_by_ip(str(remote_ip))
        #remove selected interface and his pair
        print('interface_to_be_removed',interface_to_be_removed)
        print('remote_interface',remote_interface)
        node_source.removeInterface(interface_to_be_removed)
        node_target.removeInterface(remote_interface)
        self.redeploy_demands()
        self.calculate_components()

    def add_vertex(self, n1: Node, n2: Node, metric: float = 0, util: float = 0, local_ip: str = 'None', linknum: int = 0,
        spf: str = '0', capacity: int = 0 , remote_ip: str = 'Node'):
        """Adds a vertex from node n1 to node n2"""
        #print(f'iside add_vertex n1: {n1} , n2:{n2}')
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
        try:
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
        except Exception:
            #TODO Exception propagation
            pass
            #raise
            #self.faildemands.append()

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

    def update_linknum(self,node1: Node,node2: Node):

        number_of_int_btw_nodes = [ interface for interface in node2.interfaces if interface.target == node1]
        #print(len(number_of_int_btw_nodes))
        i = 1
        node1_int = node1.interfaces
        node2_int = node2.interfaces
        for number, interface in enumerate(node1_int):
            if interface.target == node2 and interface.local_ip == node2.get_interface_by_ip(interface.remote_ip).remote_ip:
                #print(f'found one interface with target {node2} - {interface} with local_ip {interface.local_ip} and remote_ip {interface.remote_ip} and link_num {interface.link_num}')
                #print(f'updating link_num')
                interface.link_num = i
                #print(f'link_num is now {interface.link_num}')
                node2_interface = node2.get_interface_by_ip(interface.remote_ip)
                #print(f'found the pair interface {node2_interface} link_num {node2_interface.link_num}')
                #print(f'updating link_num')
                node2_interface.link_num = i
                #print(f'link_num is now {node2_interface.link_num}')
                i += 1
        #small check , this should be equal
        #TODO redo this
        if i != len(number_of_int_btw_nodes) +1 :
            raise Exception

    def get_all_circuits(self):
        all_graph_circuits = []
        for l1node in self.l1nodes:
            all_graph_circuits += l1node.get_circuits()
        return all_graph_circuits

    def get_circuits_l1_node(self,n1):
        """Return a list of circuits where n1
        is either a source or a target in the graph"""
        #Create Graph MultiGraph ( undirected )
        circuit_list = []
        G = nx.MultiGraph()
        for node in self.l1nodes:
            for circuit in node.circuits:
                G.add_edge(node,circuit.target,data=circuit)
        #find all circuits
        for circuit in G.edges(n1):
            u=circuit[0]
            for v in circuit[1:]:
                ecmp_links = [k for k, d in G[u][v].items()]
                for d in ecmp_links:
                    if G[u][v][d]['data'] not in circuit_list:
                        circuit_list.append(G[u][v][d]['data'])
                u=v

        return circuit_list
