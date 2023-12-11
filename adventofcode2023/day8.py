from collections import defaultdict
from math import gcd

from adventofcode2023.util import entry_point


EXAMPLE = (line for line in """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX""".splitlines())


def instruction_supplier(instructions):
    while True:
        for instruction in instructions:
            yield instruction


def parse_input(input):
    instructions = next(input).strip()
    nodes = {}
    a_nodes = []
    for line in input:
        if not line.strip():
            continue
        node, lr = (x.strip() for x in line.strip().split("="))
        l, r = (x.strip() for x in lr[1:-1].split(","))
        nodes[node] = {"L": l, "R": r}
        if node.endswith("A"):
            a_nodes.append(node)
    return instruction_supplier(instructions), nodes, a_nodes


def q1(input):
    instructions, nodes, _ = parse_input(input)
    node = "AAA"
    steps = 0
    while node != "ZZZ":
        node = nodes[node][next(instructions)]
        steps += 1
    return steps


def lcm(x, y):
    return (x * y) // gcd(x, y)


def set_lcm(s: list):
    _lcm = 1
    while s:
        _lcm = lcm(_lcm, s.pop())
    return _lcm


def get_sights_lcm(z_sights):
    sights = []
    for n in z_sights.values():
        for x in n.values():
            for y in x:
                sights.append(y)
    return set_lcm(sights)


def q2(input):
    instructions, nodes, a_nodes = parse_input(input)
    current_nodes = a_nodes
    steps = 0
    z_sights = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    enough_sights = 100  # arbitrary amount, just guess this is enough to see all nodes fall on "**Z"
    while enough_sights:
        instruction = next(instructions)
        current_nodes = [nodes[node][instruction] for node in current_nodes]
        steps += 1
        for a_node, node in zip(a_nodes, current_nodes):
            if node.endswith("Z"):
                if not z_sights[a_node][node]:
                    z_sights[a_node][node][steps] += 1
                else:
                    for s in z_sights[a_node][node]:
                        if steps % s == 0:
                            z_sights[a_node][node][s] += 1
                enough_sights -= 1
    return get_sights_lcm(z_sights)


if __name__ == "__main__":
    entry_point(8, q1, q2)