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

    def key_of_value(self, v):
        return next(ik for ik, iv in self.items() if iv == v)


def get_neighbours(grid, point):
    x, y = point
    for dir, step in directions.items():
        dx, dy = step
        new_point = (x + dx, y + dy)
        if grid.get(new_point, None) is not None:
            yield new_point, dir


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

    return HashableDict(convert_dijkstra_data(data))


def convert_dijkstra_data(dijkstra_data):
    return {k: tuple(dijkstra_data[k]) for k in dijkstra_data}


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

    if grid == direct_grid and (
        ((start[1] == 0 and end[1] > 0) or (start[1] > 0 and end[1] == 0))
        and (start[0] == 0 or end[0] == 0)
    ):
        # do up then left
        # sort as ULDR
        path.sort(key=lambda item: (1, 0, 2, 3).index(item[1]))

    elif grid == indirect_grid and (
        ((start[1] == 0 and end[1] == 1) or (start[1] == 1 and end[1] == 0))
        and (start[0] == 0 or end[0] == 0)
    ):
        # do down then left
        # sort as DLUR
        path.sort(key=lambda item: (2, 0, 1, 3).index(item[1]))
    else:
        # sort as LUDR
        path.sort(key=lambda item: item[1])

    return tuple([direction_indicators[step[1]] for step in path])


@cache
def build_grid_path(input_path, grid):
    output_path = ""
    for start, end in pairwise("A" + input_path):
        # print("From", start, "to", end)
        step_path = refine_path(
            grid,
            dijkstra(
                grid,
                grid.key_of_value(start),
                grid.key_of_value(end),
            ),
            grid.key_of_value(start),
            grid.key_of_value(end),
        )
        # print(path)
        output_path += "".join(step_path) + "A"

    return output_path


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

# print(
#     dijkstra(direct_grid, direct_grid.key_of_value("A"), direct_grid.key_of_value("8"))
# )

complexities = 0
# with StringIO(test) as input_data:
with open("input21.txt") as input_data:
    for line in input_data:
        line_path = build_grid_path(line.strip(), direct_grid)

        # line_path = ""
        # for start, end in pairwise("A" + line.strip()):
        #     # print("From", start, "to", end)
        #     path = refine_path(
        #         direct_grid,
        #         dijkstra(
        #             direct_grid,
        #             direct_grid.key_of_value(start),
        #             direct_grid.key_of_value(end),
        #         ),
        #         direct_grid.key_of_value(start),
        #         direct_grid.key_of_value(end),
        #     )
        #     # print(path)
        #     line_path += "".join(path) + "A"
        # print(line_path)

        indirect_path = build_grid_path(line_path, indirect_grid)

        # indirect_path = ""
        # for start, end in pairwise("A" + line_path):
        #     # print("From", start, "to", end)
        #     path = refine_path(
        #         indirect_grid,
        #         dijkstra(
        #             indirect_grid,
        #             indirect_grid.key_of_value(start),
        #             indirect_grid.key_of_value(end),
        #         ),
        #         indirect_grid.key_of_value(start),
        #         indirect_grid.key_of_value(end),
        #     )
        #     # print(path)
        #     indirect_path += "".join(path) + "A"
        # # print(indirect_path)

        inindirect_path = build_grid_path(indirect_path, indirect_grid)

        # inindirect_path = ""
        # for start, end in pairwise("A" + indirect_path):
        #     # print("From", start, "to", end)
        #     path = refine_path(
        #         indirect_grid,
        #         dijkstra(
        #             indirect_grid,
        #             indirect_grid.key_of_value(start),
        #             indirect_grid.key_of_value(end),
        #         ),
        #         indirect_grid.key_of_value(start),
        #         indirect_grid.key_of_value(end),
        #     )
        #     # print(path)
        #     inindirect_path += "".join(path) + "A"
        # # print(inindirect_path)

        complexity = len(inindirect_path) * int(line.strip()[:-1])
        print(
            len(inindirect_path),
            int(line.strip()[:-1]),
            len(inindirect_path) * int(line.strip()[:-1]),
        )

        complexities += complexity

print("Part 1:", complexities)

# 239800 too low
# 242484 ??
