from collections import defaultdict
from collections import namedtuple
from itertools import islice
from math import inf
from shutil import Error

ArcInfo = namedtuple('ArcInfo', ['from_node', 'to_node', 'capacity', 'cost'])
EdgeInfo = namedtuple('EdgeInfo', ['cost', 'capacity'])


def getSpeed(category):
    if str(category).startswith('1'):
        return 1.0
    if str(category).startswith('2'):
        return 0.8
    if str(category).startswith('3'):
        return 0.6
    if str(category).startswith('4'):
        return 0.4
    raise Error('Unknown road category: {}'.format(category))

def read_instance_from_file(filename, max_arcs = None):
    with open(filename, 'r') as file:
        arcs = dict()
        nodes = set()
        graph = defaultdict(dict)
        contents = file.read().strip().split('\n')
        if max_arcs:
            contents = contents[:2*max_arcs]
        for node_pair, arc_info in zip(islice(contents, 0, None, 2), islice(contents, 1, None, 2)):
            u, v = map(int, node_pair.strip().split())
            nodes.update([u, v])
            travel_time, distance, category = map(float, arc_info.strip().split())
            capacity = int(10*getSpeed(category))
            cost = int(travel_time)
            arcs[(u, v)] = ArcInfo(from_node = u, to_node = v, capacity = capacity, cost = cost )
            arcs[(v, u)] = ArcInfo(from_node = v, to_node = u, capacity = capacity, cost = cost )

            graph[u][v] = EdgeInfo(cost, capacity)
            graph[v][u] = EdgeInfo(cost, capacity)

        return nodes, arcs, graph

#
# def test_using_networkx(nodes, arcs, source_node, target_node, demanded_flow_value):
#     import networkx as nx
#     nxgraph = nx.DiGraph()
#     nxgraph.add_nodes_from((n, {'demand': 0}) for n in nodes)
#     nxgraph.add_edges_from((e[0], e[1], {'capacity': int(arcs[e].capacity), 'weight': arcs[e].cost}) for e in arcs)
#
#     nxgraph.node[source_node]['demand'] = demanded_flow_value
#     nxgraph.node[target_node]['demand'] = -demanded_flow_value
#     mcf = nx.min_cost_flow(nxgraph)
#     print('NetworkX min-cost-flow algorithm succeeded. Here is the flow:')
#
#     from collections import defaultdict
#     d = defaultdict(int)
#
#     for n1 in mcf:
#         if mcf[n1]:
#             for n2 in mcf[n1]:
#                 if mcf[n1][n2] > 0:
#                     print('\tArc from node {} to node {} carries {} units of flow'.format(n1, n2, mcf[n1][n2]))
#     print('Total cost of flow: {}'.format(nx.cost_of_flow(nxgraph, mcf)))


benchmark_filename = r'./res_feb_15/mincostflow-input.txt'
nodes, arcs, graph = read_instance_from_file(benchmark_filename, 100)


def my_min_cost_flow(nodes, graph, source_node, target_node, demanded_flow_value):
    total_cost = 0
    while demanded_flow_value > 0:
        path = get_min_cost_path(nodes, graph, source_node, target_node)
        flow_value = min_flow_on_path(graph, path, demanded_flow_value)
        total_cost += flow_cost_on_path(graph, path, flow_value)
        remove_path_graph(graph, path, flow_value)
        demanded_flow_value -= flow_value
    return total_cost


def get_min_cost_path(nodes, graph, source_node, target_node):
    dists = [inf for _ in nodes]  # distances from source_node to all others
    dists[source_node] = 0
    prev = [-1 for _ in nodes]
    q = set(nodes)
    while q:
        _, u = min((dists[u], u) for u in q)
        q.remove(u)
        for to, (cost, cap) in graph[u].items():
            if dists[u] + cost < dists[to]:
                dists[to] = dists[u] + cost
                prev[to] = u

    res = [target_node]
    el = prev[target_node]
    while el != -1:
        res.append(el)
        el = prev[el]
    return list(reversed(res))


def min_flow_on_path(graph, path, demanded_flow_value):
    max_possible_flow = inf
    for u, v in zip(path, path[1:]):
        max_possible_flow = min(max_possible_flow, graph[u][v].capacity)

    return min(max_possible_flow, demanded_flow_value)


def flow_cost_on_path(graph, path, flow_value):
    total_cost = 0
    for u, v in zip(path, path[1:]):
        total_cost += graph[u][v].cost * flow_value
    return total_cost


def remove_path_graph(graph, path, flow_value):
    """ Update graph according to flow value added on path. """
    for u, v in zip(path, path[1:]):
        cost, capacity = graph[u][v]
        if capacity > flow_value:
            graph[u][v] = cost, capacity - flow_value
        elif capacity == flow_value:
            del graph[u][v]

x = my_min_cost_flow(nodes, graph, 4, 9, 11)
print(x)











