from adventofcode2023.util import entry_point
from collections import deque, defaultdict
from itertools import chain

EXAMPLE = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""


def q1(input):
    three_lines = deque([None, next(input).strip()], maxlen=3)
    line_len = len(three_lines[1])
    part_numbers = []
    current_number = []
    near_symbol = False
    for next_line in chain(input, [None]):
        three_lines.append(next_line.strip() if next_line else next_line)
        middle = three_lines[1]
        for i in range(line_len):
            if middle[i].isdigit():
                current_number.append(middle[i])
                if not near_symbol:
                    # check if near symbol
                    for line in three_lines:
                        if not line:
                            continue
                        for char_idx in i-1, i, i+1:
                            if line_len > char_idx >= 0:
                                if char_near_symbol(char_idx, line):
                                    near_symbol = True
                                    break
                        if near_symbol:
                            break
            else:
                if near_symbol:
                    part_numbers.append(int("".join(current_number)))
                current_number = []
                near_symbol = False
    return sum(part_numbers)


def char_near_symbol(char_idx, line):
    return not line[char_idx].isdigit() and line[char_idx] != "."


def char_near_asterisk(char_idx, line):
    return line[char_idx] == "*"


def q2(input):
    three_lines = deque([None, next(input).strip()], maxlen=3)
    line_len = len(three_lines[1])
    current_number = []
    near_asterisk = set()
    possible_gears = defaultdict(list)
    for next_line in chain(input, [None]):
        three_lines.append(next_line.strip() if next_line else next_line)
        middle = three_lines[1]
        for i in range(line_len):
            if middle[i].isdigit():
                current_number.append(middle[i])
                # check if near symbol
                for line in three_lines:
                    if not line:
                        continue
                    for char_idx in i-1, i, i+1:
                        if line_len > char_idx >= 0:
                            if char_near_asterisk(char_idx, line):
                                near_asterisk.add((char_idx, line))
            else:
                for asterisk in near_asterisk:
                    possible_gears[asterisk].append(int("".join(current_number)))
                current_number = []
                near_asterisk = set()
    gears_sum = 0
    for parts in possible_gears.values():
        if len(parts) == 2:
            gears_sum += parts[0] * parts[1]
    return gears_sum


if __name__ == '__main__':
    entry_point(3, q1, q2)
