from pathlib import Path


def entry_point(day, q1, q2):
    f_path = Path() / f"resources/day{day}.txt"
    with open(f_path) as f:
        if q1:
            print(q1(f))
            f.seek(0)
        if q2:
            print(q2(f))
