from collections import defaultdict
from io import StringIO
from operator import itemgetter

test = """.#.
..#
###"""

initial = """.#..####
.#.#...#
#..#.#.#
###..##.
..##...#
..##.###
#.....#.
..##..##"""

conway = defaultdict(lambda:".")

def get_min_max(conway):
    min_x = min(conway.keys(), key=itemgetter(0))[0]
    min_y = min(conway.keys(), key=itemgetter(1))[1]
    min_z = min(conway.keys(), key=itemgetter(2))[2]
    min_w = min(conway.keys(), key=itemgetter(3))[3]

    max_x = max(conway.keys(), key=itemgetter(0))[0]
    max_y = max(conway.keys(), key=itemgetter(1))[1]
    max_z = max(conway.keys(), key=itemgetter(2))[2]
    max_w = max(conway.keys(), key=itemgetter(3))[3]

    return (min_x, min_y, min_z, min_w), (max_x, max_y, max_z, max_w)


def get_neighbour_count(conway, x, y, z, w):
    count = 0
    for nw in range(w-1, w+2):
        for nz in range(z-1, z+2):
            for ny in range(y-1, y+2):
                for nx in range(x-1, x+2):
                    if conway[(nx,ny,nz,nw)] == "#" and (nx, ny, nz, nw) != (x, y, z, w):
                        count += 1
    return count

with StringIO(initial) as data:
    for row, line in enumerate(data):
        for col, ch in enumerate(line.strip()):
            if ch != ".":
                conway[col, row, 0, 0] = ch

for generation in range(6):
    mins, maxs = get_min_max(conway)
    new_conway = defaultdict(lambda: ".")
    for w in range(mins[3]-1, maxs[3]+2):
        for z in range(mins[2]-1, maxs[2]+2):
            for y in range(mins[1]-1, maxs[1]+2):
                for x in range(mins[0]-1, maxs[0]+2):
                    count = get_neighbour_count(conway, x, y, z, w)
                    if conway[(x,y,z,w)] == "#" and count in (2,3):
                        new_conway[(x,y,z,w)] = "#"
                    elif conway[(x,y,z,w)] == "." and count == 3:
                        new_conway[(x,y,z,w)] = "#"
    conway = new_conway

print("Part 2:", len([ch for ch in conway.values() if ch == "#"]))

