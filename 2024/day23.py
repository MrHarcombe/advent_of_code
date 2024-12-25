from collections import defaultdict
from heapq import heappop, heappush
from io import StringIO

import networkx as nx

test = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""

lan = defaultdict(set)
lan_party = []

# with StringIO(test) as input_data:
with open("input23.txt") as input_data:
    for line in input_data:
        f, t = line.strip().split("-")

        if f in lan and t in lan:
            group_play = lan[f] & lan[t]
            for play in group_play:
                lan_party.append((f, t, play))

        lan[f].add(t)
        lan[t].add(f)

print(len([p for p in lan_party if any(pc for pc in p if pc.startswith("t"))]))


def find_cycle(start, graph, cycle_size):
    """Find a cycle of exactly cycle_size, if one exists. Note that this is not what was required for the problem...

    Args:
        start (_type_): Node to start from in the graph
        graph (_type_): Graph to search
        cycle_size (_type_): Size of the cycle to find

    Returns:
        _type_: *A* cycle, starting from the given node, of the given length
    """
    queue = []
    heappush(queue, (1, ([start], start)))

    while len(queue) > 0:
        _, (current_path, previous) = heappop(queue)

        if len(current_path) == cycle_size + 1 and current_path[-1] == current_path[0]:
            return current_path

        elif len(current_path) > 1 and current_path[-1] == current_path[0]:
            pass

        elif len(current_path) < cycle_size + 1:
            for connected in graph[current_path[-1]]:
                if connected != previous and connected not in current_path[1:-1]:
                    new_path = list(current_path) + [connected]
                    heappush(queue, (-len(new_path), (new_path, current_path[-1])))

    return None


# party_size = 4
# still_looking = True
# largest_party = None
# while still_looking:
#     for node in set(lan.keys()):
#         last_party = find_cycle(node, lan, party_size)
#         if last_party is not None:
#             largest_party = last_party
#             break
#     else:
#         still_looking = False

#     if still_looking:
#         party_size += 1

g = nx.Graph(lan)
largest_party = max(nx.find_cliques(g), key=len)
print("Part 2:", ",".join(sorted(largest_party)))
