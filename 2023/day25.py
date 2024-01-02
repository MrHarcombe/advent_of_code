from io import StringIO
from itertools import combinations, permutations
from structures import MatrixGraph
from time import time

test = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""

connections = MatrixGraph(True)
headers = []

start = time()
# with StringIO(test) as data:
with open("input25.txt") as data:
    for line in data:
        from_, to_ = line.strip().split(":")
        to_ = to_.split()

        headers.append(from_)
        
        if from_ not in connections:
            connections.add_node(from_)
        for t in to_:
            if t not in connections:
                connections.add_node(t)
            connections.add_edge(from_, t)

full_size = len(connections)
print("Parsed:", time() - start)

###
# brute force works for the test, but is simply unwieldy for the input
# so instead, I'm going to generate the dot input to use on the web
# version of GraphViz available at dreampuf.github.io/GraphvizOnline

# for group in combinations(connections.matrix[0], 6):
#     n1, n2, n3, n4, n5, n6 = group
# 
#     c1 = connections.is_connected(n1, n2)
#     c2 = connections.is_connected(n3, n4)
#     c3 = connections.is_connected(n5, n6)
# 
#     if all((c1, c2, c3)):
#         connections.delete_edge(n1, n2)
#         connections.delete_edge(n3, n4)
#         connections.delete_edge(n5, n6)
#         
#         bfs1 = connections.breadth_first(n5)
#         bfs2 = connections.breadth_first(n6)
# 
#         if len(bfs1) + len(bfs2) == full_size:
#             print(bfs1)
#             print(bfs2)
#             print("Part 1:", len(bfs1) * len(bfs2))
#             break
# 
#         connections.add_edge(n1, n2)
#         connections.add_edge(n3, n4)
#         connections.add_edge(n5, n6)

with open("day25-input.dot", "w") as dot:
    print("graph {", file=dot)
    print("edge [colorscheme=spectral10];", file=dot)
    print("layout=neato;", file=dot)
    edge = 0
    for n in connections.matrix[0]:
        # print(n, "--", "{", " ".join(nc for (nc, _) in connections.get_connections(n)), "}", file=dot)
        for nc, _ in connections.get_connections(n):
            edge += 1
            print(n, "--", nc, f'[color={edge%10}, tooltip="{n} to {nc}"]', file=dot)
    print("}", file=dot)
print("Elapsed:", time() - start)

for i in range(3):
    n1 = input("Node 1: ")
    n2 = input("Node 2: ")
    connections.delete_edge(n1, n2)
    
bfs1 = connections.breadth_first(n1)
bfs2 = connections.breadth_first(n2)
print("Part 1: ", len(bfs1), "*", len(bfs2), "=", len(bfs1) * len(bfs2))
