from collections import defaultdict
from time import time

# from io import StringIO
# from math import log10, ceil

test = """0 1 10 99 999"""
test = "125 17"


# with StringIO(test) as input_data:
with open("input11.txt") as input_data:
    for line in input_data:
        original = map(int, line.strip().split())

stones = defaultdict(int)
for stone in original:
    stones[stone] += 1

# input(f"Stones: {stones}")

begin = time()
for step in range(75):
    # print(f"Step {step+1}")
    new_stones = defaultdict(int)
    for stone in stones:
        if stone == 0:
            new_stones[1] += stones[stone]
        elif len(str(stone)) % 2 == 0:
            stone_str = str(stone)
            mid = len(stone_str) // 2
            new_stones[int(stone_str[:mid])] += stones[stone]
            new_stones[int(stone_str[mid:])] += stones[stone]
        # elif log10(stone + 0.1) > 0 and ceil(log10(stone + 0.1)) % 2 == 0:
        #     mid = ceil(log10(stone + 0.1)) // 2
        #     new_stones[stone // 10**mid] += stones[stone]
        #     new_stones[stone % 10**mid] += stones[stone]
        else:
            new_stones[stone * 2024] += stones[stone]

    stones = new_stones
    # print("# Stones:", sum(stones.values()))
    # input(f"Stones: {stones}")
    # print("Elapsed:", time() - begin)

print("# Stones:", sum(stones.values()))
print("Elapsed:", time() - begin)

# 225403963022184 - too low
# 225405189921031 - too high
# 225404711855335
