from functools import cache
from io import StringIO
from time import time

test = """#.#.### 1,1,3
.#...#....###. 1,1,3
.#.###.#.###### 1,3,1,6
####.#...#... 4,1,1
#....######..#####. 1,6,5
.###.##....# 3,2,1"""

test = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

# test = """.# 1"""

@cache
def dot(pattern, groups):
    # nothing to do other than see if the rest of the pattern matches, skipping consecutive dots
    skip = 1
    while skip < len(pattern) and pattern[skip] == ".":
        skip += 1
    return solve(pattern[skip:], groups)

@cache
def hash(pattern, group, groups):
    # consider the next "group" characters, and if they can't all be springs
    # then its not a valid possibility
    if pattern[:group].replace("?", "#") != group * "#":
        return 0

    # check whether the remaining pattern is the same length as the last group...
    if len(pattern) == group:
        if len(groups) == 1:
            return 1
        return 0

    # ...othewise check that the next character is a separator, and if it is then
    # continue solving from the character after that
    if pattern[group] in "?.":
        return solve(pattern[group+1:], groups[1:])
    
    return 0

@cache
def solve(pattern, groups):
    # base case, to avoid recursing...
    
    # no more groups?
    if len(groups) == 0:
        # ... but springs left in pattern, means a failure
        if "#" in pattern:
            return 0
        
        # ...whereas no groups and no springs means a success
        return 1

    # more groups but no pattern left means a failure
    if len(pattern) == 0:
        return 0

    # more groups and more pattern, means more recursion to do...
    ch = pattern[0]
    group = groups[0]

    if ch == "?":
        out = hash(pattern, group, groups) + dot(pattern, groups)
        
    elif ch == "#":
        out = hash(pattern, group, groups)
    
    else: # ch == ".":
        out = dot(pattern, groups)

    # print(pattern, groups, "->", out)
    return out

readings = []
# with StringIO(test) as data:
with open("input12.txt") as data:
    for line in data:
        p, g = line.strip().split()
        readings.append((p,tuple(map(int, g.split(",")))))

start = time()
totals = 0
for pattern, groups in readings:
    totals += solve(pattern, groups)

print("Part 1:", totals)
print("Elapsed:", time() - start)

start = time()
totals = 0
for pattern, groups in readings:
    totals += solve("?".join([pattern]*5), groups*5)

print("Part 2:", totals)
print("Elapsed:", time() - start)
