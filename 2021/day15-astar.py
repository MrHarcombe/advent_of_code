from collections import defaultdict
from scipy.spatial.distance import cityblock
from heapq import heappush, heappop
import io
import time

test = '''1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581'''


def astar_guess(node, goal):
    # print(f'guessing from {node} to {goal} as {6 * cityblock(node, goal)}')
    return 1 * cityblock(node, goal)


def new_n(n, x, y):
    new_n = n + x + y
    if new_n <= 9:
        return new_n
    else:
        return new_n - 9


def identify_neighbours(map, row, col):
    neighbours = []
    if row > 0:
        neighbours.append((row-1, col))
    if col > 0:
        neighbours.append((row, col-1))
    if col < len(map[0]) - 1:
        neighbours.append((row, col+1))
    if row < len(map) - 1:
        neighbours.append((row+1, col))

    return neighbours


###
# A-Star pseudocode (from Wikipedia)
# 
# function reconstruct_path(cameFrom, current)
#     total_path := {current}
#     while current in cameFrom.Keys:
#         current := cameFrom[current]
#         total_path.prepend(current)
#     return total_path
# 
# // A* finds a path from start to goal.
# // h is the heuristic function. h(n) estimates the cost to reach goal from node n.
# function A_Star(start, goal, h)
#     // The set of discovered nodes that may need to be (re-)expanded.
#     // Initially, only the start node is known.
#     // This is usually implemented as a min-heap or priority queue rather than a hash-set.
#     openSet := {start}
# 
#     // For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from start
#     // to n currently known.
#     cameFrom := an empty map
# 
#     // For node n, gScore[n] is the cost of the cheapest path from start to n currently known.
#     gScore := map with default value of Infinity
#     gScore[start] := 0
# 
#     // For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to
#     // how short a path from start to finish can be if it goes through n.
#     fScore := map with default value of Infinity
#     fScore[start] := h(start)
# 
#     while openSet is not empty
#         // This operation can occur in O(1) time if openSet is a min-heap or a priority queue
#         current := the node in openSet having the lowest fScore[] value
#         if current = goal
#             return reconstruct_path(cameFrom, current)
# 
#         openSet.Remove(current)
#         for each neighbor of current
#             // d(current,neighbor) is the weight of the edge from current to neighbor
#             // tentative_gScore is the distance from start to the neighbor through current
#             tentative_gScore := gScore[current] + d(current, neighbor)
#             if tentative_gScore < gScore[neighbor]
#                 // This path to neighbor is better than any previous one. Record it!
#                 cameFrom[neighbor] := current
#                 gScore[neighbor] := tentative_gScore
#                 fScore[neighbor] := tentative_gScore + h(neighbor)
#                 if neighbor not in openSet
#                     openSet.add(neighbor)
# 
#     // Open set is empty but goal was never reached
#     return failure

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.insert(0, current)
    return total_path


def calculate_paths(map, start, goal, func):
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

    heappush(open_set, (f_score[start], start))

    while len(open_set) > 0:
        # This operation can occur in O(1) time if openSet is a min-heap or a priority queue
        # current := the node in openSet having the lowest fScore[] value
        current = heappop(open_set)[1]

        # print('considering', current)
        if current == goal:
            # print('at goal')
            return came_from

        for friend in identify_neighbours(map, current[0], current[1]):
            # d(current,neighbor) is the weight of the edge from current to neighbor
            # tentative_gScore is the distance from start to the neighbor through current
            tentative_g_score = g_score[current] + map[current[0]][current[1]]
            if tentative_g_score < g_score[friend]:
                # This path to neighbor is better than any previous one. Record it!
                came_from[friend] = current
                g_score[friend] = tentative_g_score
                friend_f_score = tentative_g_score + func(friend, goal)
                f_score[friend] = friend_f_score
                if friend not in open_set:
                    heappush(open_set, (friend_f_score, friend))

    # Open set is empty but goal was never reached
    return


def cost(map, trace):
    total_cost = 0
    for step in trace.values():
        # print(map[step[0]][step[1]], end=" ")
        total_cost += map[step[0]][step[1]]
    print()
    return total_cost

cave = []
megacave = []

# with io.StringIO(test) as inputs:
with open('input15.txt') as inputs:
    for line in inputs:
        row = [int(n) for n in list(line.strip())]
        cave.append(row)


for y in range(5):
    for row in cave:
        megarow = []
        for x in range(5):
            megarow += [new_n(n, x, y) for n in row]
        megacave.append(megarow)

# print(cave)
# print(megacave)

trace = calculate_paths(cave, (0, 0), (len(cave)-1, len(cave[0])-1), astar_guess)
if trace:
    # print(((len(cave)-1),len(cave[0])-1),'->',trace[((len(cave)-1),len(cave[0])-1)])
    print(cost(cave, trace))

# tic = time.perf_counter()
# path = calculate_paths(megacave, (0, 0), (len(megacave)-1, len(megacave[0])-1), astar_guess)
# toc = time.perf_counter()
# if path:
#     trace = reconstruct_path(path, (len(megacave)-1, len(megacave[0])-1))
#     # print(((len(megacave)-1),len(megacave[0])-1),'->',trace[((len(megacave)-1),len(megacave[0])-1)])
#     print(cost(megacave, trace))
#     tac = time.perf_counter()
#     print(f"Completed in {toc - tic:0.4f}, then {tac - toc:0.4f} seconds")

# current = trace[((len(cave)-1),len(cave[0])-1)]
# while current[1] != (0,0):
#     print(current[1], '->',trace[current[1]])
#     current = trace[current[1]]
