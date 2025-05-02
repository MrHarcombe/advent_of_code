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


def dijkstra(maze, start, start_dir=1, reverse=False):
    queue = []
    data = defaultdict(lambda: [float("inf"), None])
    data[(start, start_dir)] = [0, None]

    heappush(queue, (0, start, start_dir))

    while len(queue) > 0:
        _, node, last_direction = heappop(queue)

        for neighbour, direction in get_neighbours(maze, node):
            new_direction = direction
            if reverse:
                new_direction = (direction + 2) % 2
            # calculate cost
            cost = 1 if new_direction == last_direction else 1001
            alt = data[(node, last_direction)][0] + cost
            if alt < data[(neighbour, new_direction)][0]:
                data[(neighbour, new_direction)][0] = alt
                data[(neighbour, new_direction)][1] = (node, last_direction)
                heappush(queue, (alt, neighbour, new_direction))

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
            elif (x, y) == start:
                row.append("S")
            elif (x, y) in path:
                row.append("O")
            elif (x, y) in maze:
                row.append(maze[(x, y)])
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
                row.append(maze[(x, y)])
            else:
                row.append(".")

        print("".join(row))
    print()


test = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""


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

# display_seats(MAX_X, MAX_Y, maze, start, end, set())

data = dijkstra(maze, start)
min_possible = min(
    [(d, data[(end, d)]) for d in directions], key=lambda item: item[1][0]
)
# print(min_possible)
print("Part 1:", min_possible[1][0])


def build_path(dijkstra_data, src, dest):
    path = [src]
    current = dest
    while current[0] != src[0]:

        path.insert(1, current)
        current = dijkstra_data[current][1]
    return path


# now, for the path that is the minimum, retrace it and at each place on the path that has an alternative
# try checking the minimum cost *from the endpoint* back to there...

###
# first, build the (well, *a*) shortest path
#
path = build_path(data, (start, 2), (end, min_possible[0]))
# display_seats(MAX_X, MAX_Y, maze, start, end, {step for step, _ in path})

###
# then, engineer the reverse paths
#
reverse_data = dijkstra(maze, end, min_possible[0], True)

###
# now, for each step along the path, check for a turn not taken and look at the cheapest cost in
# the reverse paths to that point to scope out an alternative route
#
seats = {step for step, _ in path}
for step in range(1, len(path) - 1):
    current = path[step]
    next = path[step + 1]
    cost_to_here = data[current][0]
    x, y = path[step][0]
    for d in directions:
        dx, dy = directions[d]
        possible_next = (x + dx, y + dy)
        if maze[possible_next] != "#" and d != next[1] and d != ((next[1] + 2) % 4):
            lowest_alternative = min(
                [(pnd, reverse_data[(possible_next, pnd)]) for pnd in directions],
                key=lambda item: item[1][0],
            )
            alt_dir, (alt_cost, _) = lowest_alternative
            if (alt_cost + cost_to_here) in (
                min_possible[1][0] - 1,
                min_possible[1][0] - 1001,
            ):
                alt_path = build_path(
                    reverse_data, (end, min_possible[0]), (possible_next, alt_dir)
                )
                seats |= {step for step, _ in alt_path}

#   display_seats(MAX_X, MAX_Y, maze, start, end, seats)
print("Part 2:", len(seats))

# 138424 too high
# 111488 too high

# 481 too low
