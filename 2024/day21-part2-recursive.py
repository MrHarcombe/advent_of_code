from collections import defaultdict
from functools import cache
from heapq import heappop, heappush
from io import StringIO
from itertools import pairwise

directions = {1: (0, -1), 3: (1, 0), 2: (0, 1), 0: (-1, 0)}
direction_indicators = {1: "^", 3: ">", 2: "v", 0: "<"}


class HashableDict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))

    @cache
    def key_of_value(self, v):
        return next(ik for ik, iv in self.items() if iv == v)


@cache
def get_neighbours(grid, point):
    neighbours = []
    x, y = point
    for dir, step in directions.items():
        dx, dy = step
        new_point = (x + dx, y + dy)
        if grid.get(new_point, None) is not None:
            neighbours.append((new_point, dir))
    return neighbours


@cache
def bfs(grid, start, end):
    queue = [[start]]
    visited = set()
    paths = []

    while len(queue) > 0:
        current_path = queue.pop(0)
        current_node = current_path[-1]
        visited.add(current_node)

        if current_node == end:
            paths.append(tuple(current_path))

        else:
            for neighbour, _ in get_neighbours(grid, current_node):
                if neighbour not in visited:
                    new_path = list(current_path) + [current_node]
                    queue.append(new_path)

    return tuple(paths)


@cache
def dijkstra(grid, start, end=None):
    queue = []
    data = defaultdict(lambda: [float("inf"), None, None])
    data[start] = [0, None, None]

    heappush(queue, (0, start, 3))

    while len(queue) > 0:
        _, node, prev = heappop(queue)

        if node == end:
            break

        for neighbour, dir in get_neighbours(grid, node):
            # cost = 0.1 if dir == 3 else 0.11 if dir in (1, 2) else 0.111
            alt = data[node][0] + 1  # cost
            if alt < data[neighbour][0]:
                data[neighbour][0] = alt
                data[neighbour][1] = node
                data[neighbour][2] = dir
                heappush(queue, (alt, neighbour, dir))

    return HashableDict({k: tuple(data[k]) for k in data})


@cache
def refine_path(grid, dijkstra_result, start, end):
    path = []
    current = end
    while current != start:
        path.append(
            (
                current,
                dijkstra_result[current][2],
            )
        )
        current = dijkstra_result[current][1]

    if grid == direct_grid and start[1] == 3 and end[0] == 3:
        # do up/down then left/right
        # sort as UDLR
        path.sort(key=lambda item: (1, 2, 0, 3).index(item[1]))

    elif grid == direct_grid and start[0] == 0 and end[1] == 3:
        # do left/right then up/down
        # sort as LRUD
        path.sort(key=lambda item: (0, 3, 1, 2).index(item[1]))

    elif grid == indirect_grid and start[0] == 0:
        # do left/right then up/down
        # sort as LRUD
        path.sort(key=lambda item: (0, 3, 1, 2).index(item[1]))

    elif grid == indirect_grid and end[0] == 0:
        # do up/down then left/right
        # sort as UDLR
        path.sort(key=lambda item: (1, 2, 0, 3).index(item[1]))

    elif 0 in [dir for step, dir in path]:
        # sort as LRUD
        path.sort(key=lambda item: (0, 3, 1, 2).index(item[1]))

    else:
        # sort as UDLR
        path.sort(key=lambda item: (1, 2, 0, 3).index(item[1]))

    return "".join([direction_indicators[step[1]] for step in path])


def calculate_path_length(input_path, levels):
    @cache
    def build_grid_path(start, end, level):
        if level == 0:
            grid = direct_grid
        else:
            grid = indirect_grid

        process_path = (
            refine_path(
                grid,
                dijkstra(
                    grid,
                    grid.key_of_value(start),
                    grid.key_of_value(end),
                ),
                grid.key_of_value(start),
                grid.key_of_value(end),
            )
            + "A"
        )
        # process_paths = bfs(grid, grid.key_of_value(start), grid.key_of_value(end))

        if level == levels - 1:
            return len(process_path)

        output_len = 0
        for start, end in pairwise("A" + process_path):
            # print("-" * (level + 1), "From", start, "to", end)
            output_len += build_grid_path(start, end, level + 1)

        return output_len

    output_len = 0
    for start, end in pairwise("A" + input_path):
        # print("From", start, "to", end)
        output_len += build_grid_path(start, end, 0)
    return output_len


direct_grid = HashableDict(
    {
        (0, 0): "7",
        (1, 0): "8",
        (2, 0): "9",
        (0, 1): "4",
        (1, 1): "5",
        (2, 1): "6",
        (0, 2): "1",
        (1, 2): "2",
        (2, 2): "3",
        (1, 3): "0",
        (2, 3): "A",
    }
)
indirect_grid = HashableDict(
    {(1, 0): "^", (2, 0): "A", (0, 1): "<", (1, 1): "v", (2, 1): ">"}
)


test = """029A
980A
179A
456A
379A"""

test = """379A"""

# print(
#     dijkstra(direct_grid, direct_grid.key_of_value("A"), direct_grid.key_of_value("8"))
# )

lines = []

# with StringIO(test) as input_data:
with open("input21.txt") as input_data:
    for line in input_data:
        lines.append(line.strip())

values = [int(line[:-1]) for line in lines]
complexities = []

for ln, line in enumerate(lines):
    output_len = calculate_path_length(line, 26)
    # print(ln, len(line), "->", output_len)
    complexities.append(output_len)

    # print(get_neighbours.cache_info())
    # print(dijkstra.cache_info())
    # print(refine_path.cache_info())
    # print(build_grid_step.cache_info())

print(values, complexities)
print("Total complexity:", sum(v * c for v, c in zip(values, complexities)))

# 239800 too low
# 242484 ?!

# 252967662595732 too low (with 26)
# 298790926447004 wrong :'(
# 355915209781402 wrong
# 362142005052472 wrong
# 376188062904948 too high

# 624696148034632 too high (with 27)
