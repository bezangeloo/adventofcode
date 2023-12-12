from collections import defaultdict
from math import inf
from pprint import pprint

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
PRINTER = {
    "|": "┃",
    "-": "━",
    "L": "┗",
    "J": "┛",
    "7": "┓",
    "F": "┏",
    ".": ".",
    "S": "S",
}
EXAMPLE = (line.strip() for line in """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...""".splitlines())


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
    # to check if a point is inside a shape we can draw a line starting at the point and extending to "infinity".
    # if the line crossed the sape odd times, the point is inside the shape.
    # we can treat our enclosed pipe loop as a border of a shape. yay

    # get the shape border:
    start, grid = parse_input(input)
    (i_start, j_start) = start
    connected_tiles = []
    lines = len(grid)
    line_len = len(grid[0])
    for i, j in (i_start - 1, j_start), (i_start, j_start + 1), (i_start + 1, j_start), (i_start, j_start - 1):
        if 0 <= i < lines and 0 <= j < line_len:
            if start in DIRECTIONS[grid[i][j]](i, j):
                connected_tiles.append((i, j))
    shape = get_pipe_loop(grid, start, connected_tiles.pop())
    print_shape(shape)
    area_in_shape = 0
    # for each tile that is not part of the shap, but only after we encountered the shape,
    # check how many times we cross the shape if we "draw" a line from it to the right edge
    for i in range(lines):
        start_checking = False
        point_to_crosses = {}
        for j in range(line_len):
            if (i, j) in shape:
                start_checking = True
                for k in point_to_crosses:
                    point_to_crosses[k] += 1
                continue
            if not start_checking:
                continue
            point_to_crosses[(i, j)] = 0
        area_in_shape += sum((1
                              for point in point_to_crosses
                              if point_to_crosses[point] % 2 #== 0
                              # and point_to_crosses[point] > 0
                              ))
    return area_in_shape


def print_shape(shape):
    grid = defaultdict(lambda: defaultdict(lambda: "."))
    max_i = 0
    max_j = 0
    for (i, j), tile in shape.items():
        grid[i][j] = tile
        max_i = max(i, max_i)
        max_j = max(j, max_j)
    for i in range(max_i + 5):
        line = []
        for j in range(max_j + 5):
            line.append(grid[i][j])
        print("".join(line))


def get_pipe_loop(grid, start, tile):
    parts = {start: "S"}
    while tile != start:
        i, j = tile
        parts[tile] = PRINTER[grid[i][j]]
        tile = [
            (_i, _j)
            for (_i, _j) in DIRECTIONS[grid[i][j]](i, j)
            if (_i, _j) not in parts or ((_i, _j) == start and len(parts) > 2)
        ].pop()
    return parts


if __name__ == "__main__":
    print(q2(EXAMPLE))
    # entry_point(10, q1, q2)
