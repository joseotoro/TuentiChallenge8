def solve(file_name):
    output_file_name = file_name.replace('Input', 'Output')

    with open(file_name, 'r') as file_in:
        lines = file_in.readlines()
        cases = int(lines[0])
        lines = lines[1:]

    with open(output_file_name, 'w') as file_out:
        for case in range(cases):
            rows, cols, number_items = map(int, lines[0].split())
            items = []

            items_in_col = {i: set() for i in range(cols)}
            items_in_row = {i: set() for i in range(rows)}

            for i in range(number_items):
                row, col = map(int, lines[1 + i].split())
                item = (row, col)

                items_in_col[col].add(item)
                items_in_row[row].add(item)

                items.append(item)

            lines = lines[1 + number_items:]

            #if case != 3:
            #    continue

            #print(cols, rows, number_items)

            forbidden_rows = set()
            forbidden_cols = set()

            # Empty rows or cols
            solution = 0
            for i in range(rows):
                if len(items_in_row[i]) == 0:
                    solution += 1
                    forbidden_rows.add(i)

            for i in range(cols):
                if len(items_in_col[i]) == 0:
                    solution += 1
                    forbidden_cols.add(i)

            items.sort(key=lambda x: (min(len(items_in_row[x[0]]), len(items_in_col[x[1]])), len(items_in_row[x[0]]) + len(items_in_col[x[1]])))

            def search_dependencies(item, visited=set()):
                visited.add(item)
                for i in [x for x in items_in_row[item[0]] if x not in visited]:
                    search_dependencies(i)
                for i in [x for x in items_in_col[item[1]] if x not in visited]:
                    search_dependencies(i)

                return visited

            def aux(items, forbidden_rows, forbidden_cols, best=[-1], acum=0):
                #print(items, 'rows', forbidden_rows, 'cols', forbidden_cols, best, acum)
                count = 0
                while True:
                    if len(items) == 0:
                        return count

                    ideal = acum + count + cols - len(forbidden_cols) + rows - len(forbidden_rows)
                    best[0] = max(best[0], acum + count)

                    (row, col) = items[0]
                    items = items[1:]
                    c = r = 0

                    if best[0] >= ideal:
                        return count

                    if row not in forbidden_rows and col in forbidden_cols:
                        forbidden_rows.add(row)

                        for it in items_in_row[row]:
                            forbidden_cols.add(it[1])

                        count += 1
                    elif row in forbidden_rows and col not in forbidden_cols:
                        forbidden_cols.add(col)

                        for it in items_in_col[col]:
                            forbidden_rows.add(it[0])

                        count += 1
                    else:
                        if row not in forbidden_rows:
                            n_rows = set(forbidden_rows)
                            n_rows.add(row)

                            n_cols = set(forbidden_cols)
                            for it in items_in_row[row]:
                                n_cols.add(it[1])

                            r = aux(items, n_rows, n_cols, best, count + acum + 1)
                        if col not in forbidden_cols:
                            n_cols = set(forbidden_cols)
                            n_cols.add(col)

                            n_rows = set(forbidden_rows)
                            for it in items_in_col[col]:
                                n_rows.add(it[0])

                            c = aux(items, n_rows, n_cols, best, count + acum + 1)

                            if r != 0 or c != 0:
                                best[0] = max(best[0], count + 1 + max(c, r))
                                return count + 1 + max(r, c)

            while len(items) > 0:
                component = search_dependencies(items[0])
                fil = filter(lambda it: it in component, items)
                for it in fil:
                    items.remove(it)

                solution += aux(fil, forbidden_rows, forbidden_cols)

            print('Case #{}: {}'.format(case + 1, max(solution, max(rows, cols))))
            file_out.write('Case #{}: {}\n'.format(case + 1, max(solution, max(rows, cols))))


def solve_test():
    solve('testInput.txt')


def solve_submit():
    solve('submitInput.txt')


solve_test()
