from io import StringIO
from itertools import combinations
from math import prod

def build_combinations(k, n):
    assert n > k > 1
    to_process = [[i] for i in range(1, n+1)]
    while to_process:
        l = to_process.pop()
        s = sum(l)
        le = len(l)
        # If you do not distiguish permutations put range(l[-1],n-s+1) 
        # instead, to avoid generating repeated cases.
        # And if you do not want number repetitions, putting
        # range(l[-1] + 1, n-s+1) will do the trick.
        for i in range(l[-1], n-s+1):
        #for i in range(1, n-s+1): 
            news = s + i
            if news <= n:
                newl = list(l)
                newl.append(i)
                if le == k-1 and news == n:
                    yield tuple(newl)
                elif le < k-1 and news < n:
                    to_process.append(newl)

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
average_bag = sum(weights) // 3
print("Average bag:", average_bag)

candidates = []
# print(f"Weights: {weights}")
built = sorted(build_combinations(3, len(weights)), key=lambda i: (i[0]+i[1],i[0]))
# print(combinations)
for c in built:
    print(f"Checking composition: {c}")
    for first in combinations(weights, c[0]):
        if sum(first) != average_bag: continue
        for second in combinations([w for w in weights if w not in first], c[1]):
            if sum(second) != average_bag: continue
            third = [w for w in weights if w not in set(first) | set(second)]
            if sum(third) == average_bag:
                bags = sorted((first, second, third), key=lambda i: len(i))
                # print(bags, "QE=", prod(bags[0]))
                candidates.append(bags)
                
    if len(candidates) > 0:
        break

print("Best QE=", prod(sorted(candidates, key=lambda i:len(i[0]))[0][0]))
