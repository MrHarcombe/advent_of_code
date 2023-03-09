from io import StringIO
from math import prod

# test = "3, 4, 1, 5"
test = ""

# with StringIO(test) as f:
with open("input10.txt") as f:
    lengths = [ord(n) for n in f.readline().strip()]

lengths += [17, 31, 73, 47, 23]
# print(lengths)

# loop = [n for n in range(5)]
loop = [n for n in range(256)]

skip = 0
position = 0

# print(loop, skip, position)

for rnd in range(64):
    for step in lengths:
        sub = []
        for n in range(step):
            sub.append(loop[(position + n)%len(loop)])
            
        for n in range(step):
            loop[(position + n)%len(loop)] = sub.pop()

        position = (position + step + skip) % len(loop)
        skip += 1

dense = []
for i in range(0, len(loop), 16):
    value = loop[i]
    for j in range(i+1, i+16):
        value ^= loop[j]
    dense.append(f"{value:02x}")

print("".join(dense))
