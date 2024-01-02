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

def generate_parts(counts):
    # return ["#" * c + ("." if i < len(counts)-1 else "") for i, c in enumerate(counts)]
    return ["#" * c for i, c in enumerate(counts)]

def match_possible(pattern, possible):
    for a, b, in zip(pattern, possible):
        if a != b and a != "?":
            return False
    return True

@cache
def decide_on_character(ch, hashes, part):
    to_return = []
    
    if ch == "?":
        if hashes > 0 and hashes == len(part):
            to_return.append((-1, 1, -hashes, "."))
        elif hashes == 0:
            to_return.append((-1, 0, 0, "."))

        if part and hashes+1 <= len(part):
            to_return.append((1, 0, 1, "#"))

    elif ch == ".":
        if hashes > 0 and hashes == len(part):
            to_return.append((-1, 1, -hashes, None))
        elif hashes == 0:
            to_return.append((-1, 0, 0, None))

    elif ch == "#":
        if part and hashes+1 <= len(part):
            to_return.append((1, 0, 1, None))

    return to_return

def check_patterns(patterns):
    totals = 0
    for pattern, parts in patterns:
        # print(pattern, parts)
        
        # pos = 0
        # group = 0
        # hashes = 0

        queue = [(0, 0, 0, pattern)]

        while len(queue) > 0:
            pos, group, hashes, working = queue.pop(0)
            # print(pos, len(pattern), working, len(queue))

            if pos < len(pattern):
                decisions = decide_on_character(working[pos], hashes, parts[group] if group < len(parts) else None)
                for pos_add, group_add, hash_add, replace in decisions:
                    if pos_add < 0:
                        skip_working = working.replace("?", replace, 1) if replace else working
                        skip_pos = pos + 1
                        while skip_pos < len(working) and working[skip_pos] == ".":
                            skip_pos += 1

                        queue.append((skip_pos, group + group_add, hashes + hash_add, skip_working))

                    else:
                        queue.append((pos + pos_add, group + group_add, hashes + hash_add, working.replace("?", replace, 1) if replace else working))

            else:
                if hashes > 0 and hashes == len(parts[group]):
                    group += 1
                
                if match_possible(pattern, working) and group == len(parts):
                    totals += 1
                    
        # print(pattern, "->", totals)
    
    return totals

readings = []
# with StringIO(test) as data:
with open("input12.txt") as data:
    for line in data:
        p, c = line.strip().split()
        readings.append((p,c))

start = time()
p1_patterns = []

for pattern, counts in readings:
    parts = generate_parts(list(map(int, counts.split(","))))
    p1_patterns.append((pattern, parts))

totals = check_patterns(p1_patterns)

print("Part 1:", totals)
print("Elapsed:", time() - start)

start = time()
p2_patterns = []

for pattern, counts in readings:
    p2_pattern = "?".join([pattern]*5)
    p2_counts = list(map(int, counts.split(",")))*5
    p2_parts = generate_parts(p2_counts)
    p2_patterns.append((p2_pattern, p2_parts))
    
totals = check_patterns(p2_patterns)

print("Part 2:", totals)
print("Elapsed:", time() - start)
