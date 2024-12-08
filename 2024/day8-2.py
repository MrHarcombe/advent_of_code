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

test = """T.........
...T......
.T........
..........
..........
..........
..........
..........
..........
.........."""


def check_on_roof(pos, roof_length, roof_width):
    return 0 <= pos[0] <= roof_width and 0 <= pos[1] <= roof_length


def display_antinodes(antinodes, roof_length, roof_width):
    print(antinodes)
    for y in range(roof_length + 1):
        row = ["#" if (x, y) in antinodes else "." for x in range(roof_width + 1)]
        print("".join(row))
    print()


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
            antinode_locations.add((min(x1, x2), min(y1, y2)))
            antinode_locations.add((max(x1, x2), max(y1, y2)))

            a1x = min(x1, x2) - dx
            a1y = min(y1, y2) - dy

            a2x = max(x1, x2) + dx
            a2y = max(y1, y2) + dy

            a1 = (a1x, a1y)
            a2 = (a2x, a2y)

            while check_on_roof(a1, roof_length, roof_width):
                antinode_locations.add(a1)
                a1x -= dx
                a1y -= dy
                a1 = (a1x, a1y)

            while check_on_roof(a2, roof_length, roof_width):
                antinode_locations.add(a2)
                a2x += dx
                a2y += dy
                a2 = (a2x, a2y)

        else:
            antinode_locations.add((min(x1, x2), max(y1, y2)))
            antinode_locations.add((max(x1, x2), min(y1, y2)))

            a1x = min(x1, x2) - dx
            a1y = max(y1, y2) + dy

            a2x = max(x1, x2) + dx
            a2y = min(y1, y2) - dy

            a1 = (a1x, a1y)
            a2 = (a2x, a2y)

            while check_on_roof(a1, roof_length, roof_width):
                antinode_locations.add(a1)
                a1x -= dx
                a1y += dy
                a1 = (a1x, a1y)

            while check_on_roof(a2, roof_length, roof_width):
                antinode_locations.add(a2)
                a2x += dx
                a2y -= dy
                a2 = (a2x, a2y)

# display_antinodes(antinode_locations, roof_length, roof_width)
print("Part 2:", len(antinode_locations))

# 1139 - too low
# 1249 - too high
