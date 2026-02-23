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

        for possible in get_binary_possibles(node, possibles):
            if tuple(possible) not in considered:
                considered.add(possible)
                queue.append((presses+1, possible))

def astar_guess(node, target):
    # return the sum of the differences from each
    return sum(abs(p1-p2) for p1, p2 in zip(target, node))

def get_astar_possibles(node, button_wirings):
    possible_wirings = []
    for wiring in button_wirings:
        new_node = list(node)
        for index in wiring:
            new_node[index] += 1
        possible_wirings.append(tuple(new_node))

    return possible_wirings
        
def astar(machine):
    target = tuple(machine[2])
    start = tuple([0] * len(target))
    possibles = machine[1]
    
    # The set of discovered nodes that may need to be (re-)expanded.
    # Initially, only the start node is known.
    # This is usually implemented as a min-heap or priority queue rather than a hash-set.
    # openSet = {start}
    open_set = []
    considered = set()

    # For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from start
    # to n currently known.
    came_from = {}

    # For node n, gScore[n] is the cost of the cheapest path from start to n currently known.
    g_score = defaultdict(lambda: float('inf'))
    g_score[start] = 0

    # For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to
    # how short a path from start to finish can be if it goes through n.
    f_score = defaultdict(lambda: float('inf'))
    f_score[start] = astar_guess(start, target)

    heappush(open_set, (f_score[start], start))
    considered.add(start)

    while len(open_set) > 0:
        # This operation can occur in O(1) time if openSet is a min-heap or a priority queue
        # current := the node in openSet having the lowest fScore[] value
        current = heappop(open_set)[1]

        if current == target:
            # print("Made it!")
            # print(g_score[target], f_score[target], came_from)
            return g_score[target]

        for friend in get_astar_possibles(current, possibles):
            # d(current,neighbor) is the weight of the edge from current to neighbor
            # tentative_gScore is the distance from start to the neighbor through current
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score[friend]:
                # This path to neighbor is better than any previous one. Record it!
                came_from[friend] = current
                g_score[friend] = tentative_g_score
                friend_f_score = tentative_g_score + astar_guess(friend, target)
                f_score[friend] = friend_f_score
                if friend not in considered:
                    considered.add(friend)
                    heappush(open_set, (friend_f_score, friend))

    # Open set is empty but goal was never reached
    return

total_presses = 0
for m in machines:
    total_presses += bfs_p1(tuple(m[0]), m[1])

print("Part 1:", total_presses)

# total_presses = 0
# for index, m in enumerate(machines):
#     total_presses += astar(m)
#     print(f"After machine {index+1}: {total_presses}")
# 
# print("Part 2:", total_presses)
# 