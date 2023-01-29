#route = ">"
#route = "^>v<"
#route = "^v^v^v^v^v"

with open("input.txt") as f:
  route = f.readline()
  deliveries = { (0,0) : 1 }

  location = (0,0)
  for direction in route:
    if direction == ">":
      location = (location[0]+1,location[1])
    elif direction == "<":
      location = (location[0]-1,location[1])
    elif direction == "^":
      location = (location[0],location[1]+1)
    elif direction == "v":
      location = (location[0],location[1]-1)
    else:
      print("?! ->", direction)

    if location in deliveries:
      deliveries[location] += 1
    else:
      deliveries[location] = 1

print(len(deliveries))
#print(deliveries)
