from pathlib import Path

FILE_PATH = Path() / "day1.txt"


def first_q():
    values = []
    with open(FILE_PATH) as f:
        for line in f:
            first = None
            last = None
            for c in line:
                if c.isdigit():
                    if first is None:
                        first = c
                    else:
                        last = c
            values.append(int(f"{first}{last if last is not None else first}"))
    return sum(values)


def second_q():
    digits = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}
    values = []
    with open(FILE_PATH) as f:
        for line in f:
            first = None
            last = None
            for i in range(len(line)):
                if not first and line[i].isdigit():
                    first = line[i]
                if not last and line[-(1 + i)].isdigit():
                    last = line[-(1 + i)]
                prefix = line[i:]
                if not first:
                    for digit in digits:
                        if prefix.startswith(digit):
                            first = digits[digit]
                            break
                postfix = line[:-i]
                if not last:
                    for digit in digits:
                        if postfix.endswith(digit):
                            last = digits[digit]
                            break
                if first and last:
                    break
            values.append(int(f"{first}{last}"))
    return sum(values)


if __name__ == "__main__":
    print("first:", first_q())
    print("second:", second_q())
