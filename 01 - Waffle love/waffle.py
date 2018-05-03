def solve(file_name):
    output_file_name = file_name.replace('Input', 'Output')

    with open(file_name, 'r') as file_in:
        lines = file_in.readlines()
        cases = int(lines[0])
        lines = lines[1:]

    with open(output_file_name, 'w') as file_out:
        for case in range(cases):
            vertical, horizontal = map(int, lines[case].split())

            if vertical < 2 or horizontal < 2:
                solution = 0
            else:
                solution = (vertical - 1) * (horizontal - 1)

            file_out.write('Case #{}: {}\n'.format(case + 1, solution))


def solve_test():
    solve('testInput.txt')

def solve_submit():
    solve('submitInput.txt')

solve_submit()