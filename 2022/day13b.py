from io import StringIO
import json
from functools import cmp_to_key
import time

test = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""

def compare_part(left, right):
    if isinstance(left, int) and isinstance(right, int):
        # print("Comparing ints", left, right)
        if left < right:
            return True
        elif left > right:
            return False

    elif isinstance(left, list) and isinstance(right, list):
        # print("Comparing lists", left, right)
        pos = 0
        while pos < len(left) and pos < len(right):
            result = compare_part(left[pos], right[pos])
            if result != None:
                return result
            pos += 1
        
        if pos == len(left) and pos < len(right):
            return True
        elif pos < len(left):
            return False

    elif isinstance(left, int):
        # print("Comparing int with list", left, right)
        return compare_part([left], right)
        
    elif isinstance(right, int):
        # print("Comparing list with int", left, right)
        return compare_part(left, [right])

def cmp_part(left, right):
    if isinstance(left, int) and isinstance(right, int):
        # print("Comparing ints", left, right)
        if left < right:
            return -1
        elif left > right:
            return 1

    elif isinstance(left, list) and isinstance(right, list):
        # print("Comparing lists", left, right)
        pos = 0
        while pos < len(left) and pos < len(right):
            result = cmp_part(left[pos], right[pos])
            if result != None:
                return result
            pos += 1
        
        if pos == len(left) and pos < len(right):
            return -1
        elif pos < len(left):
            return 1

    elif isinstance(left, int):
        # print("Comparing int with list", left, right)
        return cmp_part([left], right)
        
    elif isinstance(right, int):
        # print("Comparing list with int", left, right)
        return cmp_part(left, [right])

lines = []

# with StringIO(test) as f:
with open("input13.txt") as f:
    for line in f:
        if len(line.strip()) > 0:
            lines.append(json.loads(line))

# now append the "divider" packets
lines.append([[2]])
lines.append([[6]])

bubble_lines = list(lines)

# first use Python's built-in
compare_func = cmp_to_key(cmp_part)
now = time.time()
sorted_lines = sorted(lines, key=compare_func)
print("sorted:", time.time() - now)

# now compare with bubble sort :)
now = time.time()
sorted = False
while not sorted:
    sorted = True
    for i in range(len(bubble_lines)-1):
        if not compare_part(bubble_lines[i], bubble_lines[i+1]):
            bubble_lines[i], bubble_lines[i+1] = bubble_lines[i+1], bubble_lines[i]
            sorted = False
print("bubble:", time.time() - now)

for i, line in enumerate(sorted_lines):
    if line == [[2]] or line == [[6]]:
        print(i+1)
