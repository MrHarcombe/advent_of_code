from collections import defaultdict
from heapq import heappop, heappush, heapify
from io import StringIO
from time import time

test = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""

# test = """11599
# 99199
# 99199
# 99199
# 99111"""

# test = """112999
# 911111"""

# test = """111111111111
# 999999999991
# 999999999991
# 999999999991
# 999999999991"""

##
# change to return all possible steps, ie 1, 2, or 3 steps in a single direction
# and not double back... so, at most 9 neighbours
#
# to save other calls, return the destination, direction, steps, and total cost
#

def get_neighbours_and_cost_1(graph, point, previous):
    for d, (dr, dc) in enumerate(((-1,0), (0,1), (1,0), (0,-1))):
        if previous == d or previous == (d + 2) % 4:
            # can't continue on or double back, as we've already provided all three steps forward as possibilities
            continue

        cost = 0
        for step in range(1, 4):
            new_point = (point[0] + step * dr, point[1] + step * dc)

            if new_point[0] not in range(graph["max_row"]+1) or new_point[1] not in range(graph["max_col"]+1):
                break

            cost += graph[new_point]
            yield new_point, d, cost

def get_neighbours_and_cost_2(graph, point, previous):
    for d, (dr, dc) in enumerate(((-1,0), (0,1), (1,0), (0,-1))):
        if previous == d or previous == (d + 2) % 4:
            # can't continue on or double back, as we've already provided all three steps forward as possibilities
            continue

        cost = 0
        for step in range(1, 11):
            new_point = (point[0] + step * dr, point[1] + step * dc)

            if new_point[0] not in range(graph["max_row"]+1) or new_point[1] not in range(graph["max_col"]+1):
                break

            cost += graph[new_point]
            if step > 3:
                yield new_point, d, cost

def manhattan_guess(node, goal):
    # return the cityblock / manhattan distance
    return sum(abs(p1-p2) for p1, p2 in zip(node, goal))

def a_star(graph, start, goal, f_neighbour, f_heuristic):
    start_details = (start, None)
    
    # The set of discovered nodes that may need to be (re-)expanded.
    # Initially, only the start node is known.
    # This is usually implemented as a min-heap or priority queue rather than a hash-set.
    # openSet = {start}
    open_set = []

    # For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from start
    # to n currently known.
    came_from = {start_details: (None, 0)}

    # For node n, gScore[n] is the cost of the cheapest path from start to n currently known.
    g_score = defaultdict(lambda: float('inf'))
    g_score[start_details] = 0

    # For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to
    # how short a path from start to finish can be if it goes through n.
    f_score = defaultdict(lambda: float('inf'))
    f_score[start_details] = f_heuristic(start, goal)

    heappush(open_set, (f_score[start_details], start_details))

    while len(open_set) > 0:
        # This operation can occur in O(1) time if openSet is a min-heap or a priority queue
        # current := the node in openSet having the lowest fScore[] value
        estimate, current_details = heappop(open_set)
        node, previous_direction = current_details

        # Don't go past the goal
        if node == goal:
            break
        
        else:
            for neighbour, direction, cost in f_neighbour(graph, node, previous_direction):
                sub_node = (neighbour, direction)

                # d(current, neighbour) is the weight of the edge from current to neighbour
                # tentative_gScore is the distance from start to the neighbour through current
                tentative_g_score = g_score[current_details] + cost
                if tentative_g_score < g_score[sub_node]:
                    # This path to neighbour is better than any previous one. Record it!
                    came_from[sub_node] = (current_details, tentative_g_score)
                    g_score[sub_node] = tentative_g_score
                    friend_f_score = tentative_g_score + f_heuristic(neighbour, goal)
                    f_score[sub_node] = friend_f_score

                    heappush(open_set, (friend_f_score, sub_node))

    paths = []
    possibles = [k for k in came_from if k[0] == end]
    for possible in possibles:
        a_path = []
        while possible != start and possible != None:
            a_path.append((possible, came_from[possible]))
            possible = came_from[possible][0]
        paths.append(a_path[::-1])
    
    return paths, came_from

def dijkstra(graph, start, end, neighbour_f):
    queue = []
    data = defaultdict(lambda: [float("inf"), None])
    data[(start, None, 0)] = [0, None]

    heappush(queue, (0, (start, None)))

    while len(queue) > 0:
        previous_cost, node_details = heappop(queue)
        node, previous_direction = node_details

        if node == end:
            break

        else:
            for neighbour, direction, cost in neighbour_f(graph, node, previous_direction):
                sub_node = (neighbour, direction)

                if previous_cost + cost < data[sub_node][0]:
                    data[sub_node][0] = previous_cost + cost
                    data[sub_node][1] = node_details

                    heappush(queue, (data[sub_node][0], sub_node))

    if end == None:
        return data

    paths = []
    possibles = [k for k in data if k[0] == end]
    for possible in possibles:
        a_path = []
        while possible != start and possible != None:
            a_path.append((possible,data[possible][0]))
            possible = data[possible][1]
        paths.append(a_path[::-1])
    
    return paths, data

city = {}
# with StringIO(test) as data:
with open("input17.txt") as data:
    for row, line in enumerate(data):
        for col, ch in enumerate(line.strip()):
            city[(row,col)] = int(ch)

city["max_row"] = row
city["max_col"] = col

start=(0,0)
end=(row,col)

now = time()
paths, workings = dijkstra(city, start, end, get_neighbours_and_cost_1)
print("Part 1:", min(path[-1][-1] for path in paths))
print("Elapsed:", time() - now)
# now = time()
# paths, _ = a_star(city, start, end, get_neighbours_and_cost_1, manhattan_guess)
# print("Part 1:", min(path[-1][1][-1] for path in paths))
# print("Elapsed:", time() - now)

now = time()
paths, workings = dijkstra(city, start, end, get_neighbours_and_cost_2)
print("Part 1:", min(path[-1][-1] for path in paths))
print("Elapsed:", time() - now)
# now = time()
# paths, _ = a_star(city, start, end, get_neighbours_and_cost_2, manhattan_guess)
# print("Part 2:", min(path[-1][1][-1] for path in paths))
# print("Elapsed:", time() - now)
