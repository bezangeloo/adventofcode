import functools
from pathlib import Path


MAX = {"red": 12,
       "green": 13,
       "blue": 14}


def get_handful_result(handful: str):
    res = {}
    for color_pair in handful.strip().split(","):
        amount, color = color_pair.strip().split(" ")
        res[color] = int(amount)
    return res


def is_game_possible(game: str):
    colon_idx = game.find(":")
    left, right = game[:colon_idx], game[colon_idx + 2:]
    game_id = int(left[left.rfind(" ") + 1:])
    for handful in right.strip().split(";"):
        for color, amount in get_handful_result(handful).items():
            if amount > MAX[color]:
                return game_id, False
    return game_id, True


def q1(input):
    """
    Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    .
    .
    .
    Determine which games would have been possible if the bag had been loaded with only
    12 red cubes, 13 green cubes, and 14 blue cubes. What is the sum of the IDs of those games?
    """
    sum_of_possible_games = 0
    for line in input:
        game_id, possible = is_game_possible(line)
        if possible:
            sum_of_possible_games += game_id
    return sum_of_possible_games


def get_minimum(game: str):
    colon_idx = game.find(":")
    right = game[colon_idx + 2:]
    minimum = {"red": 0, "green": 0, "blue": 0}
    for handful in right.strip().split(";"):
        for color, amount in get_handful_result(handful).items():
            minimum[color] = max(minimum[color], amount)
    return minimum


def q2(input):
    """
    The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together.
    The power of the minimum set of cubes in game 1 is 48. In games 2-5 it was 12, 1560, 630, and 36, respectively.
    Adding up these five powers produces the sum 2286.
    For each game, find the minimum set of cubes that must have been present.
    What is the sum of the power of these sets?
    """
    sum_of_powers = 0
    for line in input:
        minimum = get_minimum(line)
        sum_of_powers += functools.reduce(lambda a, b: a if b == 0 else (b if a == 0 else a * b), minimum.values())
    return sum_of_powers


if __name__ == '__main__':
    f_path = Path() / "day2.txt"
    with open(f_path) as f:
        print(q1(f))
        f.seek(0)
        print(q2(f))
