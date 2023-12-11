from io import StringIO
from math import ceil

test = """.....
.S-7.
.|.|.
.L-J.
....."""

test = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""

test = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""

connections = {"|" : "1010", "-" : "0101", "L" : "1100", "J" : "1001", "7" : "0011", "F" : "0110" }
directions = "NESW"

def display_groundmap(ground, miny, maxy, minx, maxx):
    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            print(ground.get((y,x), " "), end="")
        print()
    print()

def get_start_neighbours(ground, start):
    for d, (dy, dx) in enumerate(((-1, 0), (0, 1), (1, 0), (0, -1))):
        for node, nd in get_neighbours(ground, (start[0] + dy, start[1] + dx)):
            if node == start:
                yield ((start[0] + dy, start[1] + dx), directions[d])

def get_neighbours(ground, point):
    node = ground.get(point, ".")
    if node in connections:
        cx = connections[node]
        for d, (dy, dx) in enumerate(((-1, 0), (0, 1), (1, 0), (0, -1))):
            if cx[d] == "1":
                yield ((point[0] + dy, point[1] + dx), directions[d])


ground = {}
start = None

with StringIO(test) as data:
# with open("input10.txt") as data:
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
next_step, direction = next_steps[0]

while next_step != None:
    current = next_step
    visited.append(current)
    next_steps = [(node, d) for node, d in get_neighbours(ground, current) if node not in visited]
    if len(next_steps) > 0:
        next_step = next_steps[0][0]
        direction = next_steps[0][1]
    else:
        next_step, direction = None, None

print("Part 1:", ceil(len(visited)/2))

# visited now contains the perimeter... 
# start is the starting point...

#... so as long as I know which way I'm going (from the piece) I can
# then scan perpendicular until I either fall off the edge, or I hit
# the next piece of perimeter and add those co-ordinates to a set of
# internal pieces

# current = start
# next_steps = [n for n in get_start_neighbours(ground, start)] 
# next_step, direction = next_steps[0]

# or, plan C, try performing a breadth-first on the known area,
# stopping at perimeter edges...
# then calclculate the remaining area as the total amount covered
# by the pipe and interior, so subtract the length of the pipe...

total_area = ((max_x - min_x) + 2) * ((max_y - min_y) + 2)

def get_space_neighbours(ground, loop, point):
    node = ground.get(point, ".")
    if node in connections:
        for (dy, dx) in enumerate((-1, 0), (0, 1), (1, 0), (0, -1)):
            new_pos = (point[0] + dy, point[1] + dx)
            if new_pos not in loopand min_y - 1 <= new_pos[1] <= max_y + 1 and min_x - 1 <= new_pos[1] <= max_x + 1 :
                yield (point[0] + dy, point[1] + dx)

start_pos = (min_y - 1, min_x - 1)
bfs_visited = set()
queue = [start_pos]

while len(queue) > 0:
    current = queue.pop(0)
    bfs_visited.add(current)
    
    for sn in get_space_neighbours(ground, visited, current):
        if sn not in bfs_visited:
            queue.append(sn)

print("Part 2:", total_area, len(visited), len(bfs_visited), total_area - len(visited) - len(bfs_visited))
