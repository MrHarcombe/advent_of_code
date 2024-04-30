from io import StringIO
from itertools import permutations

test = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""

preamble = 25

# with StringIO(test) as data:
with open("Input9.txt") as data:
    xmas_values = list(map(int, data.readlines()))

for consider in range(preamble, len(xmas_values)):
    invalid = xmas_values[consider]
    pool = xmas_values[consider-preamble:consider]
    # print(consider, pool)
    if not any((sum(p) == invalid for p in permutations(pool, 2))):
        print("Part 1:", invalid)
        break

start = 0
found_invalid_sum = False
while not found_invalid_sum:
    for finish in range(len(xmas_values)):
        invalid_sum = sum(xmas_values[start:finish])
        if invalid == invalid_sum:
            found_invalid_sum = True
            break
        elif invalid < invalid_sum:
            break
    if not found_invalid_sum:
        start += 1

print("Part 2:", min(xmas_values[start:finish]) + max(xmas_values[start:finish]))