from io import StringIO

test = """pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)"""

weights = {}
discs = {}

# with StringIO(test) as f:
with open("input7.txt") as f:
    for line in f:
        disc = line.strip().split()
        if len(disc) == 2:
            weights[disc[0]] = int(disc[1][1:-1])
            
        else:
            weights[disc[0]] = int(disc[1][1:-1])
            discs[disc[0]] = [d.strip(",") for d in disc[3:]]

# print(weights)
# print(discs)

def calculate_subtree(disc, show=False, depth=1):
    weight = weights[disc]
    if show: print("  " * depth, disc, weight)
    if disc in discs:
        for sub in discs[disc]:
            weight += calculate_subtree(sub, show, depth+1)
    return weight

all_values = sum(discs.values(), [])
for disc in discs:
    if disc not in all_values:
        print("Part 1:", disc)
        root = disc

root_level = True
target = root
problem = -1
while problem != 0:
    disc_tree_weights = [(disc, calculate_subtree(disc)) for disc in discs[target]]
    disc_weights = [weight for disc, weight in disc_tree_weights]
    if len(set(disc_weights)) > 1:
        problem = next((weight for weight in disc_weights if disc_weights.count(weight) == 1))
        target = next((disc for disc, weight in disc_tree_weights if weight == problem))
    
        if root_level:
            difference = (disc_weights[0] if disc_weights[0] != problem else disc_weights[1]) - problem
    else:
        problem = 0

print("Part 2:", target, weights[target] + difference)
