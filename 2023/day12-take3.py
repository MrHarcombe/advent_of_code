from collections.abc import Iterable
from io import StringIO
from itertools import chain
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

def generate_parts(counts):
    return ["#" * c  + ("." if i < len(counts)-1 else "") for i, c in enumerate(counts)]

def match_possible(pattern, possible):
    for a, b, in zip(pattern, possible):
        if a == b or a == "?":
            continue
        return False
    return True

readings = []
# with StringIO(test) as data:
with open("input12.txt") as data:
    for line in data:
        p, c = line.strip().split()
        readings.append((p,c))

def fit_next_part(pattern, match, parts, spare_dots):
    if len(parts) == 0:
        return 1 if match_possible(pattern, match + ("." * spare_dots)) else 0

    possibles = []
    for dots in range(spare_dots+1):
        if match_possible(pattern, match + ("." * dots) + parts[0]):
            possibles.append((pattern, match + ("." * dots) + parts[0], parts[1:], spare_dots - dots))

    return sum(fit_next_part(*possible) for possible in possibles)

def flatten(l):
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el

start = time()
total = 0
for pattern, counts in readings:
    parts = generate_parts(list(map(int, counts.split(","))))
    spare_dots = len(pattern) - sum(len(p) for p in parts)
    # print(pattern, parts, spare_dots)
    
    # for hit in flatten(fit_next_part(pattern, "", parts, spare_dots)):
    #     print(pattern, "->", hit, file=trace)
    total += fit_next_part(pattern, "", parts, spare_dots)

print("Part 1:", total)
print("Elapsed:", time() - start)

start = time()
total = 0
for pattern, counts in readings:
    p2_pattern = "?".join([pattern]*5)
    p2_counts = list(map(int, counts.split(",")))*5
    
    p2_parts = generate_parts(p2_counts)
    spare_dots = len(p2_pattern) - sum(len(p) for p in p2_parts)
    total += fit_next_part(p2_pattern, "", p2_parts, spare_dots)

print("Part 2:", total)
print("Elapsed:", time() - start)

# trace.close()
