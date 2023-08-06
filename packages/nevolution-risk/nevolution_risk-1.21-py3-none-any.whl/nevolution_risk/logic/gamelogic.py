import networkx as nx

class GameLogic(object):

    def __init__(self):
        self.player_one = PlayerOne()
        self.player_two = PlayerTwo()

    def find_path(graph, start_node, end_node, path=[]):
        path = path + [start_node]
        if start_node == end_node:
            return path
        if start_node not in graph:
            return None
        for node in graph[start_node]:
            if node not in graph:
                new_path = find_path(graph, node, end_node, path)
                if new_path: 
                    return new_path
        return None

    def find_all_paths(graph, start_node, end_node, path=[]):
        path = path + [start_node]
        if start_node == end_node:
            return path
        if start_node not in graph:
            return []
        paths = []
        for node in graph[start_node]:
            if node not in graph:
                new_paths = find_all_paths(graph, node, end_node, path)
                for new_path in new_paths:
                    paths.append(new_path)
        return paths 

    def find_shortest_path(graph, start_node, end_node, path=[]):
        path = path + [start_node]
        if start_node == end_node:
            return path
        if start_node not in graph:
            return None
        shortest = None
        for node in graph[start_node]:
            if node not in graph:
                new_path = find_shortest_path(graph, node, end_node, path)
                if new_path:
                    if not shortest or len(new_path) < len(shortest):
                        shortest = new_path
        return shortest
    
    # sets the node attribute conquered to all nodes in the graph and returns the new graph
    def set_node_attribute_conquered(graph, node):
        for node in graph:
            nx.set_node_attributes(graph, 'conquered', 'false')
        return graph

    def set_player_one(graph, node_nbr, player):
        graph.node[node_nbr]['conquered'] = 'true'
        graph.node[node_nbr]['player'] = self.player_one ## not sure if this works

    def set_player_two(graph, node_nbr, player):
        graph.node[node_nbr]['conquered'] = 'true'
        graph.node[node_nbr]['player'] = self.player_two

    def move_to_next_node(graph, curr_node, end_node):
        list_of_path = find_shortest_path(graph, curr_node, end_node)
        for path in list_of_path:
            #TODO -- may need help on this one!
            # graph.neighbors(curr_node) returns a list of neighbors, this could be useful



class PlayerOne():

    def __init__(self):
        self.player_name = 'Hannah'
        self.player_color = 'red'
        self.player_troops = '0'

class PlayerTwo():

    def __init__(self):
        self.player_name = 'Anna'
        self.player_color = 'blue'
        self.player_troops = '0'
