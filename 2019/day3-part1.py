from scipy.spatial import distance

#print(distance.cityblock([1,0], [0,1]))

paths = { (0,0) }

def move(cmd, x, y, line):
  if cmd[0] == 'U':
    fromx = x
    fromy = y
    
  elif cmd[0] == 'D':
    pass
  elif cmd[0] == 'L':
    pass
  elif cmd[0] == 'R':
    pass
  else:
    print("Uh-oh," cmd[0])

  return x, y

with open("test.txt") as f:
  first = f.readline()
  second = f.readline()

  x = 0, y = 0

  fparts = first.split(",")
  for fp in fparts:
    x, y = move(fp, x, y, 1)