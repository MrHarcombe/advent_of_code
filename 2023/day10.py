from io import StringIO
from math import ceil

# test = """.....
# .S-7.
# .|.|.
# .L-J.
# ....."""

# test = """..F7.
# .FJ|.
# SJ.L7
# |F--J
# LJ..."""

# test = """...........
# .S-------7.
# .|F-----7|.
# .||.....||.
# .||.....||.
# .|L-7.F-J|.
# .|..|.|..|.
# .L--J.L--J.
# ..........."""

# test = """.F----7F7F7F7F-7....
# .|F--7||||||||FJ....
# .||.FJ||||||||L7....
# FJL7L7LJLJ||LJ.L-7..
# L--J.L7...LJS7F-7L7.
# ....F-J..F7FJ|L7L7L7
# ....L7.F7||L7|.L7L7|
# .....|FJLJ|FJ|F7|.LJ
# ....FJL-7.||.||||...
# ....L---J.LJ.LJLJ..."""

test = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""

connections = {"|" : "1010", "-" : "0101", "L" : "1100", "J" : "1001", "7" : "0011", "F" : "0110" }
directions = "NESW"

def display_groundmap(ground, miny, maxy, minx, maxx):
    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            print(ground.get((y,x), " "), end="")
        print()
    print()

def update_start(ground, start, neighbours):
    s1 = tuple(p[1] - p[0] for p in zip(start, neighbours[0]))
    s2 = tuple(p[1] - p[0] for p in zip(start, neighbours[1]))
    # print(s1, s2)
    direction = "1" if (-1, 0) in (s1, s2) else "0"
    direction += "1" if (0, 1) in (s1, s2) else "0"
    direction += "1" if (1, 0) in (s1, s2) else "0"
    direction += "1" if (0, -1) in (s1, s2) else "0"
    pipe = [i[0] for i in connections.items() if i[1] == direction][0]
    # print(pipe)
    ground[start] = pipe

def get_start_neighbours(ground, start):
    for d, (dy, dx) in enumerate(((-1, 0), (0, 1), (1, 0), (0, -1))):
        for node in get_neighbours(ground, (start[0] + dy, start[1] + dx)):
            if node == start:
                yield (start[0] + dy, start[1] + dx)

def get_neighbours(ground, point):
    node = ground.get(point, ".")
    if node in connections:
        cx = connections[node]
        for d, (dy, dx) in enumerate(((-1, 0), (0, 1), (1, 0), (0, -1))):
            if cx[d] == "1":
                yield (point[0] + dy, point[1] + dx)


ground = {}
start = None

# with StringIO(test) as data:
with open("input10.txt") as data:
    for y, line in enumerate(data):
        for x, ch in enumerate(line.strip()):
            if ch != ".":
                ground[(y,x)] = ch
            if ch == "S":
                start = (y,x)

min_y = min(ground.keys(), key=lambda n:n[0])[0]
max_y = max(ground.keys(), key=lambda n:n[0])[0]
min_x = min(ground.keys(), key=lambda n:n[1])[1]
max_x = max(ground.keys(), key=lambda n:n[1])[1]
# display_groundmap(ground, min_y, max_y, min_x, max_x)

# for n in get_neighbours(ground, (1,3)):
#     print(n, ground.get(n, "."))

# for n in get_start_neighbours(ground, start):
#     print(n, ground.get(n, "."))

visited = [start]
current = start
next_steps = [n for n in get_start_neighbours(ground, start)]
update_start(ground, start, next_steps)
next_step = next_steps[0]

while next_step != None:
    current = next_step
    visited.append(current)
    next_steps = [node for node in get_neighbours(ground, current) if node not in visited]
    if len(next_steps) > 0:
        next_step = next_steps[0]
    else:
        next_step = None

print("Part 1:", ceil(len(visited)/2))

# visited now contains the perimeter... 
# start is the starting point...

#... so as long as I know which way I'm going (from the piece) I can
# then scan perpendicular until I either fall off the edge, or I hit
# the next piece of perimeter and add those co-ordinates to a set of
# internal pieces

# or, plan C, try performing a breadth-first on the known area,
# stopping at perimeter edges...
# then calculate the remaining area using the shoelace formula
# and then subtract the length of the pipe...

# or, plan D, scan from the top-left horizontally assuming I start on the
# outside and then flip (or not) according the following border patterns...
# 1) | flip
# 2) F-7 no flip
# 3) F-J flip
# 4) L-J no flip
# 5) L-7 flip
# ...in each case the number of - parts in between each corner can actually
# be 0 or more

outside = True
state = None
contained = 0
for y in range(min_y, max_y+1):
    for x in range(min_x, max_x+1):
        pipe = ground.get((y,x), ".")

        # need to check if we're now inside/outside
        if (y,x) in visited:
            if pipe == "|":
                outside = not outside
            elif pipe == "-":
                assert(state != None)
            elif pipe == "F":
                state = "case2or3"
            elif pipe == "L":
                state = "case4or5"
            elif pipe == "J":
                if state == "case2or3":
                    state = None
                    outside = not outside
                elif state == "case4or5":
                    state = None
            elif pipe == "7":
                if state == "case2or3":
                    state = None
                elif state == "case4or5":
                    state = None
                    outside = not outside

        elif not outside:
            contained += 1

print("Part 2:", contained)

# total_area = ((max_x - min_x) + 2) * ((max_y - min_y) + 2)
# 
# def get_space_neighbours(ground, loop, point):
#     node = ground.get(point, ".")
#     for (dy, dx) in ((-1, 0), (0, 1), (1, 0), (0, -1)):
#         new_pos = (point[0] + dy, point[1] + dx)
#         if new_pos not in loop and min_y - 1 <= new_pos[0] <= max_y + 1 and min_x - 1 <= new_pos[1] <= max_x + 1 :
#             yield (point[0] + dy, point[1] + dx)

# def get_shoelace_area(loop):
#     total = []
#     for i in range(len(loop)):
#         total.append(loop[i][1] * (loop[(i+1)%len(loop)][0] - loop[(i-1)%len(loop)][0]))
#     return sum(total)/2

def get_shoelace_area(loop):
    return abs(sum([(loop[i][0] + loop[i+1][0])*(loop[i][1] - loop[i+1][1]) for i in range(len(loop)-1)]))/2
# 
# start_pos = (min_y-1, min_x-1)
# bfs_visited = set()
# queue = [start_pos]
# 
# while len(queue) > 0:0
#     current = queue.pop(0)
#     bfs_visited.add(current)
#     
#     for sn in get_space_neighbours(ground, visited, current):
#         if sn not in bfs_visited:
#             queue.append(sn)

print("Why??? From an observation on Reddit...")
print("Part 2: Shoelace area - (part 1) / 2 ->", get_shoelace_area(visited) - (len(visited) // 2) + 1)
