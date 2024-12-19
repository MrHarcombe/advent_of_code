from io import StringIO


def can_match(design, patterns):
    if len(design) == 0:
        return True

    pidx = 0
    while pidx < len(patterns):
        pattern = patterns[pidx]
        if design.startswith(pattern):
            if can_match(design[len(pattern) :], list(patterns)):
                return True
            elif can_match(
                design,
                list(filter(lambda p: p[0] == pattern[0] and p != pattern, patterns)),
            ):
                return True

        pidx += 1

        print(design, pidx, pattern, len(patterns))

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
    if can_match(design, list(patterns)):
        count += 1
        if count % 100 == 0:
            print("Count:", count)
    else:
        print("Nope:", design)
        # can_match(design, patterns)

print("Part 1:", count)

# 236 too low
