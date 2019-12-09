import sys
import json
sys.path.append('../')

from graph import Graph,Node,Interface,Demand
from graph import L1Node,Circuit
from utilities import *

lnetd_links = [
    {'source': 'gb-p10-lon', 'target': 'gb-pe5-lon', 'local_ip': '10.5.10.10', 'metric': '10', 'r_ip': '10.5.10.5', 'util': 0, 'capacity': 1000} ,
    {'source': 'gb-p10-lon', 'target': 'gb-pe8-lon', 'local_ip': '10.8.10.10', 'metric': '10', 'r_ip': '10.8.10.8', 'util': 0, 'capacity': 1000} ,
    {'source': 'gb-p10-lon', 'target': 'fr-p7-mrs', 'local_ip': '10.7.10.10', 'metric': '10', 'r_ip': '10.7.10.7', 'util': 0, 'capacity': 1000} ,
    {'source': 'gb-pe8-lon', 'target': 'gb-pe5-lon', 'local_ip': '10.5.8.8', 'metric': '10', 'r_ip': '10.5.8.5', 'util': 0, 'capacity': 1000} ,
    {'source': 'gb-pe8-lon', 'target': 'gb-p10-lon', 'local_ip': '10.8.10.8', 'metric': '10', 'r_ip': '10.8.10.10', 'util': 0, 'capacity': 1000} ,
    {'source': 'gb-pe5-lon', 'target': 'gb-p10-lon', 'local_ip': '10.5.10.5', 'metric': '10', 'r_ip': '10.5.10.10', 'util': 0, 'capacity': 1000} ,
    {'source': 'gb-pe5-lon', 'target': 'gb-pe8-lon', 'local_ip': '10.5.8.5', 'metric': '10', 'r_ip': '10.5.8.8', 'util': 0, 'capacity': 1000} ,
    {'source': 'gb-pe5-lon', 'target': 'gb-pe11-lon', 'local_ip': '10.5.11.5', 'metric': '10', 'r_ip': '10.5.11.11', 'util': 0, 'capacity': 1000} ,
    {'source': 'fr-p7-mrs', 'target': 'ke-p6-nbi', 'local_ip': '10.6.7.7', 'metric': '10', 'r_ip': '10.6.7.6', 'util': 0, 'capacity': 1000} ,
    {'source': 'fr-p7-mrs', 'target': 'gb-p10-lon', 'local_ip': '10.7.10.7', 'metric': '5', 'r_ip': '10.7.10.10', 'util': 0, 'capacity': 1000} ,
    {'source': 'ke-p6-nbi', 'target': 'ke-pe2-nbi', 'local_ip': '10.2.6.6', 'metric': '10', 'r_ip': '10.2.6.2', 'util': 0, 'capacity': 1000} ,
    {'source': 'ke-p6-nbi', 'target': 'fr-p7-mrs', 'local_ip': '10.6.7.6', 'metric': '10', 'r_ip': '10.6.7.7', 'util': 0, 'capacity': 1000} ,
    {'source': 'ke-pe3-nbi', 'target': 'ke-pe2-nbi', 'local_ip': '10.2.3.3', 'metric': '5000', 'r_ip': '10.2.3.2', 'util': 0, 'capacity': 1000} ,
    {'source': 'ke-pe3-nbi', 'target': 'ke-pe2-nbi', 'local_ip': '10.22.33.33', 'metric': '10', 'r_ip': '10.22.33.22', 'util': 0, 'capacity': 1000} ,
    {'source': 'ke-pe2-nbi', 'target': 'ke-pe3-nbi', 'local_ip': '10.2.3.2', 'metric': '5000', 'r_ip': '10.2.3.3', 'util': 0, 'capacity': 1000} ,
    {'source': 'ke-pe2-nbi', 'target': 'ke-pe3-nbi', 'local_ip': '10.22.33.22', 'metric': '5000', 'r_ip': '10.22.33.33', 'util': 0, 'capacity': 1000} ,
    {'source': 'ke-pe2-nbi', 'target': 'ke-p6-nbi', 'local_ip': '10.2.6.2', 'metric': '10', 'r_ip': '10.2.6.6', 'util': 0, 'capacity': 1000} ,
    {'source': 'ke-pe2-nbi', 'target': 'ke-pe3-nbi', 'local_ip': '10.22.33.22', 'metric': '10', 'r_ip': '10.22.33.33', 'util': 0, 'capacity': 1000} ,
    {'source': 'nl-p13-ams', 'target': 'gb-pe11-lon', 'local_ip': '10.111.13.13', 'metric': '10', 'r_ip': '10.111.13.11', 'util': 0, 'capacity': 1000} ,
    {'source': 'nl-p13-ams', 'target': 'gb-pe11-lon', 'local_ip': '10.11.13.13', 'metric': '10', 'r_ip': '10.11.13.11', 'util': 0, 'capacity': 1000} ,
    {'source': 'gb-pe11-lon', 'target': 'gb-pe5-lon', 'local_ip': '10.5.11.11', 'metric': '10', 'r_ip': '10.5.11.5', 'util': 0, 'capacity': 1000} ,
    {'source': 'gb-pe11-lon', 'target': 'nl-p13-ams', 'local_ip': '10.111.13.11', 'metric': '10', 'r_ip': '10.111.13.13', 'util': 0, 'capacity': 1000} ,
    {'source': 'gb-pe11-lon', 'target': 'nl-p13-ams', 'local_ip': '10.11.13.11', 'metric': '10', 'r_ip': '10.11.13.13', 'util': 0, 'capacity': 1000} ,
]

