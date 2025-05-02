from heapq import heappop, heappush
from io import StringIO


def can_make_design(design, patterns):
    queue = []
    heappush(queue, (len(design), design))

    while len(queue) > 0:
        _, current = heappop(queue)

        if len(current) == 0:
            print("Yes:", design)
            return True

        possibles = filter(lambda p: current.startswith(p), patterns)
        for poss in possibles:
            new_design = current[len(poss) :]
            heappush(queue, (len(new_design), new_design))

    print("Nope:", design)
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
    if can_make_design(design, patterns):
        count += 1

print("Part 1:", count)

# 236 too low
