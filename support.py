import json
from graph import Graph
from node import Node
from interface import Interface
from demand import Demand

from utilities import Vector
from random import randint
import pprint
import requests

import os
import sys


def generate_path_config():
    config_name = "config.ini"

    if getattr(sys, "frozen", False):
        application_path = os.path.dirname(sys.executable)
        application_path = sys._MEIPASS
    elif __file__:
        application_path = os.path.dirname(__file__)
        application_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(application_path, config_name)
    return config_path


def load_graph_web(lnetd_web_url, lnetd_web_user, lnetd_web_password):
    """load json and return the graph()"""
    session = requests.Session()
    session.verify = False
    r = session.get(
        lnetd_web_url,
        verify=False,
        auth=requests.auth.HTTPBasicAuth(lnetd_web_user, lnetd_web_password),
    )
    if not r.status_code == 200:
        raise ValueError(
            f"Failed to get devices from LnetD HTTP error code {r.status_code}"
        )
    resp = r.json()
    data = generate_link_number(resp["links"])
    host_data = resp["nodes"]
    # set the properties of the graph
    directed = True
    weighted = True
    # graph Object
    graph = Graph(directed=directed, weighted=weighted)

    node_dictionary = {}
    # add each of the nodes of the vertex to the graph
    for vertex in data:
        vertex_components = vertex
        nodes = [
            vertex_components["source"],
            vertex_components["target"],
        ]

        metric = int(vertex_components["metric"])
        util = 0  # vertex_components['util']
        l_ip = vertex_components["local_ip"]
        linknum = vertex_components["linknum"]
        capacity = vertex_components["capacity"]
        latency = vertex_components.get("latency",1)
        # print(vertex_components.get('remote_ip'))
        for node in nodes:
            import_coordinates = False
            if node not in node_dictionary:
                # TODO improve this , maybe a dict instead of list ?!
                for node_json in host_data:
                    #
                    if node_json.get("name") == node:
                        x1 = node_json.get("x")
                        y1 = node_json.get("y")
                        import_coordinates = True
                        break

                # try to get the (x,y) and if not slightly randomize the coordinates, so the graph
                # doesn't stay in one place
                if import_coordinates:
                    x = x1
                    y = y1
                else:
                    x = randint(1, 200)
                    y = randint(1, 200)

                # add it to graph with default values
                node_dictionary[node] = graph.add_node(Vector(x, y), 40, node)
        # get the node objects from the names
        n1, n2 = node_dictionary[nodes[0]], node_dictionary[nodes[1]]
        graph.add_vertex(
            n1=n1,
            n2=n2,
            metric=metric,
            util=util,
            local_ip=vertex_components["local_ip"],
            linknum=linknum,
            capacity=capacity,
            remote_ip=(
                vertex_components.get("remote_ip")
                if vertex_components.get("remote_ip")
                else "None"
            ),
            latency=int(latency),
        )
    # if everything was successful, override the current graph
    return graph


def load_graph(path):
    """load json and return the graph()"""
    with open(path, "r") as file:
        lnetd_graph = json.load(file)
    # generate_link_number add a link_num to json
    # pprint.pprint(lnetd_graph)
    data = generate_link_number(lnetd_graph["links"])
    host_data = lnetd_graph["nodes"]

    # set the properties of the graph
    directed = True
    weighted = True
    # graph Object
    graph = Graph(directed=directed, weighted=weighted)

    node_dictionary = {}
    # add each of the nodes of the vertex to the graph
    for vertex in data:
        vertex_components = vertex
        nodes = [
            vertex_components["source"],
            vertex_components["target"],
        ]

        metric = int(vertex_components["metric"])
        util = 0  # vertex_components['util']
        l_ip = vertex_components["local_ip"]
        linknum = vertex_components["linknum"]
        capacity = vertex_components["capacity"]
        latency = int(vertex_components.get("latency",1))
        # print(vertex_components.get('remote_ip'))
        for node in nodes:
            import_coordinates = False
            if node not in node_dictionary:
                # TODO improve this , maybe a dict instead of list ?!
                for node_json in host_data:
                    #
                    if node_json.get("name") == node:
                        x1 = node_json.get("x")
                        y1 = node_json.get("y")
                        import_coordinates = True
                        break

                # try to get the (x,y) and if not slightly randomize the coordinates, so the graph
                # doesn't stay in one place
                if import_coordinates:
                    x = x1
                    y = y1
                else:
                    x = randint(1, 5600)
                    y = randint(1, 5600)

                # add it to graph with default values
                node_dictionary[node] = graph.add_node(Vector(x, y), 40, node)
        # get the node objects from the names
        n1, n2 = node_dictionary[nodes[0]], node_dictionary[nodes[1]]
        graph.add_vertex(
            n1=n1,
            n2=n2,
            metric=metric,
            util=util,
            local_ip=vertex_components["local_ip"],
            linknum=linknum,
            capacity=capacity,
            remote_ip=(
                vertex_components.get("remote_ip")
                if vertex_components.get("remote_ip")
                else "None"
            ),
            latency=latency,
        )
    # if everything was successful, override the current graph
    return graph


def generate_link_number(lnetd_links):
    """Generate link number
    for parallel links"""
    lnetd_links = sorted(lnetd_links, key=lambda i: (i["source"], i["target"]))
    i = 0
    while i < len(lnetd_links):
        if i == 0:
            lnetd_links[i]["linknum"] = 1
        elif (
            lnetd_links[i]["source"] == lnetd_links[i - 1]["source"]
            and lnetd_links[i]["target"] == lnetd_links[i - 1]["target"]
        ):
            lnetd_links[i]["linknum"] = lnetd_links[i - 1]["linknum"] + 1
        else:
            lnetd_links[i]["linknum"] = 1
        i = i + 1
    return lnetd_links
