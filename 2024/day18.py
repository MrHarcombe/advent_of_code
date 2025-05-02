from collections import defaultdict
from heapq import heappop, heappush
from io import StringIO


def get_neighbours(memory, point):
    x, y = point
    for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
        new_point = (x + dx, y + dy)
        if (
            0 <= new_point[0] <= 70  # 6
            and 0 <= new_point[1] <= 70  # 6
            and memory[new_point] != "#"
        ):
            yield new_point


def taxicab(point, goal):
    # return the cityblock / manhattan distance
    return sum(abs(p1 - p2) for p1, p2 in zip(point, goal))


def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.insert(0, current)
    return total_path


def a_star(memory, func, start, end):
    # The set of discovered nodes that may need to be (re-)expanded.
    # Initially, only the start node is known.
    # This is usually implemented as a min-heap or priority queue rather than a hash-set.
    # openSet = {start}
    open_set = []

    # For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from start
    # to n currently known.
    came_from = {}

    # For node n, gScore[n] is the cost of the cheapest path from start to n currently known.
    g_score = defaultdict(lambda: float("inf"))
    g_score[start] = 0

    # For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to
    # how short a path from start to finish can be if it goes through n.
    f_score = defaultdict(lambda: float("inf"))
    f_score[start] = func(start, end)

    heappush(open_set, (f_score[start], start))

    while len(open_set) > 0:
        # This operation can occur in O(1) time if openSet is a min-heap or a priority queue
        # current := the node in openSet having the lowest fScore[] value
        current = heappop(open_set)[1]

        if current == end:
            return came_from

        for friend in get_neighbours(memory, current):
            # d(current,neighbor) is the weight of the edge from current to neighbor
            # tentative_gScore is the distance from start to the neighbor through current
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score[friend]:
                # This path to neighbor is better than any previous one. Record it!
                came_from[friend] = current
                g_score[friend] = tentative_g_score
                friend_f_score = tentative_g_score + func(friend, end)
                f_score[friend] = friend_f_score
                heappush(open_set, (friend_f_score, friend))

    # Open set is empty but goal was never reached
    return


test = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""

start = (0, 0)
# end = (6, 6)
end = (70, 70)

memory = defaultdict(lambda: ".")
# with StringIO(test) as input_data:
with open("input18.txt") as input_data:
    for count in range(1024):
        line = input_data.readline()
        x, y = map(int, line.strip().split(","))
        memory[(x, y)] = "#"

    result = a_star(memory, taxicab, start, end)
    # print(result)
    path = reconstruct_path(result, end)
    # print(len(path), path[0])
    print("Part 1:", len(path) - 1)

    for line in input_data:
        x, y = map(int, line.strip().split(","))
        memory[(x, y)] = "#"

        result = a_star(memory, taxicab, start, end)
        if result is None:
            print("Part 2:", x, y)
            break
