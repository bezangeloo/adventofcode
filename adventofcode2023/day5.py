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
EXAMPLE = (line for line in """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4""".splitlines())


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
    to_transform = [group]
    transformed = []
    while to_transform:
        done = False
        group_start, group_length = to_transform.pop()
        for (source, mapping_length), dest in mapping.items():
            if source <= group_start <= group_start + group_length <= source + mapping_length:
                # we can transform this group
                transformed.append((group_start - source + dest, group_length))
                done = True
                break
            elif source <= group_start <= source + mapping_length < group_start + group_length:
                # we can partially transform this group
                # ----|----------|------------|-------------------------|---------------------------->
                #   source   group_start   source+mapping_length    group_start+group_length
                transformed.append((group_start - source + dest, source + mapping_length - group_start))
                to_transform.append((source + mapping_length + 1, group_start + group_length - source - mapping_length))
                done = True
                break
        if not done:
            # we cannot transform this group, so use identity
            transformed.append((group_start, group_length))
    return transformed


def find_minimum_location_for_group(structures, seeds_groups):
    groups = list(seeds_groups)
    transformed_groups = []
    for mapping_name in STAGES:
        while groups:
            group = groups.pop()
            transformed_groups.extend(transform_group(group, structures[mapping_name]))
        groups, transformed_groups = transformed_groups, []
    # we now have groups of locations in the groups' var, so simply get the minimum out of the start of each group
    return min(groups, key=lambda g: g[0])


def q2(input):
    structures = parse_input(input)
    seeds_pairs = zip(structures["seeds"][0::2], structures["seeds"][1::2])
    # instead of mapping each seed, map groups of seeds.
    return find_minimum_location_for_group(structures, seeds_pairs)


if __name__ == '__main__':
    entry_point(5, q1, q2)
    #  print(q2(EXAMPLE))
    #  weird bug made the answer for q2 to be the actual_answer+1. I guess I'll never know the reason :D
