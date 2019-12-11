import sys
import json
sys.path.append('../')

from objects.graph import Graph,Node,Interface,Demand
from objects.l1node import L1Node
from objects.circuit import Circuit
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
            capacity= capacity,
            remote_ip = vertex_components['r_ip']
        )
    return  graph

graph = load_graph(lnetd_links)


graph.check_if_demand_exists_or_add('ke-pe3-nbi','nl-p13-ams',500)
print('start',graph.demands)
#graph.check_if_demand_exists_or_add('ke-pe2-nbi','nl-p113-ams',100)
#print('start',graph.demands)
node1 = graph.get_node_based_on_label('nl-p13-ams')
node2 = graph.get_node_based_on_label('ke-pe2-nbi')
#node1.failNode()
'''
try:
    graph.check_if_demand_exists_or_add('ke-pe3-nbi','nl-p13-ams',500)
except Exception as e:
    print('ddd',e)
'''
graph.check_if_demand_exists_or_add('ke-pe3-nbi','nl-p13-ams',500)


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



node_list = graph.get_nodes()
print(node_list)

def generate_link_number(lnetd_links):
    i = 0
    while i < len(lnetd_links):
        if i==0:
            lnetd_links[1]['linknum'] = 1
        if lnetd_links[i]['source'] == lnetd_links[i-1]['source'] and lnetd_links[i]['target'] == lnetd_links[i-1]['target']:
            lnetd_links[i]['linknum'] = lnetd_links[i-1]['linknum'] + 1;
        else:
            lnetd_links[i]['linknum'] = 1;
        i = i+1
    return lnetd_links

def update_linknum(node1,node2):

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




#update_linknum(node_list[6],node_list[7])
#self, label : str , target: L1Node, linknum: int = 1

def load_dummy(graph):
    all_intefaces = graph.get_all_interface()
    #print(all_intefaces)

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

    graph.l1nodes.append(uk_a)
    graph.l1nodes.append(nl_a)
    graph.l1nodes.append(fr_a)
    graph.l1nodes.append(ke_a)



load_dummy(graph)
print(graph.l1nodes)
failed_l3_interface = [ interface for interface in graph.get_all_interface() if interface._failed]
print(failed_l3_interface)


import networkx as nx
def get_all_l1_node_interfaces(graph,n1):
    """Return a list of circuits where n1
    is either a source or a target in the graph"""
    #Create Graph
    circuit_list = []
    G = nx.MultiGraph()
    for node in graph.l1nodes:
        for circuit in node.circuits:
            G.add_edge(node,circuit.target,data=circuit)
    #find all circuits
    print('>>Node',n1)
    print('>>Edges',G.edges(n1))
    for circuit in G.edges(n1):
        u=circuit[0]
        for v in circuit[1:]:
            ecmp_links = [k for k, d in G[u][v].items()]
            for d in ecmp_links:
                if G[u][v][d]['data'] not in circuit_list:
                    circuit_list.append(G[u][v][d]['data'])
            u=v

    return circuit_list


t = get_all_l1_node_interfaces(graph,graph.l1nodes[1])
print(t)
