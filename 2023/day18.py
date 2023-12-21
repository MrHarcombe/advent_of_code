from collections import OrderedDict
from io import StringIO
import re

test = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""

command = re.compile(r"([UDLR]) ([0-9]+) \(\#([0-9a-f]+)\)")
directions = {"U": (-1,0), "R": (0,1), "D": (1,0), "L": (0,-1)}
p2_directions = "RDLU"

def get_shoelace_area(loop):
    return abs(sum([(loop[i][0] + loop[i+1][0])*(loop[i][1] - loop[i+1][1]) for i in range(len(loop)-1)]))/2

steps = []
# with StringIO(test) as data:
with open("input18.txt") as data:
    for line in data:
        match = command.search(line)
        dx = match.group(1)
        s = int(match.group(2))
        c = match.group(3)
        steps.append((dx,s,c))

trench = OrderedDict()
pos = (0,0)

for dx, count, colour in steps:
    dr, dc = directions[dx]
    new_pos = (pos[0] + dr * count, pos[1] + dc * count)
    trench[new_pos] = count # colour
    pos = new_pos

print("Part 1:", sum(trench.values()) // 2 + get_shoelace_area([k for k in trench]) + 1)

p2_trench = OrderedDict()
p2_pos = (0,0)
for _, _, instruction in steps:
    length = int(instruction[:5], 16)
    dr, dc = directions[p2_directions[int(instruction[-1])]]
    new_pos = (pos[0] + dr * length, pos[1] + dc * length)
    p2_trench[new_pos] = length
    pos = new_pos

print("Part 2:", sum(p2_trench.values()) // 2 + get_shoelace_area([k for k in p2_trench]) + 1)
