class Note:
    def __init__(self, start, length, speed, score):
        self.start = start / speed
        self.end = self.start + length / speed
        self.score = score


def binary_search(notes, start_index):
    lo = 0
    hi = start_index - 1

    while lo <= hi:
        mid = (lo + hi) // 2
        if notes[mid].end < notes[start_index].start:
            if notes[mid + 1].end < notes[start_index].start:
                lo = mid + 1
            else:
                return mid
        else:
            hi = mid - 1
    return -1


def schedule(notes):
    notes = sorted(notes, key=lambda n: n.end)

    n = len(notes)
    table = [0 for _ in range(n)]

    table[0] = notes[0].score

    for i in range(1, n):
        score = notes[i].score
        l = binary_search(notes, i)
        if l != -1:
            score += table[l]

        table[i] = max(score, table[i - 1])

    return table[n - 1]


def solve(file_name):
    output_file_name = file_name.replace('Input', 'Output')

    with open(file_name, 'r') as file_in:
        lines = file_in.readlines()
        cases = int(lines[0])
        lines = lines[1:]

    with open(output_file_name, 'w') as file_out:
        for case in range(cases):
            number_notes = int(lines[0])
            notes = []
            for i in range(number_notes):
                start, length, speed, score = map(int, lines[1 + i].split())
                notes.append(Note(start, length, speed, score))
            lines = lines[number_notes + 1:]

            # combine same time notes
            to_remove = set()
            for i in range(number_notes):
                for j in range(i + 1, number_notes):
                    if notes[i] not in to_remove and notes[j] not in to_remove:
                        if notes[i].start == notes[j].start and notes[i].end == notes[j].end:
                            to_remove.add(notes[j])
                            notes[i].score += notes[j].score

            for remove_note in to_remove:
                notes.remove(remove_note)

            solution = schedule(notes)
            print('case {}: {}'.format(case + 1, solution))

            file_out.write('Case #{}: {}\n'.format(case + 1, solution))


def solve_test():
    solve('testInput.txt')


def solve_submit():
    solve('submitInput.txt')


solve_submit()
