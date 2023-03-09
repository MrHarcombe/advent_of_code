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

# print(loop, skip, position)

for step in lengths:
    sub = []
    for n in range(step):
        sub.append(loop[(position + n)%len(loop)])
        
    for n in range(step):
        loop[(position + n)%len(loop)] = sub.pop()

    position = (position + step + skip) % len(loop)
    skip += 1

    # print(loop, skip, position)

print(loop[0]*loop[1])
