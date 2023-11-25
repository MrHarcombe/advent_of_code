from collections import defaultdict
from io import StringIO

test = """#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2"""

hits = defaultdict(int)
claims = []

# with StringIO(test) as data:
with open("input3.txt") as data:
  for line in data:
    claim, _, lt, wh = line.strip().split()
    left, top = map(int, lt[:-1].split(","))
    width, height = map(int, wh.split("x"))
    claims.append((claim, left, top, width, height))

# print(claims)
# draw out claims
for claim in claims:
  for x in range(claim[1], claim[1]+claim[3]):
   for y in range(claim[2], claim[2]+claim[4]):
     hits[(x,y)] += 1

print("Part 1:", len([n for n in hits.values() if n > 1]))

# verify claims
for claim in claims:
  overlap = False
  for x in range(claim[1], claim[1]+claim[3]):
   for y in range(claim[2], claim[2]+claim[4]):
     if hits[(x,y)] > 1:
       overlap = True
  if overlap == False:
    print("Part 2:", claim[0])
