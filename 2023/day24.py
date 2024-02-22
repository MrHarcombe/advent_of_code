from functools import cache
from io import StringIO
from itertools import combinations

test = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""

hailstones = []

@cache
def get_slope(point, velocity):
    px, py, _ = point
    vx, vy, _ = velocity
    x1 = px + vx
    y1 = py + vy

    return (y1 - py) / (x1 - px)

def get_line_components(point, velocity):
    #
    # y = mx + c -> y - mx - c = 0
    # but using ax + by + c = 0 (so... a = -m, y = 1, c = -c)
    #
    slope = get_slope(point, velocity)
    px, py, _ = point
    
    return -slope, 1, px * slope - py

def get_intersection(l1, l2):
    a1, b1, c1 = l1
    a2, b2, c2 = l2

    #
    # intersection is at
    #
    # b1c2 - b2c1 / a1b2 - a2b1, a2c1 - a1c2 /  a1b2 - a2b1
    #

    return ((b1 * c2 - b2 * c1) / (a1 * b2 - a2 * b1)), ((a2 * c1 - a1 * c2) / (a1 * b2 - a2 * b1))

# with StringIO(test) as data:
with open("input24.txt") as data:
    for line in data:
        pos, vel = line.strip().split(" @ ")
        px, py, pz = map(int, pos.split(","))
        vx, vy, vz = map(int, vel.split(","))
        
        hailstones.append(((px,py,pz),(vx,vy,vz)))

# min_intersect = 7
# max_intersect = 27
min_intersect = 200000000000000
max_intersect = 400000000000000

intersects = 0
for (p1, v1), (p2, v2) in combinations(hailstones, 2):
    # check not parallel
    if get_slope(p1, v1) != get_slope(p2, v2):
        parts1 = get_line_components(p1, v1)
        parts2 = get_line_components(p2, v2)
        
        ix, iy = get_intersection(parts1, parts2)
        if min_intersect <= ix <= max_intersect and min_intersect <= iy <= max_intersect:
            if (v1[0] > 0 and ix > p1[0])  or (v1[0] < 0 and ix < p1[0]):
                if (v2[0] > 0 and ix > p2[0])  or (v2[0] < 0 and ix < p2[0]):
                    if (v1[1] > 0 and iy > p1[1])  or (v1[1] < 0 and iy < p1[1]):
                        if (v2[1] > 0 and iy > p2[1])  or (v2[1] < 0 and iy < p2[1]):
                            intersects += 1
            
print("Part 1:", intersects)
