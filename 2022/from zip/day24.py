from io import StringIO
from collections import defaultdict
from copy import deepcopy

# test = """#.#####
# #.....#
# #>....#
# #.....#
# #...v.#
# #.....#
# #####.#"""

# test = """#.#####
# #.....#
# #<....#
# #.....#
# #...^.#
# #.....#
# #####.#"""

test = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#""" # expect 18

# test = """#.#####
# #>>>..#
# #<<<.<#
# #>.>>>#
# #####.#""" # expect 9

# def move_blizzards(valley):
#     new_valley = deepcopy(empty_valley)
#     for coord, things in [(c, t) for (c, t) in valley.items() if len(t) > 1]:
#         for thing in list(things):
#             if thing == '<':
#                 if coord[0] == min(valley, key=lambda i:i[0])[0]:
#                     left = (max(valley, key=lambda i:i[0])[0], coord[1])
#                 else:
#                     left = (coord[0]-1, coord[1])
#                 new_valley[left] += [thing]
# 
#             elif thing == '^':
#                 if coord[1] == min(valley, key=lambda i:i[1])[1]+1:
#                     up = (coord[0], max(valley, key=lambda i:i[1])[1]-1)
#                 else:
#                     up = (coord[0], coord[1]-1)
#                 new_valley[up] += [thing]
#                 
#             elif thing == '>':
#                 if coord[0] == max(valley, key=lambda i:i[0])[0]:
#                     right = (min(valley, key=lambda i:i[0])[0], coord[1])
#                 else:
#                     right = (coord[0]+1, coord[1])
#                 new_valley[right] += [thing]
#             
#             elif thing == 'v':
#                 if coord[1] == max(valley, key=lambda i:i[1])[1]-1:
#                     down = (coord[0], min(valley, key=lambda i:i[1])[1]+1)
#                 else:
#                     down = (coord[0], coord[1]+1)
#                 new_valley[down] += [thing]
# 
#     return new_valley

display_delta = { (-1,0): "<", (0,-1): "^", (1,0): ">", (0,1): "v" }

def get_valley_state(valley, turns):
    new_valley = defaultdict(list)
    for (dx, dy), blizzards in (item for item in valley.items() if len(item[0]) == 2):
        for bx, by in blizzards:
            nx = (((bx -1) + turns * dx) % valley["max_col"]) + 1
            ny = (((by -1) + turns * dy) % valley["max_row"]) + 1
            new_valley[(nx,ny)].append(display_delta[(dx,dy)])
    return new_valley

def manhattan_distance(point_a, point_b):
    result = sum([abs(x - y) for x, y in zip(point_a, point_b)])
    return result

def get_neighbours(valley, position, depth, cache):
    if (position,depth) in cache:
        return cache[(position,depth)]
    
    state = get_valley_state(valley, depth+1)

    neighbours = []
    for delta in ((-1,0),(0,-1),(1,0),(0,1),(0,0)):
        possible = (position[0]+delta[0], position[1]+delta[1])
        if possible not in state:
            if possible == valley["start"] or possible == valley["goal"]:
                neighbours.append(possible)
            elif 0 < possible[0] <= valley["max_col"]:
                if 0 < possible[1] <= valley["max_row"]:
                    neighbours.append(possible)

    neighbours.sort(key=lambda i:manhattan_distance(i, goal))
    cache[(position,depth)] = neighbours
    return neighbours

def depth_first(valley, start, goal):
    stack = [(start, 0)]

    while len(stack) > 0:
        current_pos, current_depth = stack.pop()

        if current_pos == goal:
            yield current_depth

        for neighbour in get_neighbours(valley, current_pos, current_depth):
            stack.append((neighbour, current_depth+1))

def breadth_first(valley, start, goal, turn=0):
    cache = {}
    discovered = set()
    queue = [(start, turn)]

    while len(queue) > 0:
        # queue.sort(key=lambda i:manhattan_distance(i[0][-1], goal)) # sort by closest to the goal
        current_pos, current_turn = queue.pop(0)

        if current_pos == goal:
            return current_turn, current_pos

        for neighbour in get_neighbours(valley, current_pos, current_turn, cache):
            if (neighbour, current_turn+1) not in discovered:
                queue.append((neighbour, current_turn+1))
                discovered.add((neighbour, current_turn+1))

def breadth_first_with_path(valley, start, goal, turn=0):
    cache = {}
    visited = set()
    queue = [([start], turn)]

    while len(queue) > 0:
        # queue.sort(key=lambda i:manhattan_distance(i[0][-1], goal)) # sort by closest to the goal
        current_path, current_turn = queue.pop(0)
        current_pos = current_path[-1]

        visited.add((current_pos, current_turn))

        if current_pos == goal:
            return current_turn, current_path

        neighbours = get_neighbours(valley, current_pos, current_turn, cache)
        for neighbour in neighbours:
            if (neighbour, current_turn+1) not in visited:
                new_path = list(current_path)
                new_path.append(neighbour)
                queue.append((new_path, current_turn+1))

def display_valley(valley, state, position, start, goal):
    for j in range(0, valley["max_row"]+2):
        row = []
        for i in range(0, valley["max_col"]+2):
            if (i,j) == position:
                row.append("E")
            elif (i,j) == start:
                row.append("S")
            elif (i,j) == goal:
                row.append("G")
            elif (i,j) in state:
                if len(state[(i,j)]) == 1:
                    row.append(state[(i,j)][0])
                else:
                    row.append(str(len(state[(i,j)])))
            elif 0 < i <= valley["max_col"] and 0 < j <= valley["max_row"]:
                row.append(".")
            else:
                row.append("#")
        print("".join(row))
    print()

start = None
goal = None
valley = defaultdict(list)

# with StringIO(test) as f:
with open("input24.txt") as f:
    row = 0
    for line in f:
        for col, ch in enumerate(line.strip()):
            if ch == "<":
                valley[(-1,0)] += [(col,row)]
            elif ch == ">":
                valley[(1,0)] += [(col,row)]
            elif ch == "^":
                valley[(0,-1)] += [(col,row)]
            elif ch == "v":
                valley[(0,1)] += [(col,row)]

            if ch == ".":
                if row == 0:
                    start = (col, row)
                else:
                    goal = (col, row)
        row += 1

    valley["start"] = start
    valley["goal"] = goal

    # assumption, but seems safe
    valley["min_col"] = 0
    valley["max_col"] = goal[0]
    valley["min_row"] = start[1] + 1
    valley["max_row"] = goal[1] - 1

# turn = 0
# while True:
#     state = get_valley_state(valley, turn)
#     display_valley(valley, state, None, start, goal)
#     turn += 1
#     input()

initial, _ = breadth_first(valley, start, goal)
# for turn, step in enumerate(path):
#     state = get_valley_state(valley, turn)
#     display_valley(valley, state, step, start, goal)
#     input()
print("Time at goal:", initial)

reverse, _ = breadth_first(valley, goal, start, initial)
print("Time when back at start:", reverse)
final, _ = breadth_first(valley, start, goal, reverse)
print("Time when finally at goal:", final)

## 332 too high :(
## 288 FTW !!
