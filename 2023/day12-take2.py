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
    return ["#" * c  + ("." if i < len(counts)-1 else "") for i, c in enumerate(counts)]

def match_possible(pattern, possible):
    for a, b, in zip(pattern, possible):
        if a == b or a == "?":
            continue
        return False
    return True

def get_neighbours(dot_splits):
    for i in range(len(dot_splits)):
        if dot_splits[i] > 0:
            for j in range(len(dot_splits)):
                if i != j:
                    yield tuple(dot_splits[n] - 1 if n == i else dot_splits[n] + 1 if n == j else dot_splits[n] for n in range(len(dot_splits)))

def resolve_pattern(dot_parts, parts):
    return "".join([d+p for d,p in zip(["." * n for n in dot_parts], parts + [""])])

def generate_possibles(pattern, parts):
    len_parts = sum(len(p) for p in parts)
    dot_parts = tuple(len(pattern) - len_parts if n == len(parts) else 0 for n in range(len(parts)+1))

    queue = [dot_parts]
    visited = set()
    impossible_prefix = {n for n in range(max(len(p) for p in parts)) if pattern[:n].count('#') > 0}
    impossible_suffix = {n for n in range(1, max(len(p) for p in parts)) if pattern[-n:].count('#') > 0}
    
    while len(queue) > 0:
        possible_dots = queue.pop(0)
        if possible_dots not in visited:
            visited.add(possible_dots)
            if not (possible_dots[0] in impossible_prefix or possible_dots[-1] in impossible_suffix):
                possible = resolve_pattern(possible_dots, parts)
                # print(".", end="")
                if match_possible(pattern, possible):
                    # print()
                    yield possible
            for next_possible in get_neighbours(possible_dots):
                queue.append(next_possible)

readings = []
with StringIO(test) as data:
# with open("input12.txt") as data:
    for line in data:
        p, c = line.strip().split()
        readings.append((p,c))

start = time()
total = 0
for pattern, counts in readings:
    parts = generate_parts(list(map(int, counts.split(","))))
    total += sum(1 for possible in generate_possibles(pattern, parts) if match_possible(pattern, possible))
 
print("Part 1:", total)
print("Elapsed:", time() - start)

start = time()
total = 0
for pattern, counts in readings:
    p2_pattern = "?".join([pattern]*5)
    p2_counts = list(map(int, counts.split(",")))*5
    
    p2_parts = generate_parts(p2_counts)
    total += sum(1 for possible in generate_possibles(p2_pattern, p2_parts) if match_possible(p2_pattern, possible))

##    print(p2_counts, "->", p2_parts)
##    count = 0
##    for possible in generate_possibles(p2_pattern, p2_parts):
##        print(possible)
##        count += 1
##    print(p2_pattern, count)
##    total += count

print("Part 2:", total)
print("Elapsed:", time() - start)
