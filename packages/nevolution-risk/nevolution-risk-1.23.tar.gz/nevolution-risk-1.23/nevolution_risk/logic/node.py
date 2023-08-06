from nevolution_risk.constants import colors
from nevolution_risk.logic import graph
from nevolution_risk.logic.player import Player


class Node(object):
    id = 0
    adj_list = []
    player = Player('default', 0, colors.white)

    def __init__(self, id):
        self.id = id

    def add_node_to_list(self, node):
        self.adj_list.append(node)


if __name__ == '__main__':
    test_list = []
    test_player = Player('joern', 0, colors.white)
    test_node = Node(1)
    test_node.player = test_player

    node1 = Node(1)
    node4 = Node(4)
    node5 = Node(5)
    node5.add_node_to_list(node1)
    node5.add_node_to_list(node4)

    print(graph.Graph().nodes[0].adj_list[0].id)
