from collections import defaultdict
from io import StringIO

test = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""

def get_neighbours(warehouse, spot):
    neighbours = []
    for adj in ((0-1j),(1-1j),(1+0j),(1+1j),(0+1j),(-1+1j),(-1+0j),(-1-1j)):
        nspot = spot + adj
        if warehouse[nspot] == "@":
            neighbours.append(nspot)
    return neighbours

def part1(warehouse, max_x, max_y):
    accessible = 0
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            spot = complex(x,y)
            if warehouse[spot] == "@" and len(get_neighbours(warehouse, spot)) < 4:
                accessible += 1

    return accessible

def part2(warehouse, max_x, max_y):
    accessible = 0
    made_change = True
    
    while made_change:
        made_change = False

        for y in range(max_y + 1):
            for x in range(max_x + 1):
                spot = complex(x,y)
                if warehouse[spot] == "@" and len(get_neighbours(warehouse, spot)) < 4:
                    accessible += 1
                    warehouse[spot] = "X"
                    made_change = True

    return accessible

warehouse = defaultdict(lambda: ".")

# with StringIO(test) as file:
with open("input4.txt") as file:
    for y, row in enumerate(file):
        for x, ch in enumerate(row.strip()):
            if ch == "@":
                warehouse[complex(x,y)] = ch
                
max_x = x
max_y = y

print("Part 1:", part1(warehouse, max_x, max_y))
print("Part 2:", part2(warehouse, max_x, max_y))

# 2831 too low
