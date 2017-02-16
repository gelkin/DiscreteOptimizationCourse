from collections import namedtuple
Row = namedtuple('Row', ['ID', 'weight', 'covered_columns'])

def read_instance_from_file(filename):
    rows = []
    cols = []
    with open(filename, 'r') as file:
        for line in file:
            tokens = list(map(int, line.strip().split()))
            if len(tokens) <= 2:
                cols = [[] for _ in range(tokens[0])]
                continue
            rows.append(Row(ID = len(rows), weight = tokens[0], covered_columns = set(tokens[2:])))
            for col in set(tokens[2:]):
                cols[col - 1].append(len(rows) - 1)
        return cols, rows

filename = "cover507.txt"
cols, rows = read_instance_from_file(r"./res_feb_10/" + filename)

# program = ["/* Objective function */\n", "min: "]
# for row in rows:
#     program.append("{}x_{}".format(row.weight, row.ID))
#     program.append(" + ")
# program.pop()
# program.append(";\n")
#
# program.append("\n/* Variable bounds */\n")
# for col in cols:
#     for set_ind in col:
#         program.append("x_{}".format(set_ind))
#         program.append(" + ")
#     program.pop()
#     program.append(" >= 1;\n")
#
# for row in rows:
#     program.append("0 <= x_{} <= 1;\n".format(row.ID))
#
# with open("setcover-{}.lp".format(filename), "w") as f:
#     f.write("".join(program))
#
# greedy
from itertools import chain

# Set union:
uncovered_columns = set(chain(*(r.covered_columns for r in rows)))

cover = set()
relevant_rows = set(r.ID for r in rows)

while uncovered_columns:
    # Choosing the row which minimized the “cost per column” quotient (see lecture)
    next_row = min(
        relevant_rows,
        key=lambda row_ID: rows[row_ID].weight / len(uncovered_columns & rows[row_ID].covered_columns)
    )
    cover.add(next_row)

    # Update relevant_rows to include only those that cover some uncovered columns
    uncovered_columns -= rows[next_row].covered_columns
    relevant_rows = set(filter(
        lambda row_ID: any(c in uncovered_columns for c in rows[row_ID].covered_columns),
        relevant_rows
    ))

print(sum(rows[r].weight for r in cover))
print(len(set(chain(*(rows[row_ID].covered_columns for row_ID in cover)))))