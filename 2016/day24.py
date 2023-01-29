from io import StringIO
from itertools import permutations
from collections import defaultdict
from heapq import *

def manhattan_distance(pa, pb):
    return abs(pa.real - pb.real) + abs(pa.imag - pb.imag)

def a_star_guess(pos, goal):
    return 1 * manhattan_distance(pos, goal)

def find_neighbours(world, current):
    neighbours = []
    for dx, dy in ((-1, 0), (0, -1), (1, 0), (0, 1)):
        neighbour = complex(current.real + dx, current.imag + dy)
        if neighbour in world:
            neighbours.append(neighbour)
    return neighbours

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.insert(0, current)
    return total_path

def calculate_a_star(world, start, goal, func):
    # print(start, goal)

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

    heappush(open_set, (f_score[start], start.real, start.imag, start))

    while len(open_set) > 0:
        # This operation can occur in O(1) time if openSet is a min-heap or a priority queue
        # current := the node in openSet having the lowest fScore[] value
        current = heappop(open_set)[3]

        # print('considering', current)
        if current == goal:
            # print('at goal')
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
                    heappush(open_set, (friend_f_score, friend.real, friend.imag, friend))

    # Open set is empty but goal was never reached
    return

def display_ducts():
    for y in range(int(max(ducts, key=lambda i:i.imag).imag+2)):
        row = []
        for x in range(int(max(ducts, key=lambda i:i.real).real+2)):
            target = [target for target in targets.items() if target[1] == complex(x,y)]
            if len(target) > 0:
                row.append(target[0][0])
            else:
                row.append(ducts.get(complex(x,y), "#"))
        print("".join(row))
    print()

test = """###########
#0.1.....2#
#.#######.#
#4.......3#
###########"""

start = None
ducts = {}
targets = {}

# with StringIO(test) as f:
with open("input24.txt") as f:
    y = 0
    for row in f:
        for x, cell in enumerate(row.strip()):
            if cell != '#':
                ducts[complex(x, y)] = "."
            if cell.isdigit() and cell != "0":
                targets[cell] = complex(x, y)
            if cell == "0":
                start = complex(x,y)
        y += 1

display_ducts()
print(start)
print(targets)

routes = []
cache = {}
for route in permutations(targets, len(targets)):
    position = start
    route_length = 0
    for stop in route:
        if (position, targets[stop]) in cache:
            hop = cache[(position, targets[stop])]

        else:
            path = calculate_a_star(ducts, position, targets[stop], a_star_guess)
            hop = len(reconstruct_path(path, targets[stop])) - 1
            cache[(position, targets[stop])] = hop
        
        route_length += hop
        position = targets[stop]

    # part 2 - finish at the start
    if (position, start) in cache:
        hop = cache[(position, start)]

    else:
        path = calculate_a_star(ducts, position, start, a_star_guess)
        hop = len(reconstruct_path(path, start)) - 1
        cache[(position, start)] = hop
    
    route_length += hop

    # print(",".join(route), "->", route_length)
    routes.append((route_length, ",".join(route)))

print(min(routes)[1], "->", min(routes)[0])
