from hexgrid import HexGrid
from io import StringIO

test = "nw,nw,nw"

# with StringIO(test) as f:
with open("input11.txt") as f:
    for line in f:
        steps = line.strip().split(",")

board = HexGrid(True)
origin = HexGrid.get_origin()
current = origin
max_distance = 0
for step in steps:
    current = board.get_neighbour(current, step)
    max_distance = max(max_distance, HexGrid.distance(origin, current))

print("Part 1:", HexGrid.distance(origin, current))
print("Part 2:", max_distance)
