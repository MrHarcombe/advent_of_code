from io import StringIO
from structures import WeightedMatrixGraph
from time import time

test = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""

# test = """#.#####################
# #.....................#
# #####################.#"""

slopes = {"^": (-1,0), ">": (0,1), "v": (1,0), "<": (0,1), "#": (0,0)}

def get_neighbours(graph, point):
    for dr, dc in ((-1,0), (0,1), (1,0), (0,-1)):
        pr, pc = point
        if 0 <= pr + dr <= graph["max_row"] and 0 <= pc + dc <= graph["max_col"]:
            new_point = (pr + dr, pc + dc)
            new_path = graph.get(new_point, ".")
            if new_path == "." or slopes[new_path] == (dr,dc):
                yield new_point

def get_neighbours2(graph, point):
    for dr, dc in ((-1,0), (0,1), (1,0), (0,-1)):
        pr, pc = point
        if 0 <= pr + dr <= graph["max_row"] and 0 <= pc + dc <= graph["max_col"]:
            new_point = (pr + dr, pc + dc)
            if graph.get(new_point, ".") != "#":
                yield new_point

class Day23WMG(WeightedMatrixGraph):
    def depth_first(self, start_node, end_node=None):
        if start_node in self.matrix[0]:
            queue = [(start_node, {start_node}, 0)]

            while len(queue) > 0:
                current, visited, distance = queue.pop()

                if current == end_node:
                    yield distance

                else:
                    for node, weight in self.get_connections(current):
                        if node not in visited:
                            queue.append((node, visited | {node}, distance + weight))

    def breadth_first(self, start_node, end_node=None):
        if start_node in self.matrix[0]:
            queue = [(start_node, {start_node}, 0)]

            while len(queue) > 0:
                current, visited, distance = queue.pop(0)

                if current == end_node:
                    yield distance

                else:
                    for node, weight in self.get_connections(current):
                        if node not in visited:
                            queue.append((node, visited | {node}, distance + weight))

paths = {}

# with StringIO(test) as data:
with open("input23.txt") as data:
    for row, line in enumerate(data):
        for col, ch in enumerate(line.strip()):
            if ch != ".":
                paths[(row,col)] = ch

paths["max_row"] = row
paths["max_col"] = col

start = next((0,col) for col in range(paths["max_col"]+1) if (0,col) not in paths)
goal = next((row,col) for col in range(paths["max_col"]+1) if (row,col) not in paths)

begin = time()
routes = []
queue = [(start, set())]
while len(queue) > 0:
    current, visited = queue.pop(0)
    if current == goal:
        routes.append(visited)
    else:
        for neighbour in get_neighbours(paths, current):
            if neighbour not in visited:
                queue.append((neighbour, visited | {neighbour}))

print("Part 1:", len(max(routes, key=lambda r: len(r))))
print("Elapsed:", time() - begin)

squashed = Day23WMG(True)
routes = []
visited = []
queue = [start]
squashed.add_node(start)

while len(queue) > 0:
    # assume this is a junction
    current = queue.pop(0)

    # for each of it's neighbours...
    neighbours = list(n for n in get_neighbours2(paths, current) if n not in visited)

    for neighbour in neighbours:
        # squash them down to this starting node, stopping just short of the junction
        cost = 0
        squash_neighbours = list(n for n in get_neighbours2(paths, neighbour) if n != current and n not in visited)
        squash_neighbour = neighbour
        while len(squash_neighbours) == 1:
            previous = squash_neighbour
            visited.append(previous)
            squash_neighbour = squash_neighbours[0]
            cost += 1
            squash_neighbours = list(n for n in get_neighbours2(paths, squash_neighbour) if n != previous)

        if squash_neighbour not in squashed:
            squashed.add_node(squash_neighbour)

        squashed.add_edge(current, squash_neighbour, cost+1)

        # append the end junction to the queue, to repeat the process
        if squash_neighbour not in queue and squash_neighbour not in visited:
            queue.append(squash_neighbour)

print("Squashed:", time() - begin)

# print("Part 2:", max([path for path in squashed.breadth_first(start, goal)]))
print("Part 2:", max([path for path in squashed.depth_first(start, goal)]))
print("Elapsed:", time() - begin)
