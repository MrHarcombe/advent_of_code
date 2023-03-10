lights = {}

def parse_cmd(cmd):
  onoff=x1=x2=y1=y2=0

  coords = 0

  parts = cmd.split(" ")
  if parts[0] == "turn":
    coords = 2
    if parts[1] == "on":
      onoff = 1
    elif parts[1] == "off":
      onoff = 0
  elif parts[0] == "toggle":
    coords = 1
    onoff = 2
  else:
    print("?!", onoff)

  x1,y1 = map(int, parts[coords].split(","))
  x2,y2 = map(int, parts[coords+2].split(","))

  return onoff,x1,y1,x2,y2

cmd = "turn on 0,0 through 999,999"
cmd = "turn off 499,499 through 500,500"
cmd = "toggle 0,0 through 999,0"

with open("input.txt") as f:
  cmd = f.readline().strip()

  while cmd != "":
    onoff,x1,y1,x2,y2 = parse_cmd(cmd)
    # print(onoff,x1,y1,x2,y2)
    for i in range(x1, x2+1):
      for j in range(y1, y2+1):
        if onoff == 0:
          if (i,j) in lights:
            del lights[(i,j)]
        elif onoff == 1:
          lights[(i,j)] = 1
        else:
          if (i,j) in lights:
            del lights[(i,j)]
          else:
            lights[(i,j)] = 1
    cmd = f.readline().strip()

print(len(lights))