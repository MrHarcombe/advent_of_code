from io import StringIO
# from collections import defaultdict
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

# class cave_dict(defaultdict):
#     def __missing__(self, key):
#         # return super.__missing__(key)
#         return None

def in_manhattan_area(x, y, sx, sy, distance):
    manhattan_area = set()

    for manhattan_row in range(0, distance+1):
        drawing_width = 2 * manhattan_row + 1

        manhattan_area |= { (x, sy - distance + manhattan_row) for x in range(max(min_coord, sx - drawing_width // 2), min(max_coord+1, sx + drawing_width // 2) + 1) }
        manhattan_area |= { (x, sy + distance - manhattan_row) for x in range(max(min_coord, sx - drawing_width // 2), min(max_coord+1, sx + drawing_width // 2) + 1) }

    # print(manhattan_area)
    if (14,11) in manhattan_area:
        print("(14,11) in",sx,sy,bx,bx,distance)
    return manhattan_area

def get_manhattan_coverage(distance):
    return 2 * distance ** 2 + 2 * distance + 1

# results = cave_dict()
maybes = None
min_coord = 0
# max_coord = 20
max_coord = 4000000

readings = []

# with StringIO(test) as f:
with open("input15.txt") as f:
    for line in f:
        sensor, beacon = line.strip().split(":")
        sx,sy = [int(s.split("=")[1]) for s in sensor.split(",")]
        bx,by = [int(b.split("=")[1]) for b in beacon.split(",")]
        distance = manhattan_distance((sx,sy), (bx,by))

        readings.append((sx,sy,bx,by,distance))

for sx, sy, bx, by, distance in sorted(readings, key=lambda item:item[4], reverse=True):
    print((max_coord + 1) ** 2 - get_manhattan_coverage(distance))
    
    if maybes == None:
        # maybes = { (x,y) for x in range(max_coord+1) for y in range(max(min_coord,sy-distance-1),min(max_coord,sy+distance+2)) if manhattan_distance((x,y),(sx,sy)) > distance }
        maybes = { (x,y) for x in range(max_coord+1) for y in range(max_coord+1) if manhattan_distance((x,y),(sx,sy)) > distance }

    else:
        # maybes &= { (x,y) for x in range(max_coord+1) for y in range(max(min_coord,sy-distance-1),min(max_coord,sy+distance+2)) if manhattan_distance((x,y),(sx,sy)) > distance }
        maybes &= { (x,y) for x in range(max_coord+1) for y in range(max_coord+1) if manhattan_distance((x,y),(sx,sy)) > distance }

    print(len(maybes))
    # if len(maybes) == 1:
    #     print(maybes)

print(maybes)

# for row in range(max_coord+1):
#     row_readings = np.zeros(max_coord+1, np.int8)
# 
#     for sx, sy, bx, by, distance in readings:
#         # print(sx,sy,bx,by,distance)
#         if min_coord <= sx <= max_coord and sy == row: row_readings[sx] = 1
#         if min_coord <= bx <= max_coord and by == row: row_readings[bx] = 1
# 
#         width = 2 * distance + 1
# 
#         for manhattan_row in range(0, distance+1):
#             drawing_width = 2 * manhattan_row + 1
#             
#             if sy - distance + manhattan_row == row:
#                 # print("row", row, manhattan_row, "so manhattan width=", (width // 2) - manhattan_row, "to", (width // 2) + manhattan_row)
#                 # print((sx,sy), width, "so blocking out", max(min_coord, sx - drawing_width // 2), ":", min(max_coord+1, sx + drawing_width // 2))
#                 row_readings[max(min_coord, sx - drawing_width // 2):min(max_coord+1, sx + drawing_width // 2) + 1] = 1
# 
#             if sy + distance - manhattan_row == row:
#                 # print("row", row, manhattan_row, "so manhattan width=", (width // 2) - manhattan_row, "to", (width // 2) + manhattan_row)
#                 # print((sx,sy), width, "so blocking out", max(min_coord, sx - drawing_width // 2), ":", min(max_coord+1, sx + drawing_width // 2))
#                 row_readings[max(min_coord, sx - drawing_width // 2):min(max_coord+1, sx + drawing_width // 2) + 1] = 1
# 
#     if np.sum(row_readings) < max_coord + 1:
#         print("candidate:", row, np.where(row_readings == 0))
#         break
#     else:
#         print("no candidates on", row)
