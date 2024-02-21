from collections import defaultdict
from heapq import heappush, heappop, heapify
from io import StringIO
from math import sin, cos, pi, floor, sqrt
from time import time

test = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""

def get_from_infinite(garden, point):
    row, col = point
    max_row, max_col = garden["max_row"], garden["max_col"]
    
    row %= max_row+1
    col %= max_col+1
    
    return garden.get((row, col), ".")

def get_neighbours(graph, point):
    if point not in cached:
        neighbours = []
        for dr, dc in ((-1,0), (0,1), (1,0), (0,-1)):
            # if get_from_infinite(graph, (point[0] + dr, point[1] + dc)) == ".":
            if 0 <= point[0] + dr <= graph["max_row"] and 0 <= point[1] + dc <= graph["max_col"] and graph.get((point[0] + dr, point[1] + dc), ".") == ".":
                neighbours.append((point[0] + dr, point[1] + dc))
        cached[point] = neighbours

    return cached[point]

def dijkstra(graph, max_cost, start, end=None):
    queue = []
    data = defaultdict(lambda: [float("inf"), None])

    data[start][0] = 0
    heappush(queue, (0, start))
    
    while len(queue) > 0:
        _, node = heappop(queue)

        for neighbour in get_neighbours(graph, node):
            cost = data[node][0] + 1
            if cost < max_cost+1:
                if cost < data[neighbour][0]:
                    data[neighbour][0] = cost
                    data[neighbour][1] = node
                    heappush(queue, (data[neighbour][0], neighbour))

    if end == None:
        return data

    path = []
    current = end
    while current != start:
        path.append(current)
        current = data[current][1]
    path.append(current)
    shortest = path[::-1]
    return shortest, data

def display_reachable(graph, reachable, start):
    for row in range(graph["max_row"]+1):
        line = ""
        for col in range(graph["max_col"]+1):
            if (row,col) == start:
                line += "S"
            elif (row,col) in reachable:
                line += "O"
            else:
                line += get_from_infinite(graph, (row,col))
        print(line)

cached = {}
garden = {}

# with StringIO(test) as data:
with open("input21.txt") as data:
    for row, line in enumerate(data):
        for col, ch in enumerate(line.strip()):
            if ch == "S":
                start = (row,col)
                # garden[(row,col)] = "#"
            elif ch == "#":
                garden[(row,col)] = ch
                
    garden["max_row"] = row
    garden["max_col"] = col

begin = time()
max_steps = 64

results = dijkstra(garden, max_steps, start)
print("Dijkstra elapsed:", time() - begin)

print("Part 1:", len([r for r in results if results[r][0] in range(max_steps,-1,-2)]))
# display_reachable(garden, reachable, start)
print("Finished:", time() - begin)

even_results = dijkstra(garden, garden["max_col"], start)
odd_results = dijkstra(garden, garden["max_col"]+1, start)
print("Part 2 Dijkstra elapsed:", time() - begin)

even_length = len([r for r in even_results if even_results[r][0] in range(garden["max_col"],-1,-2)])
odd_length = len([r for r in odd_results if odd_results[r][0] in range(garden["max_col"]+1,-1,-2)])

# print(even_length, odd_length)

even_corner = len([r for r in even_results if even_results[r][0] in range(66,garden["max_col"]+1,2)])
odd_corner = len([r for r in odd_results if odd_results[r][0] in range(67,garden["max_col"]+1,2)])

# print(even_corner, odd_corner)

n = ((26501365 - (garden["max_col"] // 2)) // (garden["max_col"] + 1))
# print(n)
assert(n == 202300)

print("Part 2:", (n+1)*(n+1) * odd_length + (n*n) * even_length - (n+1) * odd_corner + n * even_corner)
print("Finished:", time() - begin)

## Full (finite) square solutions 
# even steps - 7699
# odd steps - 7651