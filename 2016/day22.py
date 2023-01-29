from io import StringIO
from itertools import permutations

test = """Filesystem            Size  Used  Avail  Use%
/dev/grid/node-x0-y0   10T    8T     2T   80%
/dev/grid/node-x0-y1   11T    6T     5T   54%
/dev/grid/node-x0-y2   32T   28T     4T   87%
/dev/grid/node-x1-y0    9T    7T     2T   77%
/dev/grid/node-x1-y1    8T    0T     8T    0%
/dev/grid/node-x1-y2   11T    7T     4T   63%
/dev/grid/node-x2-y0   10T    6T     4T   60%
/dev/grid/node-x2-y1    9T    8T     1T   88%
/dev/grid/node-x2-y2    9T    6T     3T   66%"""

def parse_line(line):
    parts = line.split()
    return parts[0], int(parts[1][:-1]), int(parts[2][:-1]), int(parts[3][:-1])

def get_coordinate_from_name(name):
    _, x, y = name.split("-")
    return (int(x[1:]), int(y[1:]))

nodes = {}

# with StringIO(test) as f:
with open("input22.txt") as f:
    for line in f:
        if not line.startswith("/"):
            continue
        
        name, size, used, avail = parse_line(line)
        # print(name, used, avail)
        nodes[get_coordinate_from_name(name)] = (size, used, avail)

print(len(nodes))
count = 0
for a,b in permutations(nodes,2):
    if nodes[a][1] > 0 and nodes[a][1] <= nodes[b][2]:
        count += 1
print(count)
