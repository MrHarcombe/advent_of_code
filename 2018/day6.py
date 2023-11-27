from io import StringIO

def manhattan(pa,pb):
    return sum((abs(a - b) for a,b in zip(pa, pb)))

test = """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9"""

beacons = []
area = {}

# with StringIO(test) as data:
with open("input6.txt") as data:
    for line in data:
        x,y = map(int, line.strip().split(","))
        beacons.append((x,y))

min_x = min(beacons, key=lambda n:n[0])[0]
max_x = max(beacons, key=lambda n:n[0])[0]
min_y = min(beacons, key=lambda n:n[1])[1]
max_y = max(beacons, key=lambda n:n[1])[1]

for x in range(max_x+1):
    for y in range(max_y+1):
        distances = [manhattan((x,y), b) for b in beacons]
        min_to = min(distances)
        if distances.count(min_to) == 1:
            area[(x,y)] = distances.index(min_to)
        else:
            area[(x,y)] = "."

areas = [0] * len(beacons)
for i in range(len(beacons)):
    hits = [p[0] for p in area.items() if p[1] == i]
    if len([x for x,_ in hits if x in (min_x, max_x)]) > 0:
        continue
    if len([y for _,y in hits if y in (min_y, max_y)]) > 0:
        continue
    areas[i] = len(hits)

print("Part 1:", max(areas))

# for y in range(max(beacons, key=lambda n:n[1])[1]+1):
#     for x in range(max(beacons, key=lambda n:n[0])[0]+1):
#         print(area.get((x,y),"."), end="")
#     print()

safe_distance = 10000
safe_area = []

for x in range(min_x, max_x + 1):
    for y in range(min_y, max_y + 1):
        total = 0
        for b in beacons:
            total += manhattan((x,y), b)

        if total < safe_distance:
            safe_area.append((x,y))

print("Part 2:", len(safe_area))
