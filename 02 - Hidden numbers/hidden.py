def solve(file_name):
    output_file_name = file_name.replace('Input', 'Output')

    with open(file_name, 'r') as file_in:
        lines = file_in.readlines()
        cases = int(lines[0])
        lines = lines[1:]

    with open(output_file_name, 'w') as file_out:
        for case in range(cases):
            base = len(lines[case].strip())

            max_value = sum([x * base ** x for x in range(base - 1, 0, -1)])
            min_value = base ** (base - 1) + sum([(base - x - 1) * base ** x for x in range(base - 3, -1, -1)])

            solution = max_value - min_value
            file_out.write('Case #{}: {}\n'.format(case + 1, solution))

def solve_test():
    solve('testInput.txt')

def solve_submit():
    solve('submitInput.txt')

solve_submit()