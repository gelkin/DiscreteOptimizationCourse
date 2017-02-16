import time
import random
from itertools import combinations, chain
from math import sqrt

instance_filenames = ['d198.tsp', 'd493.tsp', 'd657.tsp', 'd2103.tsp', 'pr107.tsp', 'pr152.tsp', 'pr439.tsp']
path_to_instances = r'../HW_Feb3_TSP_Playground/res_feb_3/'


def read_tsp_instance(filename):
    with open(filename, 'r') as file:
        coordinates = []
        for line in file:
            line = line.strip().lower()
            if line.startswith('dimension'):
                coordinates = [(0, 0)] * int(line.split()[-1])
            tokens = line.split()
            if len(tokens) == 3 and tokens[0].isdecimal():
                tokens = line.split()
                coordinates[int(tokens[0]) - 1] = tuple(map(float, tokens[1:]))
        return coordinates


def euclidean_distance(point1, point2):
    return sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def calculate_tour_length(instance, permutation):
    n = len(permutation)
    return sum(euclidean_distance(instance[permutation[i]], instance[permutation[(i + 1) % n]]) for i in range(len(permutation)))


def solve_tsp(instance):
    # Your solution goes in here…
    # The return value is permutation
    return list(range(len(instance)))


def calc_dist_matrix(instance):
    n = len(instance)
    return [[euclidean_distance(instance[i], instance[j]) for j in range(n)] for i in range(n)]


def solve_tsp_nn(instance):
    dist_matrix = calc_dist_matrix(instance)

    start_v = random.randrange(0, len(instance))
    res = [start_v]
    not_visited = set(range(len(instance)))
    not_visited.remove(start_v)

    cur_v = start_v
    while not_visited:
        _, cur_v = min((dist_matrix[cur_v][v], v) for v in not_visited)
        not_visited.remove(cur_v)
        res.append(cur_v)
    return res


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
            options_for_edge = ((sum_dist(instance, x, y, v) + (perim - edge_w), (i + 1, v)) for v in not_visited)
            options = chain(options, options_for_edge)

        _, (pos, min_v) = min(options)
        res.insert(pos, min_v)
        not_visited.remove(min_v)
        # print(res)

    return res


# for filename in instance_filenames[2:3]:
#     instance = read_tsp_instance(path_to_instances + filename)
#     print('Solving instance {}…'.format(filename), end='')
#     time_start = time.monotonic()
#     permutation = solve_tsp_ni(instance)
#     time_elapsed = time.monotonic()-time_start
#     print(' done in {} seconds with tour length {}\n'.format(time_elapsed, calculate_tour_length(instance, permutation)))