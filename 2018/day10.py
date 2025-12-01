from io import StringIO
from operator import itemgetter
import regex

initial_conditions = regex.compile(r"position=< *([\-0-9]+), *([\-0-9]+)> velocity=< *([\-0-9]+), *([\-0-9]+)>")

test = """position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>"""

points = []

def get_point_at(point, time):
    pax = point[0][0] + time * point[1][0]
    pay = point[0][1] + time * point[1][1]
    return (pax, pay)

def check_verticals(time_points):
    ordered_points = sorted(time_points)
    last = ordered_points[0]
    count = 1
    for point in ordered_points[1:]:
        if point[0] == last[0] and point[1] == last[1] + 1:
            count += 1
            if count >= 5:
                return True
        else:
            count = 1
        last = point

def check_horizontals(time_points):
    ordered_points = sorted(time_points, key=itemgetter(1))
    last = ordered_points[0]
    count = 1
    for point in ordered_points[1:]:
        if point[1] == last[1] and point[0] == last[0] + 1:
            count += 1
            if count >= 3:
                return True
        else:
            count = 1
        last = point

def display_points(time_points, mnx, mxx, mny, mxy):
    for y in range(mny, mxy+1):
        row = []
        for x in range(mnx, mxx+1):
            if (x,y) in time_points:
                row.append("*")
            else:
                row.append(".")
        print("".join(row))

# with StringIO(test) as input_data:
with open("input10.txt") as input_data:
    for line in input_data:
        px, py, vx, vy = initial_conditions.match(line.strip()).allcaptures()[1:]
        
        point = (
            (int(*px), int(*py)),
            (int(*vx), int(*vy)),
        )
        points.append(point)

# print(points)

for time in range(1, 1_000_000):
    time_points = [get_point_at(p, time) for p in points]
    mnx = min(x for (x,y) in time_points)
    mxx = max(x for (x,y) in time_points)
    mny = min(y for (x,y) in time_points)
    mxy = max(y for (x,y) in time_points)

    if check_horizontals(time_points) or check_verticals(time_points):
        display_points(time_points, mnx, mxx, mny, mxy)
        print("Time:", time)
        input()
