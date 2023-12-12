from io import StringIO
from itertools import product
from time import time
import re

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

def match_springs_to_counts(springs, counts):
    m = re.findall(r"([#]+)", springs)
    return len(m) == len(counts) and all([len(mhash) == count for mhash, count in zip(m, counts)])

def spring_alternatives(spring, num_hash):
    for p in product('#.', repeat=spring.count("?")):
        if p.count("#") != num_hash:
            continue
        p_count = 0
        spring_list = list(spring)
        for i in range(len(spring_list)):
            if spring_list[i] == "?":
                spring_list[i] = p[p_count]
                p_count += 1
        yield "".join(spring_list)

start = time()
total = 0
p2_total = 0
with StringIO(test) as data:
# with open("input12.txt") as data:
    for line in data:
        springs, tcounts = line.strip().split()
        counts = list(map(int, tcounts.split(",")))
        total += sum([1 for a in spring_alternatives(springs, sum(counts) - springs.count("#")) if match_springs_to_counts(a, counts)])
        
        p2_springs = "?".join([springs]*5)
        p2_counts = list(map(int, ",".join(tcounts.split(",")*5).split(",")))
        p2_total += sum([1 for a in spring_alternatives(p2_springs, sum(p2_counts) - p2_springs.count("#")) if match_springs_to_counts(a, p2_counts)])

print("Part 1:", total)
print("Part 2:", p2_total)
print("Elapsed:", time() - start)
