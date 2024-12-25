from collections import defaultdict
from functools import cache
from heapq import heappop, heappush
from io import StringIO


def get_neighbours(graph, point):
    x, y = point
    for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
        new_point = (x + dx, y + dy)
        if graph[new_point] != "#":
            yield new_point


@cache
def taxicab(point, goal):
    # return the cityblock / manhattan distance
    return sum(abs(p1 - p2) for p1, p2 in zip(point, goal))


def reconstruct_path(came_from, current):
    """Builds the full path of a successful A* calculation

    Args:
        came_from (_type_): A* shortest path data
        current (_type_): finishing point

    Returns:
        _type_: list of nodes desribing the calculated (shortest) path
    """
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.insert(0, current)
    return total_path


def a_star(graph, func, start, end):
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

        for neighbour in get_neighbours(graph, current):
            # d(current,neighbor) is the weight of the edge from current to neighbor
            # tentative_gScore is the distance from start to the neighbor through current
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score[neighbour]:
                # This path to neighbor is better than any previous one. Record it!
                came_from[neighbour] = current
                g_score[neighbour] = tentative_g_score
                friend_f_score = tentative_g_score + func(neighbour, end)
                f_score[neighbour] = friend_f_score
                heappush(open_set, (friend_f_score, neighbour))

    # Open set is empty but goal was never reached
    return


test = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""

racetrack = defaultdict(lambda: "#")
start = None
end = None
improvements = defaultdict(int)

# with StringIO(test) as input_data:
with open("input20.txt") as input_data:
    for y, row in enumerate(input_data):
        for x, ch in enumerate(row.strip()):
            if ch == "S":
                start = (x, y)
                racetrack[(x, y)] = "."
            elif ch == "E":
                end = (x, y)
                racetrack[(x, y)] = "."
            elif ch != "#":
                racetrack[(x, y)] = "."

max_X = x
max_Y = y

path = reconstruct_path(a_star(racetrack, taxicab, start, end), end)
# print(len(path), "->", path)
original_len = len(path)

visited = set()
for i, step in enumerate(path[1:]):
    if i % 10 == 0:
        print("Step", i, "of", original_len)

    x, y = step
    for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
        new_step = (x + dx, y + dy)
        if (
            racetrack[new_step] == "#"
            and new_step not in visited
            and 0 < new_step[0] < max_X
            and 0 < new_step[1] < max_Y
        ):
            visited.add(new_step)
            improvements[
                original_len
                - len(
                    reconstruct_path(
                        a_star(racetrack | {new_step: "."}, taxicab, start, end), end
                    )
                )
            ] += 1

print(sum([v for k, v in improvements.items() if k >= 100]))
