from cvxpy import *
import numpy as np


def solve(file_name):
    output_file_name = file_name.replace('Input', 'Output')

    with open(file_name, 'r') as file_in:
        lines = file_in.readlines()
        cases = int(lines[0])
        lines = lines[1:]

    with open(output_file_name, 'w') as file_out:
        for case in range(cases):
            rows, cols, number_items = map(int, lines[0].split())

            X = Bool(cols)
            Y = Bool(rows)
            constraints = []

            for i in range(number_items):
                row, col = map(int, lines[1 + i].split())
                constraints.append(Y[row] + X[col] <= 1)

            lines = lines[1 + number_items:]

            objective = Maximize(sum_entries(X) + sum_entries(Y))
            prob = Problem(objective, constraints)

            solution = int(round(prob.solve()))

            print('Case #{}: {}'.format(case + 1, solution))
            file_out.write('Case #{}: {}\n'.format(case + 1, solution))


def solve_test():
    solve('testInput.txt')


def solve_submit():
    solve('submitInput.txt')


solve_submit()
