from io import StringIO
from itertools import permutations

test = """5 1 9 5
7 5 3
2 4 6 8"""

sheet = []

# with StringIO(test) as f:
with open("input2.txt") as f:
    for line in f:
        sheet.append([int(n) for n in line.strip().split()])

checksum = 0
for row in sheet:
    for a,b in permutations(row, 2):
        if a % b == 0:
            checksum += a // b

print(checksum)