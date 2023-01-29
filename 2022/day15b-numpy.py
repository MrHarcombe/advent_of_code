from io import StringIO
from collections import defaultdict
import numpy as np

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
"""
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

show_missing = False
class cave_dict(defaultdict):
    def __missing__(self, key):
        # return super.__missing__(key)
        if show_missing:
            print(key)
        return None

# results = cave_dict()
min_coord = 0
# max_coord = 20
# max_coord = 4000000
max_coord = 100000

results = np.zeros((max_coord+1,max_coord+1),np.int8)

# with StringIO(test) as f:
with open("input15.txt") as f:
    for line in f:
        sensor, beacon = line.strip().split(":")
        sx,sy = [int(s.split("=")[1]) for s in sensor.split(",")]
        bx,by = [int(b.split("=")[1]) for b in beacon.split(",")]

        if min_coord<=sx<=max_coord and min_coord<=sy<=max_coord: results[sx,sy] = 1
        if min_coord<=bx<=max_coord and min_coord<=by<=max_coord: results[bx,by] = 1
        distance = manhattan_distance((sx,sy), (bx,by))
        # minx = max(min_coord,min(sx-distance,minx))
        # maxx = min(max_coord,max(sx+distance,maxx))

        # print((sx,sy), (bx,by), distance)

        width = 2*distance+1
        manhattan_overlay = np.zeros((width,width),np.int8)
        for row in range(distance+1):
            manhattan_overlay[(width//2)-row:(width//2)+row+1,row] = 1
            manhattan_overlay[(width//2)-row:(width//2)+row+1,-(row+1)] = 1

        subrange = results[max(min_coord,sx-distance):min(max_coord,sx+distance),max(min_coord,sy-distance):min(max_coord,sy+distance)]
        # print(subrange)
        # print(subrange.shape)
        # print(sx-distance, max(min_coord,sx-distance))
        
        manhattan_subrange = manhattan_overlay[sx-distance:width+1,sy-distance:width+1]
        print(manhattan_subrange)
        
        # print(sx+distance, min(max_coord,sx+distance))
        # print(manhattan_overlay)
        # print(manhattan_overlay.shape)
        # print(np.add(subrange, manhattan_overlay))

        for x in range(max(min_coord, sx-distance),min(max_coord,sx+distance)+1):
            for y in range(max(min_coord,sy-distance),min(max_coord,sy+distance)+1):
                if manhattan_distance((sx,sy),(x,y)) <= distance and results[x,y] == 0:
                    results[x,y] = 1

        # for x in range(min_coord, max_coord+1):
        #     for y in range(min_coord, max_coord+1):
        #         print(results.get((x,y), "."), end="")
        #     print()

        # print("\n---\n")
        
        # need to efficiently fill the area
        # scan_and_fill(sx, sy, distance)
        # print("filled")

        # print(results)

print(np.where(results == 0))
