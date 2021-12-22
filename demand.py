from node import Node


class Demand:
    """Demand class to hold the
    required demand in Mbps between two
    graph Nodes"""

    def __init__(
        self,
        source: Node,
        target: Node,
        demand: float,
        demand_path: list = None,
    ):
        """
        :param source: The Source Node object
        :param target: The Target Node object
        :param demand: Float value for required demand
        :return: returns nothing"""
        self.source = source
        self.target = target
        self.total_metric = 0
        self.total_latency = 0
        self.demand = demand
        self.unrouted = False
        self.degraded = False
        self.demand_path = []
