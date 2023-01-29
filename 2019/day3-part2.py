from scipy.spatial import distance

#print(distance.cityblock([1,0], [0,1]))

def move(cmd):
  if cmd[0] == 'U':
    return (0, 1)
  elif cmd[0] == 'D':
    return (0, -1)
  elif cmd[0] == 'L':
    return (-1, 0)
  elif cmd[0] == 'R':
    return (1, 0)
  else:
    print("Uh-oh,", cmd[0])

with open("part1.txt") as f:
  first = f.readline().strip()
  second = f.readline().strip()

  while first != "":
    print(first, "#", second)

    paths = { (0,0) : 0 }
    
    cx = 0
    cy = 0
    psteps = 0

    parts = first.split(",")
    for p in parts:
      x, y = move(p)
      #print("x=",x,"y=",y)
      for steps in range(int(p[1:])):
        cx += x
        cy += y
        psteps += 1
        if (cx,cy) not in paths:
          paths[(cx,cy)] = [1, psteps]

    cx = 0
    cy = 0
    psteps = 0

    parts = second.split(",")
    for p in parts:
      x, y = move(p)
      for steps in range(int(p[1:])):
        cx += x
        cy += y
        psteps += 1
        if (cx,cy) in paths:
          if paths[(cx, cy)][0] == 1:
            paths[(cx,cy)] = [3, paths[(cx, cy)][1], psteps]
        else:
          paths[(cx,cy)] = [2, psteps]

    #print(paths)
    pi = list(filter(lambda x: isinstance(x[1], list) and x[1][0] == 3, paths.items()))
    #print(pi)
    print(min([sum(x[1][1:]) for x in pi]))

    first = f.readline().strip()
    second = f.readline().strip()