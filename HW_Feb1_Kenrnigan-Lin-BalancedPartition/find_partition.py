import random
from collections import defaultdict
from itertools import product


def read_col_file(filename):
    with open(filename, 'r') as file:
        vertices = set()
        edges = set()
        for line in file:
            line = line.strip()
            if line.startswith('c'):
                continue
            elif line.startswith('p'):
                tokens = line.split()
                n_vertices, n_edges = int(tokens[-2]), int(tokens[-1])
                vertices = set(range(1, n_vertices + 1))
            elif line.startswith('e'):
                tokens = line.split()
                edges.add((int(tokens[-2]), int(tokens[-1])))
        return vertices, edges


def get_random_partition(vertices):
    n = len(vertices)
    list_vertices = list(vertices)
    random.shuffle(list_vertices)
    return set(list_vertices[:int(n / 2)]), set(list_vertices[int(n / 2):])


def get_map_edges(src_edges):
    """Convert list representation of edges to map"""
    edges = defaultdict(set)
    for x, y in src_edges:
        edges[x].add(y)
        edges[y].add(x)
    return edges


def partition_weight(left, edges):
    return sum(sum((u not in left) for u in edges[v]) for v in left)


def one_nh(left, right, fixed_left=set(), fixed_right=set()):
    """Return list of all partitions in 1-neighbourhood"""

    res = []
    for v, u in product(left - fixed_left, right - fixed_right):
        left.remove(v)
        left.add(u)
        right.remove(u)
        right.add(v)

        res.append(((set(left), set(right)), (v, u)))

        left.remove(u)
        left.add(v)
        right.remove(v)
        right.add(u)
    return res


def min_in_one_nh(left, right, edges, fixed_left=set(), fixed_right=set()):
    return min((partition_weight(l, edges), (l, r), (v, u))
               for ((l, r), (v, u)) in one_nh(left, right, fixed_left, fixed_right))


def find_balanced_partition(graph):
    """Return: one part of the partition as a set and partition weight"""

    vertices, src_edges = graph
    left, right = get_random_partition(vertices)
    edges = get_map_edges(src_edges)
    weight = partition_weight(left, edges)

    weight_is_updated = True
    while weight_is_updated:
        weight_is_updated = False

        new_weight, (new_left, new_right), (v, u) = min_in_one_nh(left, right, edges)

        # if optimized within 1-neighbourhood
        if new_weight < weight:
            weight = new_weight
            left = new_left
            right = new_right
            weight_is_updated = True
            continue

        # try to optimize using consequence 1-neighbourhood optimization
        fixed_left = set()
        fixed_right = set()
        max_depth = len(new_left)
        for _ in range(max_depth - 1):
            cur_left = new_left
            cur_right = new_right
            fixed_left.add(u)
            fixed_right.add(v)

            new_weight, (new_left, new_right), (v, u) \
                = min_in_one_nh(cur_left, cur_right, edges, fixed_left, fixed_right)

            if new_weight < weight:
                weight = new_weight
                left = new_left
                right = new_right
                weight_is_updated = True
                break

        if weight_is_updated:
            continue
        else:
            return left, weight


path = "./res_feb_1/"
G = read_col_file(path + "myciel5.col")
print(G)
print(find_balanced_partition(G))