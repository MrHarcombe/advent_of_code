from collections import defaultdict
from io import StringIO

directions = {0: (0, -1), 1: (1, 0), 2: (0, 1), 3: (-1, 0)}


def get_neighbours(maze, point):
    x, y = point
    for direction in directions:
        dx, dy = directions[direction]
        new_point = (x + dx, y + dy)
        if maze.get(new_point, ".") != "#":
            yield new_point, direction


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

all_possible = []

queue = [[(start, 2)]]
# visited = set()
while len(queue) > 0:
    current_path = queue.pop(0)
    current, cur_dir = current_path[-1]
    # visited.add((current, cur_dir, prev_dir))

    if current == end:
        print("Found one:", calculate_path_cost(list(current_path)))
        all_possible.append(current_path)
    else:
        for neighbour, direction in get_neighbours(maze, current):
            if neighbour not in [step for step, _ in current_path]:
                new_path = list(current_path)
                new_path.append((neighbour, direction))
                queue.append(new_path)

print(all_possible)

# best_path = min([calculate_path_cost(path)] for path in all_possible)[0]
# print("Part 1:", best_path)

# for best in filter(lambda path: calculate_path_cost(path) <= best_path, all_possible):
#     print("Cost:", calculate_path_cost(best))
#     seats = {pos for pos, _, _ in best}
#     display_seats(MAX_X, MAX_Y, maze, start, end, seats)
#     print()

# display_seats(MAX_X, MAX_Y, maze, start, end, used_seats)
# print("Part 2:", len(used_seats))

# 138424 too high
# 137422 too high

# 422 too low
# 448 too low
