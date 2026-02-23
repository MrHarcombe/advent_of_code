from io import StringIO
from itertools import combinations
from math import prod
from structures import MatrixGraph
from time import time

test = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""

def distance_squared(a,b):
    return sum([(pa - pb) ** 2 for pa, pb in zip(a, b)])

boxes = MatrixGraph(True)
junctions = []

# with StringIO(test) as file:
with open("input8.txt") as file:
    for line in file:
        x,y,z = map(int, line.split(","))
        boxes.add_node((x,y,z))
        junctions.append((x,y,z))

checkpoint = time()
items = sorted([pair for pair in combinations(junctions, 2)], key=lambda item: distance_squared(*item))
# print(items)
print("Sorted distances:", time()- checkpoint)

checkpoint = time()
for n in range(1000):
    boxes.add_edge(*items[n])
print("Graph connected:", time() - checkpoint)

checkpoint = time()
visited = set()
circuit_sizes = []
for node in junctions:
    if node not in visited:
        connected = boxes.breadth_first(node)
        circuit_sizes.append(len(connected))
        visited |= set(connected)

print("Part 1:", prod(sorted(circuit_sizes)[-3:]))
print("Elapsed:", time() - checkpoint)

checkpoint = time()
n = 1000
while n < len(items) and len(connected) < len(boxes):
    boxes.add_edge(*items[n])
    connected = boxes.breadth_first(junctions[0])
    n += 1

print("Part 2:", items[n-1][0][0] * items[n-1][1][0])
print("Elapsed:", time() - checkpoint)

# 1434904142 too low (68306 * 71516)