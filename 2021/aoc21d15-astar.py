from collections import defaultdict
from heapq import heappush, heappop
from time import time
import io

test_cavern = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""


def astar_guess(node, goal):
    # return the cityblock / manhattan distance
    return sum(abs(p1-p2) for p1, p2 in zip(node, goal))


def get_neighbours(cavern, node):
    cavern_height = len(cavern)
    cavern_width = len(cavern[0])
    
    for dx, dy in (-1,0), (1,0), (0,-1), (0,1):
        new_neighbour = (node[0]+dx, node[1]+dy)
        if 0 <= new_neighbour[0] < cavern_height:
            if 0 <= new_neighbour[1] < cavern_width:
                yield new_neighbour


def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.insert(0, current)
    return total_path


def cost(cavern, trace):
    total_cost = 0
    for step in trace[1:]:
        total_cost += cavern[step[0]][step[1]]
    print()
    return total_cost


def calculate_paths(map, start, goal, func):
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

        for friend in get_neighbours(map, current):
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


cavern = []
# with StringIO(test_cavern) as data:
with open("input15.txt") as data:
    for line in data:
        cavern.append([int(n) for n in line.strip()])

start = (0, 0) # row, column
target = (len(cavern)-1, len(cavern[0])-1)

begin = time()
path = reconstruct_path(calculate_paths(cavern, start, target, astar_guess), target)
if path:
    print(cost(cavern, path))
print("duration:", time() - begin)
