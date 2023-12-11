from itertools import count, combinations, repeat
from io import StringIO

test = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

def manhattan_distance(pa, pb):
    return sum(abs(p1 - p2) for (p1, p2) in zip(pa, pb))

universe = {}
galaxies = count(0)
# spread = 1
spread = 999999

# with StringIO(test) as data:
with open("input11.txt") as data:
    for y, line in enumerate(data):
        for x, ch in enumerate(line.strip()):
            if ch != ".":
                universe[next(galaxies)] = [y,x]
                
y = min(universe.items(), key=lambda n:n[1][0])[1][0]
while y < max(universe.items(), key=lambda n:n[1][0])[1][0]:
    if len([gv for gv in universe.values() if gv[0] == y]) == 0:
        for gv in [gv for gv in universe.values() if gv[0] > y]:
            gv[0] += spread
        y += spread
    y += 1

x = min(universe.items(), key=lambda n:n[1][1])[1][1]
while x < max(universe.items(), key=lambda n:n[1][1])[1][1]:
    if len([gv for gv in universe.values() if gv[1] == x]) == 0:
        for gv in [gv for gv in universe.values() if gv[1] > x]:
            gv[1] += spread
        x += spread
    x += 1

print("Part 1/2:", sum([manhattan_distance(universe[p1], universe[p2]) for p1, p2 in combinations(universe, 2)]))
