from io import StringIO
from math import log10, ceil
from time import time

test = """0 1 10 99 999"""
test = "125 17"


# with StringIO(test) as input_data:
with open("input11.txt") as input_data:
    for line in input_data:
        stones = list(map(int, line.strip().split()))

begin = time()
for step in range(75):
    print(f"Step {step+1}")
    ix = 0
    while ix < len(stones):
        stone = stones[ix]
        if stone == 0:
            stones[ix] = 1
            ix += 1
        elif log10(stone) > 0 and ceil(log10(stone)) % 2 == 0:
            mid = ceil(log10(stone)) // 2
            stones[ix] = stone // 10**mid
            stones.insert(ix + 1, stone % 10**mid)
            ix += 2
        else:
            stones[ix] = stone * 2024
            ix += 1

    print("# Stones:", len(stones))
    print("Elapsed:", time() - begin)
    # print(f"{step+1}:", stones)

# print("Stones:", len(stones))
# print("Elapsed:", time() - begin)
