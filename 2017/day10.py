from io import StringIO
from math import prod

test = "3, 4, 1, 5"

# with StringIO(test) as f:
with open("input10.txt") as f:
    lengths = [int(n) for n in f.readline().strip().split(",")]

# loop = [n for n in range(5)]
loop = [n for n in range(256)]
skip = 0
position = 0
original_start = 0

for step in lengths:
    # print(step, skip)
    sub = loop[position:position+step][::-1]
    new_loop = loop[:position] + sub + loop[position+step:]
    position = (step + skip) % len(loop)
    original_start -= (step + skip)
    # print(loop, position)
    loop = new_loop[position:] + new_loop[:position]
    skip += 1

print(loop, original_start % len(loop))
print(prod(loop[original_start % len(loop):original_start % len(loop)+2]))
