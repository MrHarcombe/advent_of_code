from io import StringIO
from time import time

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

    def get_row(self, grid_row, min_x, max_x):
        leftmost = max(min_x, self.centre[0] - self.radius + abs(self.centre[1] - grid_row))
        rightmost = min(max_x, self.centre[0] + self.radius - abs(self.centre[1] - grid_row))
        return ((x, grid_row) for x in range(leftmost, rightmost + 1))

    def __contains__(self, row):
        return self.centre[1] - self.radius <= row <= self.centre[1] + self.radius

    def __str__(self):
        return f"Sensor[{self.centre}, {self.radius}]"

def manhattan_distance(pa, pb):
    distance = sum(abs(p1-p2) for p1, p2 in zip(pa, pb))
    return distance

def check_row(sensors, target_row, min_x=float("-inf"), max_x=float("inf")):
    hits = set()
    for sensor in sensors:
        if target_row in sensor:
            s_row = sensor.get_row(target_row, min_x, max_x)
            hits.update(s_row)

    return hits

# target_row = 10
target_row = 2000000
sensors = set()
beacons = set()

# with StringIO(test) as f:
with open("input15.txt") as f:
    for line in f:
        sensor, beacon = line.strip().split(":")
        sx,sy = [int(s.split("=")[1]) for s in sensor.split(",")]
        bx,by = [int(b.split("=")[1]) for b in beacon.split(",")]
        
        # print(sx,sy,bx,by)

        distance = manhattan_distance((sx,sy), (bx,by))
        width = 2 * distance + 1

        sensors.add(Sensor((sx,sy), distance))
        beacons.add((bx,by))

start = time()
print("Part 1:", len(check_row(sensors, target_row) - beacons))
print("Time:", time() - start)

start = time()
for row in range(4000001):
    row_length = check_row(sensors, row, 0, 4000000)
    if len(row_length) != 4000001:
        print(row, "->", len(row_length))
        break
    #print("Interim:", time() - start)
    
for col in range(4000001):
    if (col, row) not in row_length:
        print((col,row))
        break
print("Time:", time() - start)
