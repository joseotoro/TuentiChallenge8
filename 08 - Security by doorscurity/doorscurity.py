from fractions import gcd


def ext_gcd(a, b):
    v1 = [1, 0, a]
    v2 = [0, 1, b]

    if a > b:
        a, b = b, a
    while v1[2] > 0:
        q = v2[2] / v1[2]
        for i in range(0, len(v1)):
            v2[i] = v2[i] - q * v1[i]
        v1, v2 = v2, v1
    return v2[0], v2[1]


def chinese_remainder(a, m):
    n = len(a)

    a1 = a[0]
    m1 = m[0]

    for i in range(1, n):
        a2 = a[i]
        m2 = m[i]

        g = gcd(m1, m2)

        if a1 % g != a2 % g:
            return None

        p, q = ext_gcd(m1 / g, m2 / g)

        mod = m1 / g * m2
        x = (a1 * (m2 / g) % mod * q % mod + a2 * (m1 / g) % mod * p % mod) % mod

        a1 = x
        if a1 < 0:
            a1 += mod
        m1 = mod

    return a1


def solve(file_name):
    output_file_name = file_name.replace('Input', 'Output')

    with open(file_name, 'r') as file_in:
        lines = file_in.readlines()
        cases = int(lines[0])
        lines = lines[1:]

    with open(output_file_name, 'w') as file_out:
        for case in range(cases):
            number_doors = int(lines[0])

            n = []
            a = []
            for i in range(number_doors):
                p, t = map(int, lines[1 + i].split())
                n.append(p)
                a.append(- (t + i))

            lines = lines[1 + number_doors:]

            solution = chinese_remainder(a, n)

            if solution is None:
                file_out.write('Case #{}: NEVER\n'.format(case + 1))
            else:
                file_out.write('Case #{}: {}\n'.format(case + 1, solution))


def solve_test():
    solve('testInput.txt')


def solve_submit():
    solve('submitInput.txt')

solve_submit()
