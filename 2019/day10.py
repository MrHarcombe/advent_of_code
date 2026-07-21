from collections import defaultdict
from io import StringIO
from itertools import combinations, product
from math import degrees, gcd, atan2, pi
from operator import itemgetter

test = """.#..#
.....
#####
....#
...##"""

test = """.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....#...###..
..#.#.....#....##"""

# test = """.#.
# ###
# .#."""

test = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""

scan = {}

def find_line_intersection(line1, line2):
    (x1, y1), (x2, y2) = line1
    (x3, y3), (x4, y4) = line2

    # Calculate denominators (determinant)
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    
    # If denominator is 0, the lines are parallel and never meet
    if denom == 0:
        return None 

    # Determinant math for intersection points
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    
    # Calculate the intersection coordinates
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))

def get_vector_step(sata, satb):
    sata_x, sata_y = sata
    satb_x, satb_y = satb

    vx = satb_x - sata_x
    vy = satb_y - sata_y
    mult = gcd(vx, vy)
    vx //= mult
    vy //= mult

    return vx, vy

def get_distance(sata, satb):
    return sum([(p2-p1)**2 for p1, p2 in zip(sata, satb)]) ** 0.5

def can_a_see_b(sata, satb):
    vx, vy = get_vector_step(sata, satb)

    sata_x, sata_y = sata
    satb_x, satb_y = satb

    point = (sata_x + vx, sata_y + vy)
    while point != (satb_x, satb_y) and scan.get(point, ".") != "#":
        point = (point[0] + vx, point[1] + vy)

    if point == (satb_x, satb_y):
        return True

    return False

def get_clockwise_angle(sata, satb):
    angle = degrees(atan2(satb[0]-sata[0], satb[1]-sata[1]))
    return angle

def make_pass(centre, others):
    to_destroy = []
    for other in others:
        if can_a_see_b(centre, other[0]):
            to_destroy.append(other[0])
    return to_destroy

# with StringIO(test) as inputs:
with open("input10.txt") as inputs:
    for row, line in enumerate(inputs):
        for col, ch in enumerate(line.strip()):
            if ch != ".":
                scan[(col,row)] = ch

viewings = {}
for satellite in scan:
    can_see = sum(can_a_see_b(sata, satb) for (sata, satb) in product([satellite], filter(lambda s: s != satellite, scan.keys())))
    viewings[satellite] = can_see
    
print("Part 1:", max(viewings.values()))

vectors = []
observer = max(viewings.items(), key=itemgetter(1))[0]
for (sata, satb) in product([observer], filter(lambda s: s != observer, scan.keys())):
    vectors.append((satb, get_distance(sata, satb), *get_vector_step(sata, satb)))

vectors = sorted(vectors, key=lambda satb: (-get_clockwise_angle(observer, satb[0]), satb[1]))
to_destroy = []
while len(to_destroy) < 200:
    to_destroy += make_pass(observer, vectors)

print("Part 2:", to_destroy[199][0] * 100 + to_destroy[199][1])
