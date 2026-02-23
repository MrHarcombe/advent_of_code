from collections import defaultdict
from heapq import heappush, heappop
from io import StringIO

test = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""

machines = []

with StringIO(test) as file:
# with open("input10.txt") as file:
    for line in file:
        machine = line.strip().split()
        target = [True if ch == "#" else False for ch in machine.pop(0)[1:-1]]
        joltage = list(map(int, machine.pop()[1:-1].split(",")))
        button_wirings = [list(map(int, m[1:-1].split(","))) for m in machine]
        machines.append((target, button_wirings, joltage))


def get_binary_possibles(node, button_wirings):
    possible_wirings = []
    for wiring in button_wirings:
        new_node = list(node)
        for index in wiring:
            new_node[index] = not new_node[index]
        possible_wirings.append(tuple(new_node))

    return possible_wirings
        
def get_integer_possibles(node, button_wirings):
    possible_wirings = []
    for wiring in button_wirings:
        new_node = list(node)
        for index in wiring:
            new_node[index] = new_node[index] + 1
        possible_wirings.append(tuple(new_node))

    return possible_wirings

def bfs_p1(target, possibles):
    queue = [(0, [False] * len(target))]
    considered = set(tuple([False] * len(target)))
    while len(queue):
        presses, node = queue.pop(0)

        if node == target:
            return presses

        for possible in get_binary_possibles(node, possibles):
            if tuple(possible) not in considered:
                considered.add(possible)
                queue.append((presses+1, possible))

def bfs_p2(target, possibles):
    queue = [(0, [0] * len(target))]
    considered = set(tuple([0] * len(target)))
    while len(queue):
        presses, node = queue.pop(0)

        if node == target:
            return presses

        for possible in get_integer_possibles(node, possibles):
            if tuple(possible) not in considered:
                considered.add(possible)
                queue.append((presses+1, possible))

# total_presses = 0
# for m in machines:
#     total_presses += bfs_p1(tuple(m[0]), m[1])
# 
# print("Part 1:", total_presses)

total_presses = 0
for m in machines:
    presses = 0
    target = tuple(m[2])
    possibles = m[1]
    finished = False
    multiplier = 1

    while not finished:
        odd_parts = [part % 2 for part in target]
        if any(part == 1 for part in odd_parts):
            target = [target[n] - odd_parts[n] for n in range(len(target))]
            presses += multiplier * bfs_p2(tuple(odd_parts), possibles)
            
        target = [part // 2 for part in target]
        multiplier *= 2
        
        finished = all(part == 0 for part in target)

    total_presses += presses
    # print(f"Finished machine: {total_presses}")

print("Part 2:", total_presses)
