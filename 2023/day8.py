from io import StringIO
from math import lcm
import re

test = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

test = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

test = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

pattern = re.compile(r"(.+) = \((.+), (.+)\)")
ghost_map = {}

# with StringIO(test) as data:
with open("input8.txt") as data:
    path = data.readline().strip()
    data.readline()
    
    for line in data:
        node, left, right = pattern.findall(line)[0]
        ghost_map[node] = (left, right)

def part1(start="AAA", ends=["ZZZ"]):
    # start = "AAA"
    # end = "ZZZ"

    current = start
    steps = 0
    while current not in ends:
        for step in path:
            steps += 1
            if step == "L":
                current = ghost_map[current][0]
            else:
                current = ghost_map[current][1]

    return steps

# def part2():
#     start = [node for node in ghost_map if node.endswith("A")]
# 
#     current = start
#     steps = 0
#     while any([True for node in current if not node.endswith("Z")]):
#         for step in path:
#             steps += 1
#             for i, node in enumerate(current):
#                 if step == "L":
#                     current[i] = ghost_map[node][0]
#                 else:
#                     current[i] = ghost_map[node][1]
# 
#     print("Part 2:", steps)

def part2():
    starts = [node for node in ghost_map if node.endswith("A")]
    ends = [node for node in ghost_map if node.endswith("Z")]
    steps = [part1(start, ends) for start in starts]
    # print(steps, lcm(*steps))
    return lcm(*steps)
    

print("Part 1:", part1())
print("Part 2:", part2())