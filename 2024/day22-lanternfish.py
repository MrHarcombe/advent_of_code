from collections import defaultdict
from io import StringIO
from math import floor


def mix(number, secret):
    return number ^ secret


def prune(secret):
    return secret % 16777216


test = """1
10
100
2024"""

test = """1
2
3
2024"""

# test = """2021
# 5017
# 19751"""

# test = """5053
# 10083
# 11263"""

# test = """123"""

total = 0
runs = []
changes = []
# with StringIO(test) as input_data:
with open("input22.txt") as input_data:
    for line in input_data:
        run = []
        change = []

        secret = int(line.strip())
        run.append(secret % 10)

        for j in range(2000):
            secret = prune(mix(secret * 64, secret))
            secret = prune(mix(floor(secret / 32), secret))
            secret = prune(mix(secret * 2048, secret))
            run.append(secret % 10)
            change.append((secret % 10) - run[-2])

        # print(f"{i + 1}:", secret)
        total += secret
        runs.append(run)
        changes.append(change)

print("Part 1:", total)

slice_scores = defaultdict(lambda: [None] * len(runs))
for i, change in enumerate(changes):
    for j in range(len(change)):
        slice = tuple(change[j : j + 4])
        if len(slice) == 4 and slice_scores[slice][i] is None:
            slice_scores[slice][i] = runs[i][j + 4]

print(
    "Part 2:",
    sum(
        n
        for n in max(
            slice_scores.values(), key=lambda i: sum(n for n in i if n is not None)
        )
        if n is not None
    ),
)
