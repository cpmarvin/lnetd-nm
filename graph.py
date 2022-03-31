from __future__ import annotations
from dataclasses import dataclass
from typing import Set, Tuple, List, Generic, Any, Dict, Callable
import ipdb

import networkx as nx
from  operator import itemgetter

from node import Node
from l1node import L1Node
from interface import Interface
from demand import Demand


class Graph:
    """A class for working with graphs."""

    def __init__(self, directed=False, weighted=False):
        self.directed = directed
        self.weighted = weighted

        self.nodes: List[Node] = []
        self.l1nodes: List[L1Node] = []
        self.components: Set[Node] = []
        self.demands: List[Demand] = []

    def reset_spf1(self, demand=False):
        for node in self.nodes:
            for interface in node.interfaces:
                interface._on_spf = False
                if demand:
                    interface.util = 0

    def return_total_metric(self,paths,g):
        total_metric = []
        total_latency = []
        total_capacity = []
        for p in paths:
            path_metric = 0
            path_latency = 0
            path_capacity = 0
            u=p[0]
            for v in p[1:]:
                #print(g[u][v]['data'].values())
                min_weight = min(d['metric'] for d in g[u][v].values())
                min_latency = min(d['data'].latency for d in g[u][v].values())
                min_capacity = min(d['data'].capacity for d in g[u][v].values())
                path_metric = path_metric + min_weight
                path_latency = path_latency + min_latency
                path_capacity = path_capacity + min_capacity
                u=v
            total_metric.append(path_metric)
            total_latency.append(path_latency)
            total_capacity.append(path_capacity)
        return min(total_metric),min(total_latency),min(total_capacity)

    def network_report(self):
        G = nx.MultiDiGraph()
        # node_list = [node for node in self.get_nodes() if not node._failed]
        node_list = self.get_nodes()
        for node in node_list:
            for interface in node.interfaces:
                if not interface._failed:
                    G.add_edge(
                        node, interface.target, **interface._networkX(), data=interface
                    )
        G.add_nodes_from(node_list)
        g_undirected = G.to_undirected()
        network_report = {}
        network_report['Connected Network'] = nx.is_connected(g_undirected)
        network_report['Number of Nodes'] = g_undirected.number_of_nodes()
        network_report['Number of Links'] = g_undirected.number_of_edges()
        network_report['Network Density'] = nx.density(g_undirected)
        if nx.is_connected(g_undirected):
            network_report['Network Diameter'] = nx.diameter(g_undirected)
        else:
            network_report['Network Diameter'] = 0
        degree_dict = dict(g_undirected.degree(g_undirected.nodes(),weight=''))
        sorted_degree = sorted(degree_dict.items(), key=itemgetter(1), reverse=True)
        network_report['Connectivity Node Degree'] = sorted_degree
        network_report['paths'] = []
        for node in node_list:
            source = node
            target_nodes = [ node for node in node_list if node!=source]
            for target in target_nodes:
                try:
                    paths = list(nx.all_shortest_paths(G, source, target, weight='metric'))
                    num_ecmp_paths = len(paths)
                    total_metric,total_latency,total_capacity = self.return_total_metric(paths,G)
                    entry = {'source':source,'target':target,'ecmp_paths':num_ecmp_paths,
		             'path_metric':total_metric,'total_latency':total_latency,'total_capacity':total_capacity,
                             'paths':paths,
                             'note':'valid'}
                except Exception as e:
                    entry = {'source':source,'target':target,'ecmp_paths':'None',
                             'path_metric':'None','total_latency':'None','total_capacity':'None',
                             'paths':'None',
                             'note':'NoPath'}
                    #print(e)
                network_report['paths'].append(entry)
        return network_report

    def calculate_components(self):
        """Calculate the components of the graph.
        MAJOR TODO: make component calculation faster when only removing a Vertex."""
        self.components = []

        for node in self.nodes:
            # the current set of nodes that we know are reachable from one another
            working_set = set([node] + node.get_neighbours())
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
            if n2 == n["neighbour"]:
                return "test"
                # return True
        """
        return (
            None
            if not self.does_vertex_exist(n1, n2)
            else self.nodes[self.nodes.index(n1)].neighbours[n2]
        )
        """

    def get_nodes(self) -> List[Node]:
        """Returns a list of nodes of the graph."""
        return self.nodes

    def export_nodes(self):
        exported_nodes = []
        for node in self.nodes:
            exported_nodes.append(
                {"name": node.label, "x": node.position[0], "y": node.position[1]}
            )
        return exported_nodes

    def get_nodes_label(self) -> List[str]:
        """Returns a list of nodes label of the graph."""
        labels = []
        for node in self.nodes:
            labels.append(node.label)
        return labels

    def get_node_based_on_label(self, label) -> Node:
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

        # self.calculate_components()
        return node

    def add_demand(self, source: str, target: str, demand: float):
        source_node = self.get_node_based_on_label(source)
        target_node = self.get_node_based_on_label(target)
        if source_node not in self.nodes or target_node not in self.nodes:
            raise Exception(f"{source} or {target} not in the Graph")

        damand_exists = False
        for existing_demand in self.demands:
            if (
                source_node == existing_demand.source
                and target_node == existing_demand.target
            ):
                existing_demand.demand += demand
                damand_exists = True
        if not damand_exists:
            demand_object = Demand(source_node, target_node, demand)
            self.demands.append(demand_object)

    def edit_demand(self,source:str,target:str,demand:float,delete=False):
        '''edit existing demands , or delete based on flag'''
        source_node = self.get_node_based_on_label(source)
        target_node = self.get_node_based_on_label(target)
        for existing_demand in self.demands:
            if (
                source == existing_demand.source.label
                and target == existing_demand.target.label
            ):
                if delete:
                    self.demands.remove(existing_demand)
                else:
                    existing_demand.demand = demand
    def enableDemand(self,source:str,target:str,enable=True):
        '''Activate or deactivate demand'''
        source_node = self.get_node_based_on_label(source)
        target_node = self.get_node_based_on_label(target)
        for existing_demand in self.demands:
            if (
                source == existing_demand.source.label
                and target == existing_demand.target.label
            ):
                if enable:
                    existing_demand.active = True
                else:
                    existing_demand.active = False

    def remove_all_demands(self):
        self.demands = []
        for node in self.nodes:
            for interface in node.interfaces:
                interface._on_spf = False
                interface.util = 0

    def redeploy_demands(self):
        # self.remove_all_demands()
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
            import copy

            node_interfaces = copy.copy(node.get_interfaces())
            for interface in node_interfaces:
                if node_to_be_removed == interface.target:
                    # TODO
                    node.removeInterface(interface)
        # self.redeploy_demands()

        self.calculate_components()

    def get_node_by_interface_ip(self, local_ip):
        all_nodes = self.get_nodes()
        interface_list = []
        for node in all_nodes:
            for interface in node.interfaces:
                if interface.local_ip == local_ip:
                    return node

    def remove_interface(self, interface_to_be_removed: Interface):
        # find the other interface so we remove both
        # find the node that has this ip
        node_source = self.get_node_by_interface_ip(interface_to_be_removed.local_ip)
        node_target = interface_to_be_removed.target
        remote_ip = interface_to_be_removed.remote_ip
        remote_interface = node_target.get_interface_by_ip(str(remote_ip))
        node_source.removeInterface(interface_to_be_removed)
        node_target.removeInterface(remote_interface)
        # self.calculate_components()

    def add_vertex(
        self,
        n1: Node,
        n2: Node,
        metric: float = 0,
        util: float = 0,
        local_ip: str = "None",
        linknum: int = 0,
        spf: str = "0",
        capacity: int = 0,
        remote_ip: str = "Node",
        latency: int = 0,
    ):
        """Adds a vertex from node n1 to node n2"""
        interface = Interface(
            target=n2,
            metric=metric,
            util=util,
            local_ip=local_ip,
            capacity=capacity,
            remote_ip=remote_ip,
            linknum=linknum,
            latency=latency,
        )
        n1.interfaces.append(interface)

    def does_vertex_exist(self, n1: Node, n2: Node, ignore_direction=False) -> bool:
        """Returns True if a vertex exists between the two nodes and False otherwise."""
        return n2 in n1.get_neighbours() or (
            (not self.directed or ignore_direction) and n1 in n2.get_neighbours()
        )

    def return_vertex_ifexist(self, n1: Node, n2: Node ) -> Interface:
        """Returns True if a vertex exists between the two nodes and False otherwise."""
        result  = [ interface for interface in n2.interfaces if interface.target == n1 ]
        if len(result) >= 1:
            return result,True
        return result,False

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

    def return_next_hops(self, all_paths, G):
        unique_next_hops = {}
        source = all_paths[0][0]
        unique_paths = set([p[1] for p in all_paths])
        unique_paths_list = [
            *unique_paths,
        ]
        for n1 in unique_paths_list:
            u = all_paths[0][0]
            v = n1
            values_u_v = G[u][v].values()
            min_weight = min(d["metric"] for d in values_u_v)
            ecmp_links = [k for k, d in G[u][v].items() if d["metric"] == min_weight]
            num_ecmp_links = len(ecmp_links)
            unique_next_hops[v] = num_ecmp_links
        return unique_next_hops

    def ShowSpfPath(self, source: Node, target: Node, set_highlight: False):
        total_metric = 0
        total_latency = 0
        e2e_path = []
        G = nx.MultiDiGraph()
        # node_list = [node for node in self.get_nodes() if not node._failed]
        node_list = self.get_nodes()
        for node in node_list:
            for interface in node.interfaces:
                if not interface._failed:
                    G.add_edge(
                        node, interface.target, **interface._networkX(), data=interface
                    )
        G.add_nodes_from(node_list)
        paths = list(nx.all_shortest_paths(G, source, target, weight="metric"))
        num_ecmp_paths = len(paths)
        for p in paths:
            total_metric = 0
            total_latency = 0
            u = p[0]
            for v in p[1:]:
                ecmp_max_latency = []
                values_u_v = G[u][v].values()
                min_weight = min(d["metric"] for d in values_u_v)
                total_metric = total_metric + min_weight
                # delete old path list
                ecmp_links = [
                    k for k, d in G[u][v].items() if d["metric"] == min_weight
                ]
                num_ecmp_links = len(ecmp_links)
                for d in ecmp_links:
                    ecmp_max_latency.append(G[u][v][d]["data"].latency)
                    if set_highlight:
                        G[u][v][d]["data"].highlight = True
                        peer_interface = self.get_peer_interface(G[u][v][d]["data"])
                        peer_interface.highlight = True
                    else:
                        G[u][v][d]["data"].highlight = False
                        peer_interface = self.get_peer_interface(G[u][v][d]["data"])
                        peer_interface.highlight = False

                    e2e_path.append(
                        [
                            u.label,
                            v.label,
                            min_weight,
                            G[u][v][d]["data"].latency,
                        ]
                    )
                total_latency = total_latency + max(ecmp_max_latency)
                u = v
            e2e_path.append(
                ["-", "-", "Total:" + str(total_metric), "Total:" + str(total_latency)]
            )
        return [total_metric, total_latency, e2e_path]

    def GetSpfPath(self, source: Node, target: Node, demand: int, demand_obj: Demand):
        G = nx.MultiDiGraph()
        # node_list = [node for node in self.get_nodes() if not node._failed]
        node_list = self.get_nodes()
        for node in node_list:
            for interface in node.interfaces:
                if not interface._failed:
                    G.add_edge(
                        node, interface.target, **interface._networkX(), data=interface
                    )
        G.add_nodes_from(node_list)
        all_paths = list(nx.all_shortest_paths(G, source, target, weight="metric"))
        self._GetSpfPathList(source, target, demand, demand_obj, G)
        unique_next_hop = self.return_next_hops(
            all_paths, G
        )  # set([p[1] for p in all_paths])

        demand_next_hop = demand / sum(unique_next_hop.values())
        # print("first all_paths", all_paths)
        # print("first unique all next hops", unique_next_hop)
        # print("first demands per next hop", demand_next_hop)
        temp_list = []
        for nh, values in unique_next_hop.items():
            """
            print(
                f"***{source} will send {demand} to { nh } as {demand_next_hop * values}"
            )
            """
            self._GetSpfPath(source, nh, demand_next_hop * values, G, demand_obj)
            temp_list.append({"source": nh, "demand": demand_next_hop * values})
        while len(temp_list) >= 1:
            for i, entry in enumerate(temp_list):
                # print(entry, target)
                if entry["source"] == target:
                    temp_list.pop(i)
                    continue
                all_paths = list(
                    nx.all_shortest_paths(G, entry["source"], target, weight="metric")
                )
                unique_next_hop = self.return_next_hops(
                    all_paths, G
                )  # set([p[1] for p in all_paths])
                demand_next_hop = entry["demand"] / sum(unique_next_hop.values())
                # print("all_paths", all_paths)
                # print("unique all next hops", unique_next_hop)
                # print("demands per next hop", demand_next_hop)
                src = entry["source"]
                for nh, values in unique_next_hop.items():
                    self._GetSpfPath(src, nh, demand_next_hop * values, G, demand_obj)
                    """
                    for entry2 in temp_list:
                        if entry2["source"] == nh:
                            entry2["demand"] += demand_next_hop
                    
                    print(
                        f"***{src} will send {demand} to { nh } as {demand_next_hop * values}"
                    )
                    """
                    temp_list.append({"source": nh, "demand": demand_next_hop * values})
                temp_list.pop(i)

    def _GetSpfPathList(
        self, source: Node, target: Node, demand: int, demand_obj: Demand, G
    ):
        """
        Used to create the path list , it's called by the new GetSpfPath that solves
        the issue with unequal load balancing when >3 paths
        """
        """
        G = nx.MultiDiGraph()
        # node_list = [node for node in self.get_nodes() if not node._failed]
        node_list = self.get_nodes()
        for node in node_list:
            for interface in node.interfaces:
                if not interface._failed:
                    G.add_edge(
                        node, interface.target, **interface._networkX(), data=interface
                    )
        G.add_nodes_from(node_list)
        """
        paths = list(nx.all_shortest_paths(G, source, target, weight="metric"))
        num_ecmp_paths = len(paths)
        demand_path = demand / num_ecmp_paths
        if paths:
            demand_obj.demand_path = []
        for p in paths:
            total_metric = 0
            total_latency = 0
            u = p[0]
            for v in p[1:]:
                ecmp_max_latency = []
                values_u_v = G[u][v].values()
                min_weight = min(d["metric"] for d in values_u_v)
                total_metric = total_metric + min_weight
                # delete old path list

                ecmp_links = [
                    k for k, d in G[u][v].items() if d["metric"] == min_weight
                ]
                num_ecmp_links = len(ecmp_links)
                for d in ecmp_links:
                    ecmp_max_latency.append(G[u][v][d]["data"].latency)
                    demand_obj.demand_path.append(
                        [
                            u.label,
                            v.label,
                            min_weight,
                            G[u][v][d]["data"].latency,
                        ]
                    )
                total_latency = total_latency + max(ecmp_max_latency)
                u = v
            demand_obj.demand_path.append(
                ["-", "-", "Total:" + str(total_metric), "Total:" + str(total_latency)]
            )
            demand_obj.total_latency = total_latency
            demand_obj.total_metric = total_metric

    def _GetSpfPath(
        self, source: Node, target: Node, demand: int, G, demand_obj: Demand
    ):
        """
        Used to put demands on the links , it's called by the new GetSpfPath that solves
        the issue with unequal load balancing when >3 paths
        """
        """
        G = nx.MultiDiGraph()
        # node_list = [node for node in self.get_nodes() if not node._failed]
        node_list = self.get_nodes()
        for node in node_list:
            for interface in node.interfaces:
                if not interface._failed:
                    G.add_edge(
                        node, interface.target, **interface._networkX(), data=interface
                    )
        G.add_nodes_from(node_list)
        """
        paths = list(nx.all_shortest_paths(G, source, target))
        num_ecmp_paths = len(paths)
        demand_path = demand / num_ecmp_paths
        for p in paths:
            u = p[0]
            for v in p[1:]:
                values_u_v = G[u][v].values()
                min_weight = min(d["metric"] for d in values_u_v)
                ecmp_links = [
                    k for k, d in G[u][v].items() if d["metric"] == min_weight
                ]
                num_ecmp_links = len(ecmp_links)
                for d in ecmp_links:
                    G[u][v][d]["data"].util += int(demand_path) / int(num_ecmp_links)
                    if G[u][v][d]["data"].util > G[u][v][d]["data"].capacity:
                        demand_obj.degraded = True
                    G[u][v][d]["data"]._on_spf = True
                u = v

    def get_demands(self):
        return self.demands

    def deploy_demands(self):
        for demand in self.demands:
            if demand.active:
                try:
                    self.GetSpfPath(demand.source, demand.target, demand.demand, demand)
                    demand.unrouted = False
                except Exception:
                    demand.unrouted = True
                    pass

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

    def get_all_interfaces_map(self):
        interface_list = self.get_all_interface()
        node_interfaces = {}
        for interface in interface_list:
            node_interfaces[interface.local_ip] = interface
        return node_interfaces

    def update_linknum(self, node1: Node, node2: Node):

        number_of_int_btw_nodes = [
            interface for interface in node2.interfaces if interface.target == node1
        ]
        i = 1
        node1_int = node1.interfaces
        node2_int = node2.interfaces

        for number, interface in enumerate(node1_int):
            if (
                interface.target == node2
                and interface.local_ip
                == node2.get_interface_by_ip(interface.remote_ip).remote_ip
            ):
                interface.link_num = i
                node2_interface = node2.get_interface_by_ip(interface.remote_ip)
                node2_interface.link_num = i
                i += 1

        # small check , this should be equal
        # TODO redo this
        if i != len(number_of_int_btw_nodes) + 1:
            raise Exception(
                "number not equal to number_of_int_btw_nodes , something is wrong"
            )

    def get_all_circuits(self):
        all_graph_circuits = []
        for l1node in self.l1nodes:
            all_graph_circuits += l1node.get_circuits()
        return all_graph_circuits

    def get_circuits_l1_node(self, n1):
        """Return a list of circuits where n1
        is either a source or a target in the graph"""
        # Create Graph MultiGraph ( undirected )
        circuit_list = []
        G = nx.MultiGraph()
        for node in self.l1nodes:
            for circuit in node.circuits:
                G.add_edge(node, circuit.target, data=circuit)
        # find all circuits
        for circuit in G.edges(n1):
            u = circuit[0]
            for v in circuit[1:]:
                ecmp_links = [k for k, d in G[u][v].items()]
                for d in ecmp_links:
                    if G[u][v][d]["data"] not in circuit_list:
                        circuit_list.append(G[u][v][d]["data"])
                u = v

        return circuit_list

    def get_unrouted_demands(self):
        return_list = [demand for demand in self.demands if demand.unrouted]
        return return_list

    def get_peer_interface(self, interface):
        """Return peer interface of a graph"""
        target_node = interface.target
        for t_interface in target_node.interfaces:
            if t_interface.local_ip == interface.remote_ip:
                return t_interface

    def update_all_demands(self,value,active_only=True):
        if active_only:
            all_demands = [ n for n in self.demands if n.active ]
        else:
            all_demands = self.demands
        #apply demands value
        for demand_entry in all_demands:
            demand_entry.demand = demand_entry.demand * (1 + value/100)
