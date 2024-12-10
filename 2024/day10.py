from collections import defaultdict
from io import StringIO

test = """0123
1234
8765
9876"""

test = """...0...
...1...
...2...
6543456
7.....7
8.....8
9.....9"""

test = """..90..9
...1.98
...2..7
6543456
765.987
876....
987...."""

test = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

topomap = defaultdict(lambda: -1)
trail_starts = set()
counts = defaultdict(set)


def step_up_to_neighbours(map, location):
    value = map[location]
    x, y = location
    for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
        new_location = (x + dx, y + dy)
        if map[new_location] == value + 1:
            yield new_location


# with StringIO(test) as input_data:
with open("input10.txt") as input_data:
    for y, line in enumerate(input_data):
        for x, ch in enumerate(line.strip()):
            if ch.isdigit():
                topomap[(x, y)] = int(ch)
                if ch == "0":
                    trail_starts.add((x, y))

# print(topomap, trail_starts)

for start in trail_starts:
    queue = [start]
    while len(queue) > 0:
        current = queue.pop(0)
        for neighbour in step_up_to_neighbours(topomap, current[-1]):
            next_path = list(current) + [neighbour]
            if topomap[neighbour] == 9:
                counts[start].add(next_path)
                continue
            if next_path not in queue:
                queue.append(next_path)

print(trail_starts)
print(counts)

print("Part 1:", sum(len(s) for s in counts.values()))
