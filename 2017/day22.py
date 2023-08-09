from collections import defaultdict
from io import StringIO
from enum import Enum, auto

class Direction(Enum):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()

    def next(self):
        cls = self.__class__
        members = list(cls)
        index = members.index(self) + 1
        if index >= len(members):
            index = 0
        return members[index]

    def prev(self):
        cls = self.__class__
        members = list(cls)
        index = members.index(self) - 1
        if index < 0:
            index = len(members) - 1
        return members[index]

class Virus:
    def __init__(self, pos, dir):
        self.pos = pos
        self.dir = dir

def burst(virus, map):
    infect = False
    
    # step one, turn
    if map[virus.pos] == "#":
        virus.dir = virus.dir.next()
    else:
        virus.dir = virus.dir.prev()

    # step two, infect/disinfect
    if map[virus.pos] == "#":
        map[virus.pos] = "."
    else:
        map[virus.pos] = "#"
        infect = True
    
    # step three, move
    dx, dy = 0, 0
    if virus.dir == Direction.NORTH:
        dy -= 1
    elif virus.dir == Direction.EAST:
        dx += 1
    elif virus.dir == Direction.SOUTH:
        dy += 1
    else:
        dx -= 1

    virus.pos = (virus.pos[0]+dx, virus.pos[1]+dy)
    return infect

test = """..#
#..
..."""

map = defaultdict(lambda: ".")
centre = None

# with StringIO(test) as data:
with open("2017/input22.txt") as data:
    line_number = 0
    for line in data:
        line = line.strip()
        for pos in range(len(line)):
            map[(pos, line_number)] = line[pos]
        
        if centre == None:
            centre = len(line) // 2 # + (0 if len(line) % 2 == 0 else 1)

        line_number += 1

print(map)
print(centre, map[(centre, centre)])

virus = Virus((centre, centre), Direction.NORTH)
infected = 0
for _ in range(10000):
    infected += 1 if burst(virus, map) else 0

print(infected)
