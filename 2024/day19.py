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


@cache
def count_match(design, patterns):
    if len(design) == 0:
        return 1

    count = 0
    for pattern in patterns:
        if design.startswith(pattern):
            count += count_match(design[len(pattern) :], patterns)

    return count


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

count1 = 0
count2 = 0
for design in designs:
    if can_match(design, tuple(patterns)):
        count1 += 1

    count2 += count_match(design, tuple(patterns))
    # print(design, count2)

print("Part 1:", count1)
print("Part 2:", count2)

# 236 too low

# 719 too low
