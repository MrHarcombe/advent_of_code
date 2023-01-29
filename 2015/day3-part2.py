#route = ">"
#route = "^>v<"
#route = "^v^v^v^v^v"

with open("input.txt") as f:
  route = f.readline()
  #route = "^v"
  #route = "^>v<"
  #route = "^v^v^v^v^v"
  deliveries = { (0,0) : 1 }

  santa_location = (0,0)
  robot_location = (0,0)
  for index, direction in enumerate(route):
    if direction == ">":
      if index % 2 == 0:
        santa_location = (santa_location[0]+1,santa_location[1])
      else:
        robot_location = (robot_location[0]+1,robot_location[1])
    elif direction == "<":
      if index % 2 == 0:
        santa_location = (santa_location[0]-1,santa_location[1])
      else:
        robot_location = (robot_location[0]-1,robot_location[1])
    elif direction == "^":
      if index % 2 == 0:
        santa_location = (santa_location[0],santa_location[1]+1)
      else:
        robot_location = (robot_location[0],robot_location[1]+1)
    elif direction == "v":
      if index % 2 == 0:
        santa_location = (santa_location[0],santa_location[1]-1)
      else:
        robot_location = (robot_location[0],robot_location[1]-1)
    else:
      print("?! ->", direction)

    if index % 2 == 0:
      if santa_location in deliveries:
        deliveries[santa_location] += 1
      else:
        deliveries[santa_location] = 1
    else:
      if robot_location in deliveries:
        deliveries[robot_location] += 1
      else:
        deliveries[robot_location] = 1

print(len(deliveries))
#print(deliveries)
