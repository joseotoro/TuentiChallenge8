def open_nodes(position, double_jumps, invalids, rows, cols):
    def is_valid(pos):
        return not pos in invalids and 0 <= pos[0] < rows and 0 <= pos[1] < cols

    possibles = set()

    if position in double_jumps:
        possibles.add((position[0] + 4, position[1] + 2))
        possibles.add((position[0] + 4, position[1] - 2))
        possibles.add((position[0] - 4, position[1] + 2))
        possibles.add((position[0] - 4, position[1] - 2))

        possibles.add((position[0] + 2, position[1] + 4))
        possibles.add((position[0] + 2, position[1] - 4))
        possibles.add((position[0] - 2, position[1] + 4))
        possibles.add((position[0] - 2, position[1] - 4))
    else:
        possibles.add((position[0] + 2, position[1] + 1))
        possibles.add((position[0] + 2, position[1] - 1))
        possibles.add((position[0] - 2, position[1] + 1))
        possibles.add((position[0] - 2, position[1] - 1))

        possibles.add((position[0] + 1, position[1] + 2))
        possibles.add((position[0] + 1, position[1] - 2))
        possibles.add((position[0] - 1, position[1] + 2))
        possibles.add((position[0] - 1, position[1] - 2))

    return filter(is_valid, possibles)

def bfs(source, destination, double_jumps, invalids, rows, cols):
    visited = set()
    actual = source

    nodes = map(lambda x: (x, 1), open_nodes(actual, double_jumps, invalids, rows, cols))
    solution = None

    while solution is None and len(nodes) > 0:
        node = nodes[0][0]
        node_cost = nodes[0][1]
        nodes = nodes[1:]

        visited.add(node)

        if node == destination:
            return node_cost

        new_nodes = open_nodes(node, double_jumps, invalids, rows, cols)
        for n in new_nodes:
            if n not in visited and n not in map(lambda x: x[0], nodes):
                nodes.append((n, node_cost + 1))

    return None

def solve(file_name):
    output_file_name = file_name.replace('Input', 'Output')

    with open(file_name, 'r') as file_in:
        lines = file_in.readlines()
        cases = int(lines[0])
        lines = lines[1:]

    with open(output_file_name, 'w') as file_out:
        for case in range(cases):
            rows, cols = map(int, lines[0].split())
            terrain = []
            source = princess = destination = None
            double_jumps = set()
            invalids = set()

            for i in range(rows):
                row = list(lines[i + 1].strip())

                if 'S' in row:
                    source = (i, row.index('S'))
                if 'P' in row:
                    princess = (i, row.index('P'))
                if 'D' in row:
                    destination = (i, row.index('D'))

                for c in [index for index, x in enumerate(row) if x == '*']:
                    double_jumps.add((i, c))

                for c in [index for index, x in enumerate(row) if x == '#']:
                    invalids.add((i, c))

                terrain.append(row)

            lines = lines[rows + 1:]

            source_to_princess = bfs(source, princess, double_jumps, invalids, rows, cols)
            princess_to_destination = None

            if source_to_princess is not None:
                princess_to_destination = bfs(princess, destination, double_jumps, invalids, rows, cols)

            if princess_to_destination is None:
                file_out.write('Case #{}: IMPOSSIBLE\n'.format(case + 1))
            else:
                file_out.write('Case #{}: {}\n'.format(case + 1, source_to_princess + princess_to_destination))


def solve_test():
    solve('testInput.txt')

def solve_submit():
    solve('submitInput.txt')

solve_submit()