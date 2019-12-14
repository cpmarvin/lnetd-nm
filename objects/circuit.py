from objects.l1node import L1Node

class Circuit:
    """Circuit class to hold a possible
    L1 Circuit. The circuit is used for L1 Topology
    and maps multiple L3 interfaces"""
    def __init__(self, label : str , target: L1Node, link_num: int = 1):
        """
        :param label: Circuit ID/Label
        :param target: The Target L1 Node object
        :param link_num: Defaults to 1, used in visualization if multiple links exits btw nodes
        :return: returns nothing"""
        self.label = label
        self.target = target
        self.link_num = link_num
        self.interfaces = []
        self._failed = False

    def __repr__(self):
        return self.label

    def failCircuit(self):
        """Change state of a circuit and the associated interfaces
        for both itself and his neighbour L1node if there
        #TODO Find a way to fail circuits for a pair node without
        any circuits as the Graph for L1 is directed"""
        self._failed = True
        for interface in self.interfaces:
            #print('this is interface in failCircuit',interface)
            interface.failInterface()

    def unfailCircuit(self):
        """Change state of a circuit and the associated interfaces
        for both itself and his neighbour L1node if there
        #TODO Find a way to fail circuits for a pair node without
        any circuits as the Graph for L1 is directed"""
        self._failed = False
        for interface in self.interfaces:
            #print('this is interface in unfailCircuit',interface)
            interface.unfailInterface()

    def get_interfaces(self):
        """Return all L3 interfaces"""
        return self.interfaces
