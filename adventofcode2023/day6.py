from adventofcode2023.util import entry_point


def parse_input_line(line):
    return (int(x.strip())
            for x in line.strip().split(":")[1].strip().split(" ")
            if x.strip())


def parse_input(input):
    times = parse_input_line(next(input))
    distances = parse_input_line(next(input))
    return ({
        "time": t,
        "distance": d
    } for t,d in zip(times, distances))


def q1(input):
    races = parse_input(input)
    beat_it_multiply = 0
    for race in races:
        beat_it_possibilities = 0
        race_time = race["time"]
        race_distance = race["distance"]
        for speed in range(1, race_time):
            travel_time = race_time - speed
            distance = speed * travel_time
            if distance > race_distance:
                beat_it_possibilities += 1
        if beat_it_multiply == 0:
            beat_it_multiply = beat_it_possibilities
        else:
            beat_it_multiply *= beat_it_possibilities
    return beat_it_multiply


def parse_input_line_q2(line):
    return int("".join(line.strip().split(":")[1].strip().split(" ")))


def parse_input_q2(input):
    time = parse_input_line_q2(next(input))
    distance = parse_input_line_q2(next(input))
    return time, distance


def q2(input):
    race_time, race_distance = parse_input_q2(input)
    beat_it_possibilities = 0
    for speed in range(1, race_time):
        travel_time = race_time - speed
        distance = speed * travel_time
        if distance > race_distance:
            beat_it_possibilities += 1
    return beat_it_possibilities


if __name__ == "__main__":
    entry_point(6, q1, q2)