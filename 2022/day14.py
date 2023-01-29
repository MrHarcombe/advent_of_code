from io import StringIO
from collections import defaultdict

test = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

minx = None
miny = None
maxx = None
maxy = None

class cavedict(defaultdict):
    def __missing__(self, key):
        x,y = key
        if y == maxy+2:
            return 1
        else:
            return None

cave = cavedict()

def display_cave():
    all_coords = cave.keys()
    leastx = min(all_coords, key=lambda i:i[0])[0]
    leasty = min(all_coords, key=lambda i:i[1])[1]
    mostx = max(all_coords, key=lambda i:i[0])[0]
    mosty = max(all_coords, key=lambda i:i[1])[1]
    
    # print(minx,maxx, miny,maxy)
    for y in range(leasty-1, mosty+2):
        for x in range(leastx-1, mostx+2):
            print(cave.get((x,y), "."), end="")
        print()

def drop_sand(origin):
    x,y = origin

    # part b - stop if the origin is full already
    if cave.get(origin,None) == 1:
        return False

    # drop until hit something (or falling to infinity)
    while maxy + 2 > y and cave[(x,y+1)] == None:
        y += 1

    # fell into infinity - for part b, this counts as floor
    # if y >= maxy:
    #     return False

    # drop down-left?
    if cave[(x-1,y+1)] == None:
        # cave[(x-1,y+1)] = 1
        return drop_sand((x-1,y+1))
    # drop down-right?
    elif cave[(x+1,y+1)] == None:
        # cave[(x+1,y+1)] = 1
        return drop_sand((x+1,y+1))
    # leave here
    else:
        cave[(x,y)] = 1

    return True

# with StringIO(test) as f:
with open("input14.txt") as f:
    px,py = None, None
    for line in f:
        coords = line.split(" -> ")
        for coord in coords:
            x,y = [int(n) for n in coord.split(",")]
            if px != None:
                # print(px,py,x,y)
                if x != px:
                    # print("horizontal")
                    for wallx in range(min(px,x),max(px,x)+1):
                        cave[(wallx,y)] = 0
                else:
                    # print("vertical")
                    for wally in range(min(py,y),max(py,y)+1):
                        cave[(x,wally)] = 0
            px,py = x,y
        px,py = None,None
    
    all_coords = cave.keys()
    minx = min(all_coords, key=lambda i:i[0])[0]
    miny = min(all_coords, key=lambda i:i[1])[1]
    maxx = max(all_coords, key=lambda i:i[0])[0]
    maxy = max(all_coords, key=lambda i:i[1])[1]

# display_cave()
stopped = drop_sand((500,0))
while stopped:
     stopped = drop_sand((500,0))
print()
# display_cave()

print("sand:", sum(cave.values()))