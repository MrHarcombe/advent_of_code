from io import StringIO
from itertools import combinations, permutations

test = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""

def dijkstra(start_node, end_node=None):
    queued = {n: [False, 0 if n == start_node else float("inf"), None] for n in caves}
    
    current_node = start_node
    while current_node != None:
        _, current_cost, _ = queued[current_node]
        for neighbour in caves[current_node]:
            visited, total_cost, _ = queued[neighbour]
            if not visited:
                if total_cost > current_cost + 1:
                    queued[neighbour][1] = current_cost + 1
                    queued[neighbour][2] = current_node

        queued[current_node][0] = True
        if end_node != None and current_node == end_node:
            current_node = None
        else:
            current_node, details = sorted(queued.items(), key=lambda n: (n[1][0], n[1][1]))[0]
            if queued[current_node][0]:
                current_node = None

    # print(queued)
    if end_node == None:
        return queued

    path = []
    current = end_node
    while current != start_node:
        path.append(current)
        current = queued[current][2]
    path.append(current)
    shortest = path[::-1]
    return shortest

def score_journey(journey):
    total_release = 0
    for cave, turns in journey:
        total_release += pressures[cave] * turns
    return total_release, journey

def run_through_sublists(cave_list, journey_length, you=[], elephant=[]):
    if journey_length == 0: return
    # if len(cave_list) == 1: cave_list.append("##")

    if len(cave_list) > 1:
        cave_iter = iter(combinations(cave_list, 2))
    else:
        cave_iter = iter(combinations(cave_list, 1))

    next_caves = next(cave_iter, None)
    while next_caves != None:
        if len(next_caves) == 2:
            cave1, cave2 = next_caves
        else:
            cave1, cave2 = next_caves[0], None

        if cave2 == None:
            yield you + [cave1], elephant
            yield you, elephant + [cave1]

        elif len(you) + 1 == journey_length:
            yield you + [cave1], elephant + [cave2]
            yield you + [cave2], elephant + [cave1]

        else:
            yield from run_through_sublists([cave for cave in cave_list if cave not in you + elephant + [cave1, cave2]], journey_length, you + [cave1], elephant + [cave2])
            yield from run_through_sublists([cave for cave in cave_list if cave not in you + elephant + [cave1, cave2]], journey_length, you + [cave2], elephant + [cave1])

            # if len(you) == journey_length:
            #     yield you, elephant
            #     you, elephant = [], []
            #     cave_iter = top_list
            # 
            # else:
            #     remaining = [cave for cave in cave_list if cave not in you + elephant]
            #     if len(remaining) == 1: remaining.append("##")
            #     cave_iter = iter(permutations(remaining, 2))

        next_caves = next(cave_iter, None)

def permute_list(cave_list):
    start = "AA"

    for possible in permutations(cave_list, len(cave_list)):
        journey = []
        current = start
        # turns = 30
        turns = 26

        for cave in possible:
            if current not in dijkstra_cache:
                costs = dijkstra(current)
                dijkstra_cache[current] = costs
            else:
                costs = dijkstra_cache[current]

            if (turns - (costs[cave][1] + 1)) <= 0:
                yield journey
                break

            cave_release = (turns - (costs[cave][1] + 1)) * pressures[cave]
            turns -= costs[cave][1] + 1
            journey.append((cave, turns))
            current = cave

        yield journey

caves = {}
pressures = {}
dijkstra_cache = {}

# with StringIO(test) as f:
with open("input16.txt") as f:
    for line in f:
        flow, tunnels = line.strip().split(";")
        here, flow = flow.split("has")
        here = here.split()[1].strip()
        flow = int(flow.split("=")[1])
        tunnels = [tunnel.strip().replace("s ", "") for tunnel in tunnels.split("valve")[1].split(",")]
        
        # print(here, flow, tunnels)
        caves[here] = tunnels
        pressures[here] = flow

non_zero_caves = [cave for cave, pressure in sorted(pressures.items(), key=lambda item : item[1], reverse=True) if pressure > 0]

# for length in range(1,4):
#     lists = []
#     for you, elephant in run_through_sublists(non_zero_caves, length):
#         lists.append((you, elephant))
#     for row in sorted(lists, key=lambda i: (i[0][0], i[1][0])):
#         print(row)
# 
#     print("\n---\n")

length = 8
best_score = 0
best_journey = []

for you, elephant in run_through_sublists(non_zero_caves, length):
    your_best, your_journey = max([score_journey(journey) for journey in permute_list(you)], key=lambda i: i[0])
    their_best, their_journey = max([score_journey(journey) for journey in permute_list(elephant)], key=lambda i: i[0])

    if your_best + their_best > best_score:
        best_score = your_best + their_best
        best_journey = (your_journey, their_journey)
        print("new best", best_score, *best_journey)

print("***", best_score, best_journey)
