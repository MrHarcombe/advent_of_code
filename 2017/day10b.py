from io import StringIO
from math import prod

# test = "3, 4, 1, 5"
test = ""

with StringIO(test) as f:
# with open("input10.txt") as f:
    lengths = [ord(n) for n in f.readline().strip()]

lengths += [17, 31, 73, 47, 23]
# print(lengths)

# loop = [n for n in range(5)]
loop = [n for n in range(256)]

skip = 0
position = 0
original_start = 0

for i in range(64):
    for step in lengths:
        # print(step, skip)
        sub = loop[position:position+step][::-1]
        new_loop = loop[:position] + sub + loop[position+step:]
        position = (step + skip) % len(loop)
        original_start -= (step + skip)
        # print(loop, position)
        loop = new_loop[position:] + new_loop[:position]
        skip += 1

    # print(loop, original_start % len(loop))
    loop = loop[original_start % len(loop):] + loop[:original_start % len(loop)]
    original_start = 0
    position = (position + original_start) % len(loop)
    # print(loop)
    # print(prod(loop[:2]))

# print(loop)

dense = []
for i in range(0, len(loop), 16):
    value = loop[i]
    for j in range(i+1, i+16):
        value ^= loop[j]
    dense.append(f"{value:02x}")

print("".join(dense))
