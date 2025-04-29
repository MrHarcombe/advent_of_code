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

    max_x = max(conway.keys(), key=itemgetter(0))[0]
    max_y = max(conway.keys(), key=itemgetter(1))[1]
    max_z = max(conway.keys(), key=itemgetter(2))[2]

    return (min_x, min_y, min_z), (max_x, max_y, max_z)


def get_neighbour_count(conway, x, y, z):
    count = 0
    for nz in range(z-1, z+2):
        for ny in range(y-1, y+2):
            for nx in range(x-1, x+2):
                if conway[(nx,ny,nz)] == "#" and (nx, ny, nz) != (x, y, z):
                    count += 1
    return count

def display_zone(generation, conway):
    mins, maxs = get_min_max(conway)
    print(f"Generation: {generation+1}")
    print(f"Min X:{mins[0]}, Y:{mins[1]}")
    
    for dz in range(mins[2], maxs[2]+1):
        print(f"z={dz}")
        for dy in range(mins[1], maxs[1]+1):
            for dx in range(mins[0], maxs[0]+1):
                print(conway[(dx,dy,dz)], end="")
            print()
        print()

with StringIO(initial) as data:
    for row, line in enumerate(data):
        for col, ch in enumerate(line.strip()):
            if ch != ".":
                conway[col, row, 0] = ch

display_zone(-1, conway)

for generation in range(6):
    mins, maxs = get_min_max(conway)
    new_conway = defaultdict(lambda: ".")
    for z in range(mins[2]-1, maxs[2]+2):
        for y in range(mins[1]-1, maxs[1]+2):
            for x in range(mins[0]-1, maxs[0]+2):
                count = get_neighbour_count(conway, x, y, z)
                #print(x,y,z,count)
                if conway[(x,y,z)] == "#" and count in (2,3):
                    new_conway[(x,y,z)] = "#"
                elif conway[(x,y,z)] == "." and count == 3:
                    new_conway[(x,y,z)] = "#"
    conway = new_conway

#display_zone(generation, conway)
print("Part 1:", len([ch for ch in conway.values() if ch == "#"]))

