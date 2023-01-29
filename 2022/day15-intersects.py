from io import StringIO
from time import time
from itertools import permutations

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
    def generate_line(lx, ly, rx, ry):
        i, j = lx, ly
        while i != rx and j != ry:
            yield complex(i, j)
            i += 1 if i <= rx else -1
            j += 1 if j <= ry else -1
        yield complex(i, j)

    def __init__(self, centre_x, centre_y, radius):
        self.centre = complex(centre_x, centre_y)
        self.radius = radius
        self.lines = {
                        1: { p for p in Sensor.generate_line(centre_x - radius, centre_y, centre_x, centre_y - radius) },
                        2: { p for p in Sensor.generate_line(centre_x + radius, centre_y, centre_x, centre_y - radius) },
                        3: { p for p in Sensor.generate_line(centre_x - radius, centre_y, centre_x, centre_y + radius) },
                        4: { p for p in Sensor.generate_line(centre_x + radius, centre_y, centre_x, centre_y + radius) }
                     }

    """
        want to separate into four conceptual lines:
            #
           1 2
          1   2
         #  C  #
          3   4
           3 4
            #

        then look for intersects of 1 or 4 with other sensor's 2 or 3.
        1x2 may have a gap above, and 4x3 may have a gap below on the x-axis, or
        1x3 may have a gap left, and 4x2 may have a gap right on the y-axis.
    """

    def get_row(self, grid_row, min_x, max_x):
        leftmost = max(min_x, int(self.centre.real) - self.radius + abs(int(self.centre.imag) - grid_row))
        rightmost = min(max_x, int(self.centre.real) + self.radius - abs(int(self.centre.imag) - grid_row))
        return (complex(x, grid_row) for x in range(leftmost, rightmost + 1))

    def __contains__(self, row):
        return self.centre.imag - self.radius <= row <= self.centre.imag + self.radius

    def __str__(self):
        return f"Sensor[{self.centre}, {self.radius}]"

def manhattan_distance(pa, pb):
    distance = sum(abs(p1-p2) for p1, p2 in zip(pa, pb))
    return distance

def check_row(sensors, target_row, min_x=float("-inf"), max_x=float("inf")):
    hits = set()
    [hits.update(sensor.get_row(target_row, min_x, max_x)) for sensor in sensors if target_row in sensor]

    return hits

# target_row = 10
target_row = 2000000
min_xy = 0
max_xy = 4000000
sensors = set()
beacons = set()

start = time()

# with StringIO(test) as f:
with open("input15.txt") as f:
    for line in f:
        sensor, beacon = line.strip().split(":")
        sx,sy = [int(s.split("=")[1]) for s in sensor.split(",")]
        bx,by = [int(b.split("=")[1]) for b in beacon.split(",")]
        
        # print(sx,sy,bx,by)

        distance = manhattan_distance((sx,sy), (bx,by))
        # width = 2 * distance + 1

        sensors.add(Sensor(sx, sy, distance))
        beacons.add(complex(bx,by))
print("Setup:", time() - start)

start = time()
print("Part 1:", len(check_row(sensors, target_row) - beacons))
print("Time:", time() - start)

start = time()
found = False
for s1, s2 in permutations(sensors, 2):
    def check_candidate(cell):
        return min_xy <= cell.real <= max_xy and min_xy <= cell.imag <= max_xy and len(check_row(sensors, int(cell.imag), min_xy, max_xy)) != (max_xy - min_xy) + 1
        # if min_xy <= cell.real <= max_xy:
        #     # print("x in bounds")
        #     if min_xy <= cell.imag <= max_xy:
        #         # print("y in bounds")
        #         if len(check_row(sensors, int(cell.imag), min_xy, max_xy)) != (max_xy - min_xy) + 1:
        #             print(f"{(cell.real,cell.imag)} is the one")
        #             return True
        #         # else:
        #             # print(f"{(cell.real,cell.imag)} is not the one")
        #             # return False
        # print(f"{(cell.real,cell.imag)} is not the one")
        # return False

    s11s22 = s1.lines[1] & s2.lines[2]
    if len(s11s22) > 0:
        assert(len(s11s22) == 1)
        meet = next(c for c in s11s22)
        cell = complex(meet.real, meet.imag-1)
        found = check_candidate(cell)
        if found: break

    s11s23 = s1.lines[1] & s2.lines[3]
    if len(s11s23) > 0:
        assert(len(s11s23) == 1)
        meet = next(c for c in s11s23)
        cell = complex(meet.real-1, meet.imag)
        found = check_candidate(cell)
        if found: break

    s14s22 = s1.lines[4] & s2.lines[2]
    if len(s14s22) > 0:
        assert(len(s14s22) == 1)
        meet = next(c for c in s14s22)
        cell = complex(meet.real+1, meet.imag)
        found = check_candidate(cell)
        if found: break

    s14s23 = s1.lines[4] & s2.lines[3]
    if len(s14s23) > 0:
        assert(len(s14s23) == 1)
        meet = next(c for c in s14s23)
        cell = complex(meet.real, meet.imag+1)
        found = check_candidate(cell)
        if found: break

if found:
    print("Part 2:", (int(cell.real), int(cell.imag)), cell.real * 4000000 + cell.imag)
print("Time:", time() - start)

# 13029714573243 - (3257428, 2573242)
