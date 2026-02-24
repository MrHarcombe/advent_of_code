from io import StringIO
from structures import DiscreteIntervalEncodingTree
from time import time

test = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""

checkpoint = time()
diet = DiscreteIntervalEncodingTree()
ingredient_count = 0

# with StringIO(test) as file:
with open("input5.txt") as file:
    for line in file:
        if "-" not in line:
            break

        start, stop = map(int, line.strip().split("-"))
        diet.insert((start, stop))

    for line in file:
        ingredient = int(line)
        if ingredient in diet:
            ingredient_count += 1

print("Part 1:", ingredient_count)
print("Elapsed:", time() - checkpoint)
print("Part 2:", len(diet))
print("Final:", time() - checkpoint)
# print(diet)

# 355373167127369 too high
