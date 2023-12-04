from adventofcode2023.util import entry_point

EXAMPLE = (l for l in """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45""".splitlines())


def parse_input(input):
    lines = []
    for line in input:
        lines.append(
            [int(x.strip()) for x in line.strip().split(" ")]
        )
    return lines


def extrapolate(line: list, right=True):
    lines = [line]
    while not all((x == 0 for x in lines[-1])):
        lines.append([b - a for a, b in zip(line[:-1], line[1:])])
        line = lines[-1]
    if right:
        lines[-1] += [0]
        edge_idx = -1
    else:
        lines[-1] = [0] + lines[-1]
        edge_idx = 0
    for i in range(len(lines) - 2, -1, -1):
        if right:
            lines[i] += [lines[i][edge_idx] + lines[i + 1][edge_idx]]
        else:
            lines[i] = [lines[i][edge_idx] - lines[i + 1][edge_idx]] + lines[i]
    return lines[0][edge_idx]


def q1(input):
    lines = parse_input(input)
    result = 0
    for line in lines:
        result += extrapolate(line)
    return result


def q2(input):
    lines = parse_input(input)
    result = 0
    for line in lines:
        result += extrapolate(line, right=False)
    return result


if __name__ == "__main__":
    # print(q2(EXAMPLE))
    entry_point(9, q1, q2)
