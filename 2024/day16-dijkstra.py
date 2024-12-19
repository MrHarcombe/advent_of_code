from collections import defaultdict
from heapq import heappop, heappush
from io import StringIO

directions = {0: (0, -1), 1: (1, 0), 2: (0, 1), 3: (-1, 0)}


def get_neighbours(maze, point):
    x, y = point
    for direction in directions:
        dx, dy = directions[direction]
        new_point = (x + dx, y + dy)
        if maze.get(new_point, ".") != "#":
            yield new_point, direction


def dijkstra(maze, start, end=None):
    queue = []
    data = defaultdict(lambda: [float("inf"), None])
    data[(start, 1)] = [0, None]

    heappush(queue, (0, start, 1))

    while len(queue) > 0:
        _, node, last_direction = heappop(queue)

        if node == end:
            break

        for neighbour, direction in get_neighbours(maze, node):
            # calculate cost
            cost = 1 if direction == last_direction else 1001
            alt = data[(node, last_direction)][0] + cost
            if alt < data[(neighbour, direction)][0]:
                data[(neighbour, direction)][0] = alt
                data[(neighbour, direction)][1] = (node, last_direction)
                heappush(queue, (alt, neighbour, direction))

    return data


def calculate_path_cost(path):
    cost = 0
    _, prev = path.pop(0)
    for step in path:
        _, cur = step
        if cur != prev:
            cost += 1000
        cost += 1
        prev = cur
    return cost


def display_path(maze_width, maze_height, maze, start, end, path_data):
    path = []
    current = end
    while current[0] != start:
        current = path_data[current][1]
        path.insert(0, current[0])
    # print(path)

    for y in range(maze_height + 1):
        row = []
        for x in range(maze_width + 1):
            if (x, y) == end:
                row.append("E")
            if (x, y) == start:
                row.append("S")
            elif (x, y) in path:
                row.append("O")
            elif (x, y) in maze:
                row.append("#")
            else:
                row.append(".")

        print("".join(row))
    print()


def display_seats(maze_width, maze_height, maze, start, end, seats):
    for y in range(maze_height + 1):
        row = []
        for x in range(maze_width + 1):
            if (x, y) == end:
                row.append("E")
            elif (x, y) == start:
                row.append("S")
            elif (x, y) in seats:
                row.append("O")
            elif (x, y) in maze:
                row.append("#")
            else:
                row.append(".")

        print("".join(row))
    print()


test = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""

maze = defaultdict(lambda: ".")
start = None
end = None

# with StringIO(test) as input_data:
with open("input16.txt") as input_data:
    for y, row in enumerate(input_data):
        for x, ch in enumerate(row.strip()):
            if ch == "#":
                maze[(x, y)] = ch
            elif ch == "S":
                start = (x, y)
            elif ch == "E":
                end = (x, y)

MAX_Y = y
MAX_X = x

data = dijkstra(maze, start)
min_possible = min(
    [(d, data[(end, d)]) for d in directions], key=lambda item: item[1][0]
)
print(min_possible)
print("Part 1:", min_possible[1][0])

# now, for the path that is the minimum, retrace it and at each place on the path that has an alternative
# try taking that path with Dijkstra and checking the cost from there to the endpoint...

path = [(start, 2)]
current = (end, min_possible[0])
while current[0] != start:
    path.insert(1, current)
    current = data[current][1]

seats = {step for step, _ in path}
for step in range(1, len(path) - 1):
    current = path[step]
    next = path[step + 1]
    cost_to_here = data[step][0]
    x, y = path[step][0]
    for d in directions:
        dx, dy = directions[d]
        possible_next = (x + dx, y + dy)
        if maze[possible_next] != "#" and d != next:
            alt_data = dijkstra(maze, possible_next, end)

# display_path(MAX_X, MAX_Y, maze, start, min_possibles[1], data)

# all_matching = []

# queue = [([(start, 2)], set())]
# while len(queue) > 0:
#     current_path, visited = queue.pop(0)
#     current, cur_dir = current_path[-1]

#     path_cost = calculate_path_cost(list(current_path))
#     if path_cost > min_possibles[0]:
#         print("Discarding path:", path_cost)
#         continue

#     if current == end:
#         print("Found one")
#         all_matching.append(current_path)

#     else:
#         for neighbour, direction in get_neighbours(maze, current):
#             # if (neighbour, direction) not in current_path:
#             if neighbour not in visited:
#                 new_path = list(current_path)
#                 new_path.append((neighbour, direction))
#                 queue.append((new_path, visited | {neighbour}))

# seats = set()
# for path in all_matching:
#     for step, _ in path:
#         seats.add(step)

# print("Part 2:", len(seats))

# alternatives = []

# stack = [[(start, 2, 0)]]
# visited = set()

# while len(stack) > 0:
#     current_path = stack.pop()
#     current, prev_dir, cost = current_path[-1]
#     if current == end and cost <= min_possibles:
#         print("Found:", current_path)
#         alternatives.append(current_path)

#     elif cost > min_possibles:
#         # print("Ignoring expensive path:", cost)
#         pass

#     else:
#         for neighbour, direction in get_neighbours(maze, current):
#             step_cost = 1 if direction == prev_dir else 1001
#             if (
#                 neighbour,
#                 direction,
#             ) not in visited:
#                 new_path = list(current_path)
#                 new_path.append([neighbour, direction, cost + step_cost])
#                 stack.append(new_path)

# print(len(alternatives))

# print(data)
# display_path(MAX_X, MAX_Y, maze, start, end, data)

# part 2 requires backtracking along the path, finding all possibles at each step that have the smallest cost
# and following those back to the start

# seats = set()
# seats.add(end)
# seats.add(start)

# possibles = [data[(end, d)] for d in directions]
# cost, last = min(possibles, key=lambda item: item[0])
# queue = [last]
# while len(queue) > 0:
#     current = queue.pop(0)
#     seats.add(current)
#     possibles = [data[(current, d)] for d in directions]
#     value = min(possibles, key=lambda item: item[0])[0]
#     lowest = filter(lambda item: item[0] == value, possibles)
#     for _, pos in lowest:
#         if pos != start:
#             queue.append(pos)

# print("Part 2:", len(seats))
# display_seats(MAX_X, MAX_Y, maze, start, end, seats)

# 138424 too high
# 111488 too high
