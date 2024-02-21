from io import StringIO
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

def display_reachable(graph, reachable, start):
    for row in range(graph["max_row"]+1):
        line = ""
        for col in range(graph["max_col"]+1):
            if (row,col) == start:
                line += "S"
            elif (row,col) in reachable:
                line += "O"
            else:
                line += graph.get((row,col), ".")
        print(line)

cached = {}
garden = {}
reachable = set()
previous_reachable = 0
max_steps = 64
            
def get_neighbours(graph, point):
    if point not in cached:
        cached[point] = [(point[0] + dr, point[1] + dc) for dr, dc in ((-1,0), (0,1), (1,0), (0,-1)) if 0 <= point[0] + dr <= graph["max_row"] and 0 <= point[1] + dc <= graph["max_col"] and graph.get((point[0] + dr, point[1] + dc), ".") == "."]

    return cached[point]

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

queue = [(start, 0)]
while len(queue) > 0:
    current, steps = queue.pop()
    if steps < max_steps:
        for neighbour in get_neighbours(garden, current):
            if steps+1 == max_steps:
                reachable.add(neighbour)
                if len(reachable) > previous_reachable:
                    print(len(reachable), len(queue))
                    previous_reachable = len(reachable)
            else:
                queue.append((neighbour, steps+1))

# display_reachable(garden, reachable, start)
start = time()
print("Part 1:", len(reachable))
print("Elapsed:", time() - start)

## 211,225 too low
