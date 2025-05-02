from collections import defaultdict
from io import StringIO
from itertools import permutations

test = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""


def check_on_roof(pos, roof_length, roof_width):
    return 0 <= pos[0] <= roof_width and 0 <= pos[1] <= roof_length


antenna = defaultdict(list)

# with StringIO(test) as input_data:
with open("input8.txt") as input_data:
    for y, line in enumerate(input_data):
        for x, ch in enumerate(line.strip()):
            if ch != ".":
                antenna[ch].append((x, y))

roof_length = y
roof_width = x

antinode_locations = set()

for dish in antenna:
    pairs = permutations(antenna[dish], 2)
    for p1, p2 in pairs:
        x1, y1 = p1
        x2, y2 = p2

        # calculate equation of line
        m = (y2 - y1) / (x2 - x1)
        # c = y1 - m * x1

        # calculate points either side, same distance away
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)

        if m > 0:
            a1 = (min(x1, x2) - dx, min(y1, y2) - dy)
            a2 = (max(x1, x2) + dx, max(y1, y2) + dy)
        else:
            a1 = (min(x1, x2) - dx, max(y1, y2) + dy)
            a2 = (max(x1, x2) + dx, min(y1, y2) - dy)

        if check_on_roof(a1, roof_length, roof_width):
            antinode_locations.add(a1)
        if check_on_roof(a2, roof_length, roof_width):
            antinode_locations.add(a2)

print("Part 1:", len(antinode_locations))
