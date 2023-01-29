from io import StringIO
from itertools import permutations

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

caves = {}
pressures = {}

with StringIO(test) as f:
    for line in f:
        flow, tunnels = line.strip().split(";")
        here, flow = flow.split("has")
        here = here.split()[1].strip()
        flow = int(flow.split("=")[1])
        tunnels = [tunnel.strip().replace("s ", "") for tunnel in tunnels.split("valve")[1].split(",")]
        
        # print(here, flow, tunnels)
        caves[here] = tunnels
        pressures[here] = flow

journey_length = len([i for i in pressures.items() if i[1] > 0])

journey = []
current = "AA"
turns = 30

while len(journey) < journey_length:
    costs = dijkstra(current)
    best_release = 0
    best_cave = None
    best_cave_cost = 0

    for cave in costs:
        if cave == current or cave in [cave for cave, cost in journey]:
            continue
        cave_release = (turns - (costs[cave][1] + 1)) * pressures[cave]
        # print(cave, cave_release)
        if cave_release > best_release:
            best_release = cave_release
            best_cave = cave

    print("best_cave:", best_cave, best_release)

    turns -= costs[best_cave][1] + 1
    print("turns:", turns)

    journey.append((best_cave, turns))
    current = best_cave

total_release = 0
for cave, turns in journey:
    total_release += pressures[cave] * turns
    
print(total_release)