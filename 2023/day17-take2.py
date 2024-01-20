from collections import defaultdict
from structures import WeightedMatrixGraph
from heapq import heappop, heappush, heapify
from io import StringIO

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

# test = """
# 11599
# 99199
# 99199
# 99199
# 99111"""

def path_cost(graph, path):
    cost = 0
    for p in path[1:]:
        cost += graph[p]
    return cost

def get_neighbours(graph, point, previous):
    for d, (dr, dc) in enumerate(((-1,0), (0,1), (1,0), (0,-1))):
        new_point = (point[0] + dr, point[1] + dc)
        if 0 <= new_point[0] <= graph["max_row"] and 0 <= new_point[1] <= graph["max_col"]:
            if len(previous) > 0:
                if previous[-1] == (d + 2) % 4:
                    # print(point, new_point, "not doubling back:", previous[-1], d)
                    continue

                most_recent = previous[-3:]
                if len(most_recent) == 3 and all(d == p for p in most_recent):
                    # print(point, new_point, "turning:", most_recent, d)
                    continue

            yield new_point, d

def depth_first(graph, src, dst):
    best_path = float("inf")
    queue = [(src, [], [])]

    while len(queue) > 0:
        current, previous_path, previous_steps = queue.pop()

        if current == dst:
            full_path = previous_path + [current]
            return path_cost(graph, full_path)

        else:
            for neighbour, step in get_neighbours(graph, current, previous_steps):
                if neighbour not in previous_path:
                    queue.append((neighbour, list(previous_path) + [current], list(previous_steps) + [step]))


def breadth_first(graph, src, dst, target):
    best_path = target
    queue = [(src, [], [])]
    visited = set()

    while len(queue) > 0:
        current, previous_path, previous_steps = queue.pop(0)
        visited.add(current)

        if current == dst:
            full_path = previous_path + [current]
            full_path_cost = path_cost(graph, full_path)
            if full_path_cost < best_path:
                best_path = full_path_cost
            yield full_path

        else:
            for neighbour, step in get_neighbours(graph, current, previous_steps):
                if neighbour not in visited:
                    if path_cost(graph, previous_path + [current]) < best_path:
                        queue.append((neighbour, list(previous_path) + [current], list(previous_steps) + [step]))

city = {}
with StringIO(test) as data:
# with open("input17.txt") as data:
    for row, line in enumerate(data):
        for col, ch in enumerate(line.strip()):
            city[(row,col)] = int(ch)

city["max_row"] = row
city["max_col"] = col

start=(0,0)
end=(row,col)

initial_cost = depth_first(city, start, end)
print("Initial cost:", initial_cost)

paths = []
best_cost = initial_cost
for path in breadth_first(city, start, end, best_cost):
    this_cost = (path_cost(city, path))
    if this_cost < best_cost:
        best_cost = this_cost
        print("New best cost:", best_cost)
    paths.append((this_cost, path))

print(min(paths))
