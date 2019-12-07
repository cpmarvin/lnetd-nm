import sys
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
        util = 0
        local_ip = vertex_components['local_ip']
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
            local_ip = local_ip,
            remote_ip = ( 'None' if not vertex_components.get("remote_ip") else remote_ip),
            linknum= linknum,
            capacity= capacity
        )
    return  graph

graph = load_graph(lnetd_links)

def test_graph_load():
    assert load_graph(lnetd_links)

def get_number_of_graph_nodes(graph):
    #check number of nodes
    return len(graph.get_nodes())

def get_number_of_graph_links(graph):
    #check number of nodes
    number_of_links = 0
    for node in graph.nodes:
        for interface in node.interfaces:
            number_of_links += 1
    return number_of_links


def test_number_of_nodes():
    assert get_number_of_graph_nodes(graph) == 9

def test_number_of_links():
    assert get_number_of_graph_links(graph) == 23


# get two nodes from graph
node1 = graph.get_node_based_on_label('nl-p13-ams')
node2 = graph.get_node_based_on_label('ke-pe2-nbi')
'''
def get_spf_between_nodes(graph,node1,node2):
    spf = graph.GetSpfPath(node1,node2,0)
    spf_result = []
    for node in graph.nodes:
        for interface in node.interfaces:
            if interface._on_spf:
                spf_result.append({interface.get_label(): interface.utilization()})
    graph.reset_spf()
    return(spf_result)

def test_spf_path_between_nodes():
    expected_result = [{'10.7.10.10': 0.0}, {'10.5.10.5': 0.0}, {'10.6.7.7': 0.0}, {'10.5.11.11': 0.0},
                       {'10.2.6.6': 0.0}, {'10.111.13.13': 0.0}, {'10.11.13.13': 0.0}
                       ]
    print(expected_result)
    assert get_spf_between_nodes(graph,node1,node2) == expected_result

'''
def get_demand_between_nodes(graph,node1:str,node2:str,demand):
    depoly_demand = graph.check_if_demand_exists_or_add(str(node1),str(node2),demand)
    demand_result = []
    for node in graph.nodes:
        for interface in node.interfaces:
            if interface.util != 0.0 :
                demand_result.append({interface.get_label(): interface.utilization()})
    graph.remove_all_demands()
    return demand_result

def test_demand_between_nodes():
    expected_result = [{'10.7.10.10': 100.0}, {'10.5.10.5': 100.0}, {'10.6.7.7': 100.0}, {'10.5.11.11': 100.0}, {'10.2.6.6': 100.0}, {'10.111.13.13': 50.0}, {'10.11.13.13': 50.0}]
    assert get_demand_between_nodes(graph,'nl-p13-ams','ke-pe2-nbi',1000) == expected_result


def test_demand_between_nodes_metric_changed():
    interface_change = graph.get_interface_by_ip('10.111.13.13')
    interface_change.metric  = 99100
    result = get_demand_between_nodes(graph,node1,node2,1000)
    #reset interface metric
    interface_change.metric  = 10
    expected_result = [{'10.7.10.10': 100.0}, {'10.5.10.5': 100.0}, {'10.6.7.7': 100.0}, {'10.5.11.11': 100.0}, {'10.2.6.6': 100.0}, {'10.11.13.13': 100.0}]
    assert result == expected_result

def test_demand_between_nodes_fail_interface():
    interface_change = graph.get_interface_by_ip('10.11.13.13')
    interface_change.failInterface()
    result = get_demand_between_nodes(graph,node1,node2,1000)
    expected_result = [{'10.7.10.10': 100.0}, {'10.5.10.5': 100.0}, {'10.6.7.7': 100.0}, {'10.5.11.11': 100.0}, {'10.2.6.6': 100.0}, {'10.111.13.13': 100.0}]
    assert result == expected_result

'''
TODO TEST graph deploy multiple demands
#demands
demand1 = Demand(node1,node2,500)
demand2 = Demand(node1,node2,500)

graph.add_demand(node1,node2,500)
graph.add_demand(node1,node2,500)

print(graph.get_demands())

graph.deploy_demands()
spf_result = []
for node in graph_nodes:
    for interface in node.interfaces:
        if interface.util != 0.0 :
            spf_result.append({interface.get_label(): interface.utilization()})
print(spf_result)
expected_result = [{'10.7.10.10': 100.0}, {'10.5.10.5': 100.0}, {'10.6.7.7': 100.0}, {'10.5.11.11': 100.0}, {'10.2.6.6': 100.0}, {'10.111.13.13': 50.0}, {'10.11.13.13': 50.0}]
if expected_result == spf_result:
    print('all ok')
else:
    raise Exception
graph.reset_spf()

'''
