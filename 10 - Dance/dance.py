MEMO = {}


def transform(dancers, src, dst):
    if src > dst:
        temp = src
        src = dst
        dst = temp

    right_idx = []
    for i in dancers:
        if src < i < dst:
            right_idx.append(i)

    left_idx = []
    for i in dancers:
        if i != src and i != dst and i not in right_idx:
            left_idx.append(i)

    return left_idx, right_idx


def divide_and_conquer(dancers, grudges):
    size = len(dancers)
    if size == 0:
        return 1
    elif size < 2:
        return 0
    elif size == 2:
        if not dancers[1] in grudges[dancers[0]]:
            return 1
        else:
            return 0

    h = tuple(dancers)
    if h in MEMO:
        return MEMO[h]

    dancer = dancers[0]

    total = 0
    for i in dancers:
        if i == dancer:
            continue
        if i not in grudges[dancer]:
            left_dancers, right_dancers = transform(dancers, dancer, i)

            if len(left_dancers) <= len(right_dancers):
                first = left_dancers
                second = right_dancers
            else:
                first = right_dancers
                second = left_dancers

            first_sol = divide_and_conquer(first, grudges)

            if first_sol != 0:
                second_sol = divide_and_conquer(second, grudges)
                total += first_sol * second_sol

    MEMO[h] = total
    return total


def solve(file_name):
    output_file_name = file_name.replace('Input', 'Output')

    with open(file_name, 'r') as file_in:
        lines = file_in.readlines()
        cases = int(lines[0])
        lines = lines[1:]

    with open(output_file_name, 'w') as file_out:
        for case in range(cases):
            MEMO.clear()
            number_dancers, number_grudges = map(int, lines[0].split())
            grudges = {x: set() for x in range(number_dancers)}

            for i in range(number_grudges):
                dancer_a, dancer_b = map(int, lines[i + 1].split())
                grudges[dancer_a].add(dancer_b)
                grudges[dancer_b].add(dancer_a)

            lines = lines[1 + number_grudges:]

            solution = divide_and_conquer(list(range(number_dancers)), grudges) % (10 ** 9 + 7)

            print('Case #{}: {}'.format(case + 1, solution))
            file_out.write('Case #{}: {}\n'.format(case + 1, solution))


def solve_test():
    solve('testInput.txt')


def solve_submit():
    solve('submitInput.txt')


solve_submit()
