from collections import defaultdict
from io import StringIO

# from mpl_toolkits.mplot3d import axes3d
# import matplotlib.pyplot as plt
# from matplotlib import style

test = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""

# test = """1,0,1~1,2,1
# 1,0,3~1,0,6"""

# test = """0,0,1~0,1,1
# 1,1,1~1,1,1
# 0,0,2~0,0,2
# 0,1,2~1,1,2"""

# test = """0,0,1~1,0,1
# 0,1,1~0,1,2
# 0,0,5~0,0,5
# 0,0,4~0,1,4"""

class sandpile(defaultdict):
    def __missing__(self, key):
        if type(key) is tuple and len(key) == 3 and key[2] == 0:
            return "Floor"

        if key not in self:
            return None

def sort_by_z(line):
    a,b = line.strip().split("~")
    _,_,z1 = a.split(",")
    _,_,z2 = b.split(",")
    return (a,b) if a < b else (b,a)

def display_sandpile(pile):
    max_x = max(pile, key=lambda k:k[0])[0]
    max_y = max(pile, key=lambda k:k[1])[1]
    max_z = max(pile, key=lambda k:k[2])[2]
    
    for z in range(max_z,-1,-1):
        xs = ""
        for x in range(max_x+1):
            for y in range(max_y+1):
                if (x,y,z) in pile:
                    xs += str(pile[(x,y,z)])
                    break
            else:
                xs += "."
        ys = ""
        for y in range(max_y+1):
            for x in range(max_x+1):
                if (x,y,z) in pile:
                    ys += str(pile[(x,y,z)])
                    break
            else:
                ys += "."
        print(xs, "\t", ys, z)

def graph_sandpile(pile):
    style.use("ggplot")
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection="3d")
    ax1.set_aspect("equal")
    ax1.autoscale(True, "both", True)

    max_x = max(pile, key=lambda k:k[0])[0]
    max_y = max(pile, key=lambda k:k[1])[1]
    ax1.set_xbound(0,max_x)
    ax1.set_ybound(0,max_y)

    for s in pile:
        ax1.scatter([s[0]], [s[1]], [s[2]], c=[pile[s]], marker="s")

    plt.show()

def find_shapes_on_z(pile, z):
    return set(pile[k] for k in pile if k[2] == z)

def find_shape(pile, block):
    return [pos for pos,blk in pile.items() if blk == block]

def drop_shape(pile, block):
    for coords in find_shape(pile, block):
        del pile[coords]
        x, y, z = coords
        pile[(x, y, z-1)] = block
        

def find_shapes_relative(pile, block, z_offset):
    block_coords = find_shape(pile, block)
    relatives = set()
    for x, y, z in block_coords:
        relative = pile[(x, y, z + z_offset)]
        if relative != None and relative != block:
            relatives.add(relative)

    return relatives

def simulate_block_disintegrate(pile, block, previous=None, going=set()):
    above = find_shapes_relative(pile, block, 1)
    below = find_shapes_relative(pile, block, -1)
    
    if previous == None or below == {previous} or below <= going:
        response = {block}
        for a in above:
            response |= simulate_block_disintegrate(pile, a, block, going | response)
        return response

    return set()

pile = sandpile()

# with StringIO(test) as data:
with open("input22.txt") as data:
    full_data = data.readlines()

    # for block, line in enumerate(sorted(full_data, key=sort_by_z)):
    for block, line in enumerate(full_data):
        src, dst = line.strip().split("~")
        sx, sy, sz = map(int, src.split(","))
        dx, dy, dz = map(int, dst.split(","))

        for x in range(sx, dx+1):
            for y in range(sy, dy+1):
                for z in range(sz, dz+1):
                    pile[(x,y,z)] = block

    # *now* drop them... not one at a time...
    z = 2
    while z <= max(pile, key=lambda k:k[2])[2]:
        for block in find_shapes_on_z(pile, z):
            # display_sandpile(pile)
            # graph_sandpile(pile)
            # print(find_shape(pile, block))
            # input()

            below = find_shapes_relative(pile, block, -1)
            can_drop = len(below) == 0
            while can_drop:
                drop_shape(pile, block)
                below = find_shapes_relative(pile, block, -1)
                can_drop = len(below) == 0

            # display_sandpile(pile)
            # graph_sandpile(pile)
            # print(find_shape(pile, block))
            # input()

        # now move up a layer
        z += 1

toplevel = set()
multiples = set()

for block in range(max(pile.values())+1):
    above = find_shapes_relative(pile, block, 1)
    if len(above) == 0:
        # print("Can disintegrate", block)
        toplevel.add(block)

    else:
        if all(len(find_shapes_relative(pile, higher, -1)) > 1 for higher in above):
            multiples.add(block)

disintegrate = toplevel | multiples
print("Part 1:", len(disintegrate))

## 641, 747, 1061, 1110, 1238 too high
## 396, 602 not right

print("Part 2 candidate pool size:", len(set(pile.values()) - disintegrate))

total_blocks = 0
for block in set(pile.values()) - disintegrate:
    blocks = len(simulate_block_disintegrate(pile, block) - {block})
    # print("blocks for", block, "=", blocks)
    total_blocks += blocks
print("Part 2:", total_blocks)


