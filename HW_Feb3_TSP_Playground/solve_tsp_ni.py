from itertools import chain
from HW_Feb3_TSP_Playground.tcp_sandbox import euclidean_distance


def sum_of_sides(instance, figure):
    res = 0
    for i in range(len(figure)):
        x = figure[i]
        y = figure[(i + 1) % len(figure)]
        res += euclidean_distance(instance[x], instance[y])
    return res


def sum_dist(instance, x, y, v):
    return euclidean_distance(instance[x], instance[v]) + euclidean_distance(instance[y], instance[v])


def sum_dist_edge(instance, x, y, v):
    return sum_dist(instance, x, y, v) - euclidean_distance(instance[x], instance[y])


def solve_tsp_ni(instance):
    n = len(instance)
    _, start_triangle = min((sum_of_sides(instance, triangle), triangle) for triangle in combinations(range(n), 3))

    res = []
    res.extend(start_triangle)

    not_visited = set(range(len(instance))) - set(start_triangle)

    while not_visited:
        perim = sum_of_sides(instance, res)
        print("perim = {}".format(perim))
        options = []

        for i in range(len(res)):
            x = res[i]
            y = res[(i + 1) % len(res)]
            edge_w = euclidean_distance(instance[x], instance[y])

            # remove one edge and calc new perimeter with all possible vertices
            options_for_edge = [(sum_dist(instance, x, y, v) + (perim - edge_w), (i, v)) for v in not_visited]
            options = chain(options, options_for_edge)

        _, (pos, min_v) = min(options)
        res.insert(pos, min_v)
        not_visited.remove(min_v)
        print(res)

    return res