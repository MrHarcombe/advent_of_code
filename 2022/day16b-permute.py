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
    return total_release

def permute_all_but_one(starting_list, list_length):
    for first in starting_list:
        for possible in permutations([cave for cave in starting_list if cave != first], list_length - 1):
            possible = [first] + list(possible)

            journey = []
            current = "AA"
            turns = 30

            for cave in possible:
                if current not in dijkstra_cache:
                    costs = dijkstra(current)
                    dijkstra_cache[current] = costs
                else:
                    costs = dijkstra_cache[current]

                if (turns - (costs[cave][1] + 1)) < 0:
                    yield journey
                    break

                cave_release = (turns - (costs[cave][1] + 1)) * pressures[cave]
                turns -= costs[cave][1] + 1
                journey.append((cave, turns))
                current = cave
                
            yield journey

def run_through_sublists(cave_list, journey_length):
    for sublist in combinations(cave_list, journey_length):
        for journey in permute_list(sublist):
            yield journey

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

            if (turns - (costs[cave][1] + 1)) < 0:
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

length = 1
previous_best = -1
best_score = 0
best_journey = None
while best_score > previous_best:
    previous_best = best_score
    for journey in run_through_sublists(non_zero_caves, length):
        journey_score = score_journey(journey)
    
        for journey2 in run_through_sublists([cave for cave in non_zero_caves if cave not in (cave for cave, turns in journey)], length):
            journey2_score = score_journey(journey2)
            
            if journey_score + journey2_score > best_score:
                best_score = journey_score + journey2_score
                best_journey = (journey,journey2)

    print("length:", length, "best_score:", best_score, best_journey)
    length += 1

print(best_score, best_journey)
