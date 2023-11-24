from io import StringIO

test = """+1
-2
+3
+1"""

drift = 0
changes = []
# with StringIO(test) as data:
with open("input1.txt") as data:
  for line in data:
    changes.append(int(line))
    # drift += int(line)

# print("Part 1:", drift)

duplicate = False
seen = set()
while not duplicate:
  for change in changes:
    drift += change
    if drift in seen:
      duplicate = True
      break
    else:
      seen.add(drift)

print("Part 2:", drift)
