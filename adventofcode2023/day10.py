from math import inf

from adventofcode2023.util import entry_point

DIRECTIONS = {
    "|": lambda i, j: ((i + 1, j), (i - 1, j)),
    "-": lambda i, j: ((i, j + 1), (i, j - 1)),
    "L": lambda i, j: ((i - 1, j), (i, j + 1)),
    "J": lambda i, j: ((i - 1, j), (i, j - 1)),
    "7": lambda i, j: ((i + 1, j), (i, j - 1)),
    "F": lambda i, j: ((i + 1, j), (i, j + 1)),
    ".": lambda i, j: ((None, None), (None, None)),
    "S": lambda i, j: ((None, None), (None, None))
}
EXAMPLE = (line.strip() for line in """..F7.
.FJ|.
SJ.L7
|F--J
LJ...""".splitlines())


def compute_steps(grid, start, tile, tile_to_step):
    steps = 1
    while tile != start:
        tile_to_step[tile] = steps
        steps += 1
        i, j = tile
        tile = [
            (_i, _j)
            for (_i, _j) in DIRECTIONS[grid[i][j]](i, j)
            if (_i, _j) not in tile_to_step or ((_i, _j) == start and len(tile_to_step) > 2)
        ].pop()


def parse_input(input):
    grid = []
    start = None
    for i, line in enumerate(input):
        grid.append(line.strip())
        if not start:
            j = grid[-1].find("S")
            if j != -1:
                start = (i, j)
    return start, grid


def q1(input):
    start, grid = parse_input(input)
    (i_start, j_start) = start
    # look for all connected tiles, should be two out of the possible 4
    connected_tiles = []
    lines = len(grid)
    line_len = len(grid[0])
    for i, j in (i_start - 1, j_start), (i_start, j_start + 1), (i_start + 1, j_start), (i_start, j_start - 1):
            if 0 <= i < lines and 0 <= j < line_len:
                if start in DIRECTIONS[grid[i][j]](i, j):
                    connected_tiles.append((i, j))
    # for each of them, find steps for all unknown tiles
    first_tile_to_step = {start: 0}
    compute_steps(grid, start, connected_tiles.pop(), first_tile_to_step)
    second_tile_to_step = {start: 0}
    compute_steps(grid, start, connected_tiles.pop(), second_tile_to_step)
    tiles_in_pipe = set(first_tile_to_step.keys()) | set(second_tile_to_step.keys())
    tile_to_step = {}
    for tile in tiles_in_pipe:
        tile_to_step[tile] = min(first_tile_to_step[tile] if tile in first_tile_to_step else inf,
                                 second_tile_to_step[tile] if tile in second_tile_to_step else inf)
    return max(tile_to_step.values())


def q2(input):
    pass


if __name__ == "__main__":
    # print(q1(EXAMPLE))
    entry_point(10, q1, q2)