def load_graph(lnetd_links):
    data = lnetd_links

    directed = True
    weighted = True

    graph = Graph(directed=directed, weighted=weighted)

    node_dictionary = {}

    for vertex in data:
        #print(vertex)
        vertex_components = vertex

        # the formats are either 'A B' or 'A <something> B'
        nodes = [
            vertex_components['source'],
            vertex_components['target'],
            ]

        # if weights are present, the formats are:
        # - 'A B num' for undirected graphs
        # - 'A <something> B num (num)' for directed graphs
        metric = int(vertex_components['metric'])
        util = 0 #vertex_components['util']
        l_ip = vertex_components['local_ip']
        linknum = 1
        capacity = vertex_components['capacity']

        for node in nodes:
            #print(node)
            import_coordinates = False
            if node not in node_dictionary:
                x = 1 #self.canvas.width() / 2 + (random() - 0.5) + randint(1,600)
                y = 2 #self.canvas.height() / 2 + (random() - 0.5) + randint(1,600)

                # add it to graph with default values
                node_dictionary[node] = graph.add_node(
                    Vector(x, y), 3 , node
                )
        # get the node objects from the names
        n1, n2 = node_dictionary[nodes[0]], node_dictionary[nodes[1]]

        graph.add_vertex(
            n1=n1,
            n2=n2,
            metric = metric,
            util = util,
            local_ip =l_ip,
            linknum= linknum,
            capacity= capacity
        )
    return  graph

graph = load_graph(lnetd_links)


graph.check_if_demand_exists_or_add('nl-p13-ams','ke-pe2-nbi',500)
#print('start',graph.demands)
graph.check_if_demand_exists_or_add('ke-pe2-nbi','nl-p13-ams',100)
#print('start',graph.demands)

print('start',graph.demands)
def load_demands(graph):
    for row_number , row_data in enumerate(graph.get_all_interface()):
        #print(row_number,row_data)
        #print(enumerate(vars(row_data).items()))
        print(row_data.__dict__.keys())
        #DemandTable.insertRow(row_number)
        for column_number, data in enumerate( row_data.__dict__.values() ):
            #print(column_number,data)
            pass
            #print(column_number, data)
load_demands(graph)

#print(graph.get_all_interface())


print(graph)
def get_interface_by_ip(self,local_ip):
    all_nodes = graph.get_nodes()
    interface_list = []
    for node in all_nodes:
        interface_list += node.get_interfaces()
    interface = [ interface for interface in interface_list if interface.local_ip == '1.1.1.1']
    return interface[0]

#get node by interface_ip

def get_node_by_interface_ip(self,local_ip):
    all_nodes = self.get_nodes()
    interface_list = []
    for node in all_nodes:
        for interface in node.interfaces:
            print(interface.local_ip)
            if interface.local_ip == local_ip:
                return node

print(get_node_by_interface_ip('10.5.10.10'))

