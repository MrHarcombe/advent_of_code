with open("input.txt") as f:
  floors = f.readline()

final_floor = 0
for index, floor in enumerate(floors):
  if floor == ")":
    final_floor -= 1
  elif floor == "(":
    final_floor += 1
  else:
    print("?! ->", floor)

  if final_floor < 0:
    break

print(index, final_floor)