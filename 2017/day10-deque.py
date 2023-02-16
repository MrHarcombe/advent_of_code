from collections import deque
from io import StringIO
from math import prod

test = "3, 4, 1, 5"

with StringIO(test) as f:
# with open("input10.txt") as f:
    lengths = [int(n) for n in f.readline().strip().split(",")]

loop = deque((n for n in range(5)), 5)

skip = 0
position = 0
original_start = 0

for step in lengths:

