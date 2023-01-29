from io import StringIO
from itertools import permutations
from collections import defaultdict
from heapq import *

test = """Filesystem            Size  Used  Avail  Use%
/dev/grid/node-x0-y0   10T    8T     2T   80%
/dev/grid/node-x0-y1   11T    6T     5T   54%
/dev/grid/node-x0-y2   32T   28T     4T   87%
/dev/grid/node-x1-y0    9T    7T     2T   77%
/dev/grid/node-x1-y1    8T    0T     8T    0%
/dev/grid/node-x1-y2   11T    7T     4T   63%
/dev/grid/node-x2-y0   10T    6T     4T   60%
/dev/grid/node-x2-y1    9T    8T     1T   88%
/dev/grid/node-x2-y2    9T    6T     3T   66%"""

def parse_line(line):
    parts = line.split()
    return parts[0], int(parts[1][:-1]), int(parts[2][:-1]), int(parts[3][:-1])

def get_coordinate_from_name(name):
    _, x, y = name.split("-")
    return (int(x[1:]), int(y[1:]))

def manhattan_distance(point_a, point_b):
    return sum([abs(x - y) for x, y in zip(point_a, point_b)])

def a_star_guess(pos, goal):
    return 1 * manhattan_distance(pos, goal)

def find_neighbours(world, current):
    neighbours = []
    for dx, dy in ((-1, 0), (0, -1), (1, 0), (0, 1)):
        neighbour = (current[0] + dx, current[1] + dy)
        if neighbour in world and world[neighbour] != "#":
            neighbours.append(neighbour)
    return neighbours

def reconstruct_path(a_star_result, current):
    total_path = [current]
    while current in a_star_result:
        current = a_star_result[current]
        total_path.insert(0, current)
    return total_path

def calculate_a_star(world, start, goal, func):
    # The set of discovered nodes that may need to be (re-)expanded.
    # Initially, only the start node is known.
    # This is usually implemented as a min-heap or priority queue rather than a hash-set.
    # openSet = {start}
    open_set = []

    # For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from start
    # to n currently known.
    came_from = {}

    # For node n, gScore[n] is the cost of the cheapest path from start to n currently known.
    g_score = defaultdict(lambda: float('inf'))
    g_score[start] = 0

    # For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to
    # how short a path from start to finish can be if it goes through n.
    f_score = defaultdict(lambda: float('inf'))
    f_score[start] = func(start, goal)

    heappush(open_set, (f_score[start], start))

    while len(open_set) > 0:
        # This operation can occur in O(1) time if openSet is a min-heap or a priority queue
        # current := the node in openSet having the lowest fScore[] value
        current = heappop(open_set)[1]

        if current == goal:
            return came_from

        for friend in find_neighbours(world, current):
            # d(current, neighbour) is the weight of the edge from current to neighbour
            # tentative_gScore is the distance from start to the neighbour through current
            tentative_g_score = g_score[current] + 1 # every move only costs 1
            if tentative_g_score < g_score[friend]:
                # This path to neighbour is better than any previous one. Record it!
                came_from[friend] = current
                g_score[friend] = tentative_g_score
                friend_f_score = tentative_g_score + func(friend, goal)
                f_score[friend] = friend_f_score
                if friend not in open_set:
                    heappush(open_set, (friend_f_score, friend))

    # Open set is empty but goal was never reached
    return

def successors(node, goal, nodes):
    x,y = node
    print(node)
    possibles = []
    for change in ((-1,0), (1,0), (0,-1), (0,1)):
        new_x = x + change[0]
        new_y = y + change[1]
        if 0 <= new_x <= 2 and 0 <= new_y <= 2:
            print(new_x, new_y)
            if nodes[(x,y)][1] == 0 and nodes[(x,y)][0] >= nodes[(new_x, new_y)][1]:
                possibles.append((new_x, new_y))
#             if nodes[(new_x,new_y)][1] == 0 and nodes[(new_x,new_y)][0] >= nodes[(x, y)][1]:
#                 possibles.append((new_x, new_y))

    print(possibles)
    return possibles
    

"""
https://en.wikipedia.org/wiki/Iterative_deepening_A*

procedure ida_star(root)
    bound := h(root)
    path := [root]
    loop
        t := search(path, 0, bound)
        if t = FOUND then return (path, bound)
        if t = ∞ then return NOT_FOUND
        bound := t
    end loop
end procedure
"""
def ida_star(root, goal, nodes):
    bound = manhattan_distance(root, goal)
    path = [root]
    while True:
        t = search(path, 0, bound, goal, nodes)
        
        if t == True:
            return (path, bound)
        elif t == float("inf"):
            return False
        
        bound = t

"""
function search(path, g, bound)
    node := path.last
    f := g + h(node)
    if f > bound then return f
    if is_goal(node) then return FOUND
    min := ∞
    for succ in successors(node) do
        if succ not in path then
            path.push(succ)
            t := search(path, g + cost(node, succ), bound)
            if t = FOUND then return FOUND
            if t < min then min := t
            path.pop()
        end if
    end for
    return min
end function
"""
def search(path, g, bound, goal, nodes):
    node = path[-1]
    f = g + manhattan_distance(node, goal)
    
    if f > bound: return f
    if node == goal: return True
    
    minimum = float("inf")
    for s in successors(node, goal, nodes):
        if s not in path:
            path.append(s)
            t = search(path, g + 1, bound, goal, nodes | {node:nodes[s][1], s:nodes[node][1]})
            
            if t: return True
            if t < minimum: minimum = t
            
            path.pop()
    
    return minimum

def display_node(node):
    return f"({node[0]:2},{node[1]:2},{node[2]:2})"

def display_nodes(nodes):
    for y in range(max((y for x,y in nodes))+1):
        row = []
        for x in range(max((x for x,y in nodes))+1):
            row.append(display_node(nodes.get((x,y), (0, 0, 0))))
        print(" ".join(row))
    print()

def display_grid(grid):
    for y in range(max((y for x,y in grid))+1):
        row = []
        for x in range(max((x for x,y in grid))+1):
            row.append(grid.get((x,y), "#"))
        print(" ".join(row))
    print()

nodes = {}

# with StringIO(test) as f:
with open("input22.txt") as f:
    for line in f:
        if not line.startswith("/"):
            continue

        name, size, used, avail = parse_line(line)
        # print(name, used, avail)
        nodes[get_coordinate_from_name(name)] = (size, used, avail)

# print(len(nodes))
# count = 0
# for a,b in permutations(nodes,2):
#     if nodes[a][1] > 0 and nodes[a][1] <= nodes[b][2]:
#         count += 1
# print(count)

goal = (0,0)
target = (max((x for x,y in nodes if y == 0)), 0)
# print(goal, start)

need = nodes[goal][1]
grid = {}
for y in range(max((y for x,y in nodes))+1):
    for x in range(max((x for x,y in nodes))+1):
        # print((x,y))
        if (x,y) == target:
            grid[target] = "T"
        elif (x,y) == goal:
            grid[goal] = "G"
        elif (x,y) in nodes:
            if nodes[(x,y)][1] == 0:
                grid[(x,y)] = "_"
            elif nodes[(x,y)][1] > nodes[goal][0]:
                grid[(x,y)] = "#"
            else:
                assert(nodes[(x,y)][0] >= need)
                grid[(x,y)] = "."

# display_nodes(nodes)
display_grid(grid)
# print(ida_star((1,1), (0,0), nodes))

# 204, 205 too high (205 is someone else's answer)
# 199 too low

space = next((item[0] for item in grid.items() if item[1] == "_"))
print(space)
path = calculate_a_star(grid, space, (target[0]-1,target[1]), a_star_guess)
rp = reconstruct_path(path, (target[0]-1,target[1]))
print("Steps to move gap to left of target:", len(rp) - 1)
print("Places to cycle space and target node * 5:", (target[0] - 1 - goal[0]) * 5)
print("Plus 1 to move the target into final gap:", (len(rp) - 1) + ((target[0] - 1 - goal[0]) * 5) + 1)

# 34 to move the gap to the left of the target node, then 33 * 5 to move the target node along until the gap
# is on the goal node, then 1 more to move it into position = 200 YES!!
