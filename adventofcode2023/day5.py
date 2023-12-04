from itertools import chain
from math import inf

from adventofcode2023.util import entry_point

STAGES = ["seed-to-soil",
          "soil-to-fertilizer",
          "fertilizer-to-water",
          "water-to-light",
          "light-to-temperature",
          "temperature-to-humidity",
          "humidity-to-location"]


def parse_input(input):
    result = {"seeds": [int(seed) for seed in next(input).strip().split(":")[1].strip().split(" ")]}
    map_name = None
    for line in input:
        if not line.strip():
            map_name = None
            continue
        if ":" in line:
            # line should look like "a-to-b map:"
            map_name = line.strip().split(" ")[0]
            result[map_name] = {}
            continue
        if map_name:
            # dest source length
            dest, source, length = line.strip().split(" ")
            result[map_name][(int(source), int(length))] = int(dest)
    return result


def transform(value, mapping: dict):
    for (source, length), dest in mapping.items():
        if source <= value <= source + length:
            return value - source + dest
    return value


def find_minimum_location(structures, seeds_supplier):
    min_location = inf
    for seed in seeds_supplier:
        value = seed
        for mapping_name in STAGES:
            value = transform(value, structures[mapping_name])
        min_location = min(min_location, value)
    return min_location


def q1(input):
    structures = parse_input(input)
    return find_minimum_location(structures, structures["seeds"])


def seed_generator(seed_and_length):
    seed, length = seed_and_length
    start, end = seed, seed + length
    while start < end:
        yield start
        start += 1


def q2_that_runs_forever(input):
    """
    so that didn't work, after looking at the actual amount of seeds for this q it is obvious why.
    new plan - map the seeds in groups in q2
    """
    structures = parse_input(input)
    seeds_pairs = zip(structures["seeds"][0::2], structures["seeds"][1::2])
    seeds_supplier = chain(*(seed_generator(seeds_pair) for seeds_pair in seeds_pairs))
    return find_minimum_location(structures, seeds_supplier)


def transform_group(group, mapping: dict):
    group_start, group_length = group
    for (source, length), dest in mapping.items():
        if source <= group_start <= source + length:
            # we can transform this group, at least partially
            if group_start +
            return value - source + dest
    return value


def find_minimum_location_for_group(structures, seeds_supplier):
    min_location = inf
    for seed in seeds_supplier:
        value = seed
        for mapping_name in STAGES:
            value = transform(value, structures[mapping_name])
        min_location = min(min_location, value)
    return min_location


def q2(input):
    structures = parse_input(input)
    seeds_pairs = zip(structures["seeds"][0::2], structures["seeds"][1::2])
    # instead of mapping each seed, map groups of seeds.


if __name__ == '__main__':
    entry_point(5, q1, q2)
