from collections import defaultdict
from functools import cache
from heapq import heappop, heappush
from io import StringIO
from itertools import product


@cache
def get_neighbours(point):
    neighbours = []
    x, y = point
    for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
        new_point = (x + dx, y + dy)
        if racetrack[new_point] != "#":
            neighbours.append(new_point)
    return neighbours


@cache
def taxicab(point, goal):
    # return the cityblock / manhattan distance
    return sum(abs(p1 - p2) for p1, p2 in zip(point, goal))


def dijkstra(maze, start, end=None):
    queue = []
    data = defaultdict(lambda: [float("inf"), None])
    data[start] = [0, None]

    heappush(queue, (0, start))

    while len(queue) > 0:
        _, node = heappop(queue)

        if node == end:
            return data

        for neighbour in get_neighbours(node):
            # calculate cost
            alt = data[node][0] + 1
            if alt < data[neighbour][0]:
                data[neighbour][0] = alt
                data[neighbour][1] = node
                heappush(queue, (alt, neighbour))

    return data


def build_path(dijkstra_data, src, dest):
    path = [src]
    current = dest
    while current != src:
        path.insert(1, current)
        current = dijkstra_data[current][1]

    return path


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

original_data = dijkstra(racetrack, start, end)
path = build_path(original_data, start, end)
original_len = len(path)

reverse_data = dijkstra(racetrack, end)

# radius = 2 # part 1
radius = 20  # part 2

visited = set()
for i, step in enumerate(path):
    if i % 50 == 1:
        print("Step", i, "of", original_len)
    x, y = step
    for dx, dy in product(range(-radius, radius + 1), range(-radius, radius + 1)):
        new_step = (x + dx, y + dy)
        if (
            (step, new_step) not in visited
            and racetrack[new_step] != "#"
            and 0 < new_step[0] < max_X
            and 0 < new_step[1] < max_Y
            and 0 < taxicab(step, new_step) <= radius
        ):
            visited.add((step, new_step))
            saving = (
                original_len
                - (
                    original_data[step][0]
                    + taxicab(step, new_step)
                    + reverse_data[new_step][0]
                )
                - 1
            )
            # print("Saving", saving, "from", step, "to", new_step)
            improvements[saving] += 1

print(sum([v for k, v in improvements.items() if k >= 100]))
# print(sorted([(k, v) for k, v in improvements.items() if k >= 100]))
# print(sorted(visited))
