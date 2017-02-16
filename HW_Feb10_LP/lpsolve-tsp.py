from itertools import combinations

from HW_Feb3_TSP_Playground.tcp_sandbox import read_tsp_instance, euclidean_distance

instance_filenames = ['dtest.tsp', 'd198.tsp', 'd493.tsp', 'd657.tsp', 'd2103.tsp', 'pr107.tsp', 'pr152.tsp', 'pr439.tsp']
path_to_instances = r'../HW_Feb3_TSP_Playground/res_feb_3/'


# 2D-coordinates of vertices as tuples
instance = read_tsp_instance(path_to_instances + instance_filenames[0])
n = len(instance)

program = ["/* Objective function */\n", "min: "]
for i, j in combinations(range(n), 2):
    program.append(" {0:.2f}".format(euclidean_distance(instance[i], instance[j])))
    program.append("x_{}_{}".format(i, j))
    program.append(" +")
program.pop()
program.append(";\n")

# print(program)
program.append("/* Variable bounds */\n")
for i in range(n):
    for j in range(n):
        if i == j:
            continue
        program.append("x_{}_{}".format(i, j))
        program.append(" + ")
    program.pop()
    program.append(" = 1;\n")

for i in range(n):
    for j in range(n):
        if i == j:
            continue
        program.append("x_{}_{}".format(j, i))
        program.append(" + ")
    program.pop()
    program.append(" = 1;\n")

for i in range(1, n):
    for j in range(1, n):
        if i == j:
            continue
        program.append("u_{0} - u_{1} + {2}x_{0}_{1} <= {3};\n".format(i, j, n - 1, n - 2))


program.append("\n/* Variables constraints */\n")
for i in range(n):
    for j in range(n):
        if i == j:
            continue
        program.append("0 <= x_{}_{} <= 1;\n".format(i, j))

for i in range(1, n):
    program.append("1 <= u_{} <= {};\n".format(i, n - 1))

# print("".join(program))

with open("tsp-{}.lp".format(instance_filenames[0]), "w") as f:
    f.write("".join(program))

# program.append("\n/* All variables are integers */\n")