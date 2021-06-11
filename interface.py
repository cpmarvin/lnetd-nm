from networkx import exception
from node import Node


class Interface:
    """A class for interface model"""

    def __init__(
        self,
        target: Node,
        metric: int,
        local_ip: str,
        util: float,
        capacity: int,
        remote_ip: str = None,
        linknum: int = 1,
        latency: int = 0,
    ):
        self.target = target
        self.metric = metric
        self.util = 0  # util
        self.capacity = capacity
        self.local_ip = local_ip
        self.remote_ip = remote_ip
        self._failed = False
        self._on_spf = False
        self.link_num = linknum
        self.latency = latency

    def __repr__(self):
        return self.local_ip

    def _networkX(self):
        return {"metric": self.metric}

    def utilization(self):
        """Returns utilization percent = (self.traffic/self.capacity)*100 """
        try:
            return round((self.util / self.capacity) * 100, 3)
        except exception:
            return -1

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

    def change_metric(self, value):
        self.metric = value
