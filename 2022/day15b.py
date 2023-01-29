from io import StringIO
from collections import defaultdict
from more_itertools import pairwise

test = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

# test = """Sensor at x=2, y=2: closest beacon is at x=-2, y=-2"""

class Sensor:
    def __init__(self, centre, radius):
        self.centre = centre
        self.radius = radius
        self.corners = ((centre[0]-radius,centre[1]),(centre[0],centre[1]-radius),(centre[0]+radius,centre[1]),(centre[0],centre[1]+radius))
        self.sides = set()
        for (c1x,c1y),(c2x,c2y) in pairwise(list(self.corners) + [self.corners[0]]):
            i, j = c1x,c1y
            while i != c2x and j != c2y:
                self.sides.add((i,j))
                i += 1 if i <= c2x else -1
                j += 1 if j <= c2y else -1

    def get_corners(self):
        return self.corners

    def get_sides(self):
        return self.sides

    def __contains__(self, row):
        return self.centre[1] - radius <= row <= self.centre[1] + radius

    def __str__(self):
        return f"Sensor[{self.centre}, {self.radius}]"

def manhattan_distance(pa, pb):
    distance = sum(abs(p1-p2) for p1, p2 in zip(pa, pb))
    return distance

"""
fn fill(x, y):
  if not Inside(x, y) then return
  let s = new empty queue or stack
  Add (x, x, y, 1) to s
  Add (x, x, y - 1, -1) to s
  while s is not empty:
    Remove an (x1, x2, y, dy) from s
    let x = x1
    if Inside(x, y):
      while Inside(x - 1, y):
        Set(x - 1, y)
        x = x - 1
    if x < x1:
      Add (x, x1-1, y-dy, -dy) to s
    while x1 <= x2:
      while Inside(x1, y):
        Set(x1, y)
        x1 = x1 + 1
        Add (x, x1 - 1, y+dy, dy) to s
        if x1 - 1 > x2:
          Add (x2 + 1, x1 - 1, y-dy, -dy) to s
      x1 = x1 + 1
      while x1 < x2 and not Inside(x1, y):
        x1 = x1 + 1
      x = x1

def scan_and_fill(ox, oy, boundary_distance):
    def is_inside(x,y):
        return 0 <= x <= 4000000 and 0 <= y <= 4000000 and manhattan_distance((x,y),(ox,oy)) <= boundary_distance and results[(x,y)] == None
    
    # print((ox,oy), boundary_distance)
    if not is_inside(ox,oy):
        return

    s = [(ox,ox,oy,1), (ox,ox,oy-1,-1)]
    while len(s) != 0:
        # print("len s:", len(s))
        x1,x2,y,dy = s.pop()
        x = x1
        if is_inside(x,y):
            while is_inside(x-1,y):
                results[(x-1,y)] = 1
                x -= 1
        if x < x1:
            # print("adding 1")
            s.append((x,x1-1,y-dy,-dy))
        while x1 <= x2:
            while is_inside(x1,y):
                results[(x1,y)] = 1
                x1 += 1
                # print("adding 2")
                s.append((x,x1-1,y+dy,dy))
                if x1-1 > x2:
                    # print("adding 3")
                    s.append((x2+1,x1-1,y-dy,-dy))
            x1 += 1
            while x1 < x2 and not is_inside(x1,y):
                x1 += 1
            x = x1
"""

show_missing = False
class cave_dict(defaultdict):
    def __missing__(self, key):
        # return super.__missing__(key)
        if show_missing:
            print(key)
        return None

results = cave_dict()
min_coord = 0
max_coord = 4000000

sensors = set()
corners = {}
sides = {}
with StringIO(test) as f:
# with open("input15.txt") as f:
    minx = float("inf")
    maxx = float("-inf")

    row = 0
    for line in f:
        sensor, beacon = line.strip().split(":")
        sx,sy = [int(s.split("=")[1]) for s in sensor.split(",")]
        bx,by = [int(b.split("=")[1]) for b in beacon.split(",")]
        
        results[(sx,sy)] = 0
        results[(bx,by)] = 0
        distance = manhattan_distance((sx,sy), (bx,by))
        
        s = Sensor((sx,sy), distance)
        sensors.add(s)
        for corner in s.get_corners():
            corners[corner] = chr(ord("A") + row)

        for point in s.get_sides():
            sides[point] = chr(ord("A") + row)

        row += 1

        # minx = max(min_coord,min(sx-distance,minx))
        # maxx = min(max_coord,max(sx+distance,maxx))

        # print((sx,sy), (bx,by), distance)

        # for x in range(max(min_coord, sx-distance),min(max_coord,sx+distance)+1):
        #     for y in range(max(min_coord,sy-distance),min(max_coord,sy+distance)+1):
        #         if manhattan_distance((sx,sy),(x,y)) <= distance and results[(x,y)] == None:
        #             results[(x,y)] = 1

        # for x in range(min_coord, max_coord+1):
        #     for y in range(min_coord, max_coord+1):
        #         print(results.get((x,y), "."), end="")
        #     print()

        # print("\n---\n")
        
        # need to efficiently fill the area
        # scan_and_fill(sx, sy, distance)
        # print("filled")

    # print(sum(results.values()))
    # show_missing=True
    # for x in range(min_coord, max_coord+1):
        # for y in range(min_coord, max_coord+1):
            # results[(x,y)]
            # print(results.get((x,y), "."), end="")
        #print()

#     definitely_not = 0
#     for n in range(minx,maxx+1):
#         if results[(n,target_row)] != None:
#             definitely_not += results[(n,target_row)]
# 
#     print(definitely_not)
    
    # for n in range(minx,maxx+1):
    #     print(results.get((n,target_row),"."),end="")

for j in range(21):
    row = []
    for i in range(21):
        if (i,j) in corners:
            row.append(corners[(i,j)])
        elif (i,j) in sides:
            row.append(sides[(i,j)].lower())
        else:
            row.append(" ")
    print("".join(row))

for s in sensors:
    for c in s.get_corners():
        if 0 <= c[0] <= 20 and 0 <= c[1] <= 20:
            for d in ((-1,0),(0,-1),(1,0),(0,1)):
                if 0 <= d[0] <= 20 and 0 <= d[1] <= 20:
                    if (c[0]+d[0],c[1]+d[1]) not in sides:
                        print(corners[c], "found:", (c[0]+d[0]+1,c[1]+d[1]+1))
