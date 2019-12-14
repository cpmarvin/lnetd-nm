from objects.node import Node

class Demand:
    """Demand class to hold the
    required demand in Mbps between two
    graph Nodes"""

    def __init__(self,source:Node,target:Node,demand:float):
        """
        :param source: The Source Node object
        :param target: The Target Node object
        :param demand: Float value for required demand
        :return: returns nothing"""
        self.source = source
        self.target = target
        self.demand = demand
        self.unrouted = False
