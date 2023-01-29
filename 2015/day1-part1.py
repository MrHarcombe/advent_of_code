with open("input.txt") as f:
  floors = f.readline()

final_floor = 0
for floor in floors:
  if floor == ")":
    final_floor -= 1
  elif floor == "(":
    final_floor += 1
  else:
    print("?! ->", floor)

print(final_floor)  