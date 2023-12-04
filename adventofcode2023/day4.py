from adventofcode2023.util import entry_point
from collections import defaultdict


def find_matches(numbers: str):
    winning, have = numbers.strip().split("|")
    winning = set(int(n.strip()) for n in winning.strip().split(" ") if n.strip())
    have = set(int(n.strip()) for n in have.strip().split(" ") if n.strip())
    return winning & have


def calculate_points(numbers: str):
    matches = find_matches(numbers)
    if not matches:
        return 0
    points = 2 ** (len(matches) - 1)
    return points


def q1(input):
    points = 0
    for line in input:
        card, numbers = line.strip().split(":")
        points += calculate_points(numbers)
    return points


def q2(input):
    card2amount = defaultdict(int)
    card2matches = {}
    for line in input:
        card, numbers = line.strip().split(":")
        card = int(card.strip().split(" ")[-1])
        card2matches[card] = card2matches.get(card, len(find_matches(numbers)))
        card2amount[card] = card2amount[card] + 1
        for i in range(card + 1, card + card2matches[card] + 1):
            card2amount[i] = card2amount[i] + card2amount[card]
    return sum(card2amount.values())


if __name__ == '__main__':
    entry_point(4, q1, q2)
