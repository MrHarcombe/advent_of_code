from functools import cache
from io import StringIO


@cache
def can_match(design, patterns):
    if len(design) == 0:
        return True

    for pattern in patterns:
        if design.startswith(pattern):
            if can_match(design[len(pattern) :], patterns):
                return True

    return False


test = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""

# with StringIO(test) as input_data:
with open("input19.txt") as input_data:
    patterns = sorted(
        input_data.readline().strip().split(", "), key=lambda d: (-len(d), d)
    )
    input_data.readline()
    designs = input_data.read().strip().split("\n")

# print(patterns, designs)

count = 0
for design in designs:
    if can_match(design, tuple(patterns)):
        count += 1
        if count % 100 == 0:
            print("Count:", count)
    else:
        print("Nope:", design)
        # can_match(design, patterns)

print("Part 1:", count)

# 236 too low
