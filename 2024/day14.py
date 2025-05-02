from collections import defaultdict
from io import StringIO
from math import prod

test = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""

# test = """p=2,4 v=2,-3"""


def get_robot_position_at(robot, time, room):
    start, velocity = robot
    x, y = start
    dx, dy = velocity
    rx, ry = room
    x = (x + dx * time) % rx
    y = (y + dy * time) % ry

    return (x, y)


def score_room(room, room_size):
    width, height = room_size
    mw = width // 2
    mh = height // 2
    tl = [len(room[r]) for r in room if r[0] < mw and r[1] < mh]
    tr = [len(room[r]) for r in room if r[0] > mw and r[1] < mh]
    bl = [len(room[r]) for r in room if r[0] < mw and r[1] > mh]
    br = [len(room[r]) for r in room if r[0] > mw and r[1] > mh]
    return tl, tr, bl, br


turns = 100
room_size = (101, 103)
robots = []

# with StringIO(test) as input_data:
with open("input14.txt") as input_data:
    for line in input_data:
        point, velocity = line.strip().split()
        # print(point, velocity)
        robot = (
            tuple(list(map(int, point[2:].split(",")))),
            tuple(list(map(int, velocity[2:].split(",")))),
        )
        robots.append(robot)

# print(robots)

for t in range(turns + 1):
    room = defaultdict(list)
    for r in robots:
        pos = get_robot_position_at(r, t, room_size)
        # print(r, "->", pos)
        room[pos].append(r)
    # print(room)

    # for y in range(7):
    #     line = []
    #     for x in range(11):
    #         if (x, y) in room:
    #             line.append(str(len(room[(x, y)])))
    #         else:
    #             line.append(".")
    #     print("".join(line))
    # print()

quadrants = score_room(room, room_size)
print("Part 1:", prod(sum(q) for q in quadrants))

# 224351424 too high

t = 0
finished = False
while not finished:
    t += 1
    room = defaultdict(list)
    for r in robots:
        pos = get_robot_position_at(r, t, room_size)
        # print(r, "->", pos)
        room[pos].append(r)

    rcount = [len(room[r]) for r in room]
    if prod(rcount) == 1:
        print("Time:", t)
        for y in range(room_size[1]):
            line = []
            for x in range(room_size[0]):
                if (x, y) in room:
                    line.append(str(len(room[(x, y)])))
                else:
                    line.append(".")
            print("".join(line))
        print()
        input("More? ")
