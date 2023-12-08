from collections import Counter
from functools import total_ordering

from adventofcode2023.util import entry_point


EXAMPLE = (line.strip() for line in """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""".splitlines())

CARD_SCORES = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10}
CARD_SCORES_Q2 = {"A": 14, "K": 13, "Q": 12, "J": 1, "T": 10}
_hand_tracker = set()


@total_ordering
class Hand:
    def __init__(self, hand: str):
        self.hand = hand
        self.counts = Counter(hand)

    def __eq__(self, other):
        if not isinstance(other, Hand):
            return False
        return self.hand == other.hand

    def __lt__(self, other):
        if not isinstance(other, Hand):
            raise TypeError("comparison only supported with other Hand")
        if self.get_score() < other.get_score():
            return True
        if self.get_score() > other.get_score():
            return False
        for card, other_card in zip(self.hand, other.hand):
            if card != other_card:
                return self.get_card_score(card) < self.get_card_score(other_card)
        return False

    def five_of_kind(self):
        return len(self.counts) == 1

    def four_of_kind(self):
        return len(self.counts) == 2 and set(self.counts.values()) == {4, 1}

    def full_house(self):
        return len(self.counts) == 2 and set(self.counts.values()) == {3, 2}

    def three_of_kind(self):
        return len(self.counts) == 3 and set(self.counts.values()) == {3, 1}

    def two_pairs(self):
        return len(self.counts) == 3 and set(self.counts.values()) == {2, 1}

    def one_pair(self):
        return len(self.counts) == 4 and set(self.counts.values()) == {2, 1}

    def high_card(self):
        return len(self.counts) == 5

    def get_score(self):
        """
        score a hend from 0 to 6 according to the strength
        """
        if self.five_of_kind():
            _hand_tracker.add(self.hand)
            return 6
        if self.four_of_kind():
            _hand_tracker.add(self.hand)
            return 5
        if self.full_house():
            _hand_tracker.add(self.hand)
            return 4
        if self.three_of_kind():
            _hand_tracker.add(self.hand)
            return 3
        if self.two_pairs():
            _hand_tracker.add(self.hand)
            return 2
        if self.one_pair():
            _hand_tracker.add(self.hand)
            return 1
        if self.high_card():
            _hand_tracker.add(self.hand)
            return 0
        raise Exception(f"{self.hand} has no score")

    def get_card_score(self, card):
        if card.isdigit():
            return int(card)
        return CARD_SCORES.get(card)


class HandWithJoker(Hand):
    def __init__(self, hand: str):
        super().__init__(hand)
        self.jokers_count = self.counts["J"]
        del self.counts["J"]
        max_count = 0
        max_key = None
        for key, count in self.counts.items():
            max_count = max(max_count, count)
            if count == max_count:
                max_key = key
        self.counts[max_key] = self.counts[max_key] + self.jokers_count

    def get_card_score(self, card):
        if card.isdigit():
            return int(card)
        return CARD_SCORES_Q2.get(card)


def parse_input(input):
    for line in input:
        hand, bid = line.strip().split(" ")
        hand = Hand(hand.strip())
        bid = int(bid.strip())
        yield hand, bid


def parse_input_q2(input):
    for line in input:
        hand, bid = line.strip().split(" ")
        hand = HandWithJoker(hand.strip())
        bid = int(bid.strip())
        yield hand, bid


def q1(input):
    sorted_hands = sorted(parse_input(input), key=lambda pair: pair[0])
    total_winnings = 0
    for i, (hand, bid) in enumerate(sorted_hands, start=1):
        total_winnings += i * bid
    return total_winnings


def q2(input):
    sorted_hands = sorted(parse_input_q2(input), key=lambda pair: pair[0])
    total_winnings = 0
    for i, (hand, bid) in enumerate(sorted_hands, start=1):
        total_winnings += i * bid
    return total_winnings


if __name__ == "__main__":
    entry_point(7, q1, q2)
