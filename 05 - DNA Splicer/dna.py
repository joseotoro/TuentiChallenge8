from telnetlib import Telnet


def backtracking(p1, p2, idx, sequences):
    def aux(p_1, p_2, indexes):
        if len(p_1) > len(p_2):
            temp = p_1
            p_1 = p_2
            p_2 = temp

        for i, seq in enumerate(sequences):
            if i in indexes:
                continue

            p_1_new = p_1 + seq

            if p_1_new == p_2:
                indexes.append(i)
                indexes.sort()
                print(','.join(map(str, indexes)))
                return ','.join(map(lambda x: str(x + 1), indexes))

            elif p_1_new.startswith(p_2) or p_2.startswith(p_1_new):
                new_indexes = list(indexes)
                new_indexes.append(i)
                call = aux(p_1_new, p_2, new_indexes)
                if call is not None:
                    return call
        return None

    return aux(p1, p2, idx)


def main():
    tn = Telnet(host='52.49.91.111', port=3241)

    tn.read_until('\n')
    tn.read_until('\n')
    tn.write('SUBMIT\n')

    while True:
        print(tn.read_until('\n'))
        sequences = tn.read_until('\n').split()
        print(sequences)

        p_1 = p_2 = None
        solution = None

        for i, seq in enumerate(sequences):
            if solution is not None:
                break
            for j, seq2 in enumerate(sequences):
                if i >= j:
                    continue
                if seq.startswith(seq2) or seq2.startswith(seq):
                    p_1 = seq
                    p_2 = seq2

                    solution = backtracking(seq, seq2, [i, j], sequences)
                    if solution is not None:
                        break

        tn.write(solution + '\n')

main()
