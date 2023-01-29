from io import StringIO
from itertools import combinations
from math import prod

test="""1
2
3
4
5
7
8
9
10
11"""

# with StringIO(test) as f:
with open("input24.txt") as f:
    weights = [int(line.strip()) for line in f.readlines()]

print("Total bags:", sum(weights))
average_bag = sum(weights) // 4
print("Average bag:", average_bag)

candidates = []
for i in range(len(weights)):
    for n in combinations(weights, i):
        if sum(n) == average_bag:
            for j in range(len(weights) - len(n) + 1):
                for o in combinations([w for w in weights if w not in n], j):
                    if sum(o) == average_bag:
                        for k in range(len(weights) - len(n) - len(o) + 1):
                            for p in combinations([w for w in weights if w not in n], k):
                                if sum(o) == average_bag:
                                    candidates.append((n, o, sum([w for w in weights if w not in n and w not in o and w not in p])))
                        if len(candidates) > 0:
                            break
                        else:
                            print(i, j, k, len(candidates))
            if len(candidates) > 0:
                break
            else:
                print(i, j, len(candidates))
    if len(candidates) > 0:
        break
    else:
        print(i, len(candidates))
        
print(min([prod(b[0]) for b in candidates]))
        
# 29728298883 - too high
# 10439961859 part 1
# 72050269 part 2