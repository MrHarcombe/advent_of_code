from io import StringIO

test = """0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10"""

def bridge_length(bridge):
    return len(bridge)

def bridge_strength(bridge):
    return sum([sum(port) for port in bridge])

ports = []
# with StringIO(test) as data:
with open("input24.txt") as data:
    for line in data:
        ports.append([int(n) for n in line.split("/")])

starts = [p for p in ports if p[0] == 0]
bridges = []

for sp in starts:
    # treat like a DFS...
    open_port = sp[1] # first port must be 0, will be in sp[0]
    queue = [[open_port, [sp], [p for p in ports if p != sp]]]

    for next_ in queue:
        port, chain, remaining = next_
        possibles = [p for p in remaining if port in p]
        if len(possibles) == 0:
            bridges.append(chain)
        else:
             for link in possibles:
                 new_port = link[1] if link[0] == port else link[0]
                 queue.append([new_port, chain + [link], [p for p in remaining if p != link]])

# print("Bridges:", bridges)
# for bridge in bridges:
#     print(sum([sum(n) for n in bridge]), "->", bridge)
    
print("Part 1:", bridge_strength(max(bridges, key=bridge_strength)))
print("Part 2:", bridge_strength(sorted(bridges, key=lambda l: (bridge_length(l), bridge_strength(l)), reverse=True)[0]))