W = WHOLE_STEP = True
H = HALF_STEP = not WHOLE_STEP

MAJOR_SCALE = [W, W, H, W, W, W, H]
NATURAL_MINOR_SCALE = [W, H, W, W, H, W, W]

STEP = {
    'A' : 'A#',
    'A#' : 'B',
    'B' : 'C',
    'C' : 'C#',
    'C#' : 'D',
    'D' : 'D#',
    'D#' : 'E',
    'E' : 'F',
    'F' : 'F#',
    'F#' : 'G',
    'G' : 'G#',
    'G#' : 'A'
}

HALF_DOWN_EQ = {v : k for k, v, in STEP.items()}

ALL_NOTES = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
ALL_SCALES = list(map(lambda x: 'M' + x, ALL_NOTES)) + list(map(lambda x: 'm' + x, ALL_NOTES))

def convert_equivalent_note(note):
    if note.endswith('b'):
        return HALF_DOWN_EQ[note[0]]
    elif note not in STEP:
        return STEP[note[0]]
    else:
        return note


def gen_scale_set(note, scale):
    scale_set = set()

    for step_type in scale:
        if step_type == HALF_STEP:
            note = STEP[note]
        else:
            note = STEP[STEP[note]]
        scale_set.add((note,))

    return scale_set


def solve(file_name):
    output_file_name = file_name.replace('Input', 'Output')

    a = 'asd'
    a.endswith('b')

    # pre-compute scales
    major_scales = {x: gen_scale_set(x, MAJOR_SCALE) for x in ALL_NOTES}
    natural_minor_scales = {x: gen_scale_set(x, NATURAL_MINOR_SCALE) for x in ALL_NOTES}

    with open(file_name, 'r') as file_in:
        lines = file_in.readlines()
        cases = int(lines[0])
        lines = lines[1:]

    with open(output_file_name, 'w') as file_out:
        for case in range(cases):
            number_notes = int(lines[0])
            lines = lines[1:]

            if number_notes == 0:
                file_out.write('Case #{}: {}\n'.format(case + 1, ' '.join(ALL_SCALES)))
            else:
                notes = set(map(lambda x: (convert_equivalent_note(x),), lines[0].split()))
                lines = lines[1:]
                solution = []

                # major scales
                for note in ALL_NOTES:
                    if notes.issubset(major_scales[note]):
                        solution.append('M' + note)
                # minor scales
                for note in ALL_NOTES:
                    if notes.issubset(natural_minor_scales[note]):
                        solution.append('m' + note)

                if len(solution) == 0:
                    file_out.write('Case #{}: None\n'.format(case + 1))
                else:
                    file_out.write('Case #{}: {}\n'.format(case + 1, ' '.join(solution)))


def solve_test():
    solve('testInput.txt')

def solve_submit():
    solve('submitInput.txt')

solve_submit()