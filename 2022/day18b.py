from io import StringIO
import matplotlib.pyplot as plt
import numpy as np

test = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""

def get_internal_neighbours(x,y,z, lava, bubbles):
    neighbours = []
    for possible in ((x-1,y,z), (x+1,y,z), (x,y-1,z), (x,y+1,z), (x,y,z-1), (x,y,z+1)):
        if possible in lava or possible in bubbles:
            neighbours.append(possible)
    return neighbours

def get_outward_facing_neighbours(x, y, z, lava, enclosing):
    neighbours = []
    for possible in ((x-1,y,z), (x+1,y,z), (x,y-1,z), (x,y+1,z), (x,y,z-1), (x,y,z+1)):
        if possible in enclosing:
            neighbours.append(possible)
    return neighbours

def get_enclosing(minx, miny, minz, maxx, maxy, maxz, lava):
    enclosing = set()
    
    # for dx, dy, dz in ((-1,0,0), (1,0,0), (0,-1,0), (0,1,0), (0,0,-1), (0,0,1)):
    # go from minx to maxx, for all y and z
    for y in range(miny, maxy+1):
        for z in range(minz, maxz+1):
            for x in range(minx, maxx+1):
                if (x,y,z) not in lava:
                    enclosing.add((x,y,z))
                else:
                    break

    # go from maxx to minx, for all y and z
    for y in range(miny, maxy+1):
        for z in range(minz, maxz+1):
            for x in range(maxx, minx-1, -1):
                if (x,y,z) not in lava:
                    enclosing.add((x,y,z))
                else:
                    break

    # go from miny to maxy, for all x and z
    for x in range(minx, maxx+1):
        for z in range(minz, maxz+1):
            for y in range(miny, maxy+1):
                if (x,y,z) not in lava:
                    enclosing.add((x,y,z))
                else:
                    break
    # go from maxy to miny, for all x and z
    for x in range(minx, maxx+1):
        for z in range(minz, maxz+1):
            for y in range(maxy, miny-1, -1):
                if (x,y,z) not in lava:
                    enclosing.add((x,y,z))
                else:
                    break

    # go from minz to maxz, for all x and y
    for x in range(minx, maxx+1):
        for y in range(miny, maxy+1):
            for z in range(minz, maxz+1):
                if (x,y,z) not in lava:
                    enclosing.add((x,y,z))
                else:
                    break
    # go from maxz to minz, for all x and y
    for x in range(minx, maxx+1):
        for y in range(miny, maxy+1):
            for z in range(maxz, minz-1, -1):
                if (x,y,z) not in lava:
                    enclosing.add((x,y,z))
                else:
                    break

    return enclosing

"""
Flood-fill (node):
  1. Set Q to the empty queue or stack.
  2. Add node to the end of Q.
  3. While Q is not empty:
  4.   Set n equal to the first element of Q.
  5.   Remove first element from Q.
  6.   If n is Inside:
         Set the n
         Add the node to the west of n to the end of Q.
         Add the node to the east of n to the end of Q.
         Add the node to the north of n to the end of Q.
         Add the node to the south of n to the end of Q.
  7. Continue looping until Q is exhausted.
  8. Return.

https://en.wikipedia.org/wiki/Flood_fill#Moving_the_recursion_into_a_data_structure
"""

def floodfill_enclosing(ox, oy, oz, lava):
    enclosed = set()
    queue = [(ox, oy, oz)]

    while len(queue) > 0:
        nx, ny, nz = queue.pop(0)

        if (nx, ny, nz) not in enclosed and (nx, ny, nz) not in lava and (minx <= nx <= maxx and miny <= ny <= maxy and minz <= nz <= maxz):
            enclosed.add((nx, ny, nz))
            queue.append((nx-1, ny, nz))
            queue.append((nx+1, ny, nz))
            queue.append((nx, ny-1, nz))
            queue.append((nx, ny+1, nz))
            queue.append((nx, ny, nz-1))
            queue.append((nx, ny, nz+1))

    return enclosed

def get_bubbles(lx, ly, lz, lava):
    bubbles = set()
    not_enclosed = set()

    for dx, dy, dz in ((-1,0,0), (1,0,0), (0,-1,0), (0,1,0), (0,0,-1), (0,0,1)):
        px, py, pz = lx, ly, lz

        # get past lava in one direction
        while (px, py, pz) in lava:
            px += dx
            py += dy
            pz += dz

        possibles = set()
        while minx <= px <= maxx and miny <= py <= maxy and minz <= pz <= maxz:
            if (px, py, pz) in lava:
                bubbles |= possibles
                break
            else:
                possibles.add((px,py,pz))
            px += dx
            py += dy
            pz += dz
        else:
            not_enclosed |= possibles

    # print(bubbles)

    for px, py, pz in bubbles:
        edges = 0
        for dx, dy, dz in ((-1,0,0), (1,0,0), (0,-1,0), (0,1,0), (0,0,-1), (0,0,1)):
            cx, cy, cz = px, py, pz
            while minx <= cx <= maxx and miny <= cy <= maxy and minz <= cz <= maxz:
                cx += dx
                cy += dy
                cz += dz
                if (cx, cy, cz) in lava:
                    # print((bx,by,bz), "found lava #", edges, (x,y,z), (dx,dy,dz))
                    edges += 1
                    break

        if edges < 6:
            # print((bx,by,bz),"not contained")
            not_enclosed.add((px,py,pz))

    bubbles -= not_enclosed

    return bubbles, not_enclosed

def explode(data):
    size = np.array(data.shape)*2
    data_e = np.zeros(size - 1, dtype=data.dtype)
    data_e[::2, ::2, ::2] = data
    return data_e

droplets = {}
minx,maxx=float("inf"),float("-inf")
miny,maxy=float("inf"),float("-inf")
minz,maxz=float("inf"),float("-inf")

with StringIO(test) as f:
# with open("input18.txt") as f:
    for line in f:
        x,y,z = [int(n) for n in line.strip().split(",")]
        minx,maxx=min(minx,x),max(maxx,x)
        miny,maxy=min(miny,y),max(maxy,y)
        minz,maxz=min(minz,z),max(maxz,z)
        droplets[(x,y,z)] = 0

minx -= 1
maxx += 1
miny -= 1
maxy += 1
minz -= 1
maxz += 1
print(minx,maxx,miny,maxy,minz,maxz)

bubbles = set()
# enclosing = get_enclosing(minx, miny, minz, maxx, maxy, maxz, droplets)
enclosing = floodfill_enclosing(minx, miny, minz, droplets)

for droplet in droplets:
    interior, exterior = get_bubbles(*droplet, droplets)
    bubbles |= interior

# print(bubbles)
# print(enclosing)

for droplet in droplets:
    # droplets[droplet] -= len(get_internal_neighbours(*droplet, droplets, bubbles))
    droplets[droplet] += len(get_outward_facing_neighbours(*droplet, droplets, enclosing))

# bubble_droplets = { bubble : 6 for bubble in bubbles }
# for droplet in bubble_droplets:
#     bubble_droplets[droplet] -= len(get_neighbours(*droplet, bubble_droplets))

# print(bubble_droplets)

lava_sa = sum(droplets.values())
# bubble_sa = sum(bubble_droplets.values())
# print(lava_sa, "+", bubble_sa, "=", lava_sa + bubble_sa)
print(lava_sa)

# prepare some coordinates
x, y, z = np.indices((maxx+1, maxy+1, maxz+1))

lava_v = np.zeros((maxx+1,maxy+1,maxz+1), dtype=bool)
for lx,ly,lz in droplets:
    lava_v[lx,ly,lz] = True
    # lava_array[lx,ly,lz] = 1
bubble_v = np.zeros((maxx+1,maxy+1,maxz+1), dtype=bool)
for bx,by,bz in bubbles:
    bubble_v[bx,by,bz] = True
    # bubble_array[bx,by,bz] = 2
enclosing_v = np.zeros((maxx+1,maxy+1,maxz+1), dtype=bool)
for ex,ey,ez in enclosing:
    enclosing_v[ex,ey,ez] = True

voxel_array = lava_v | bubble_v # | enclosing_v

colors = np.empty(voxel_array.shape, dtype=object)
colors[lava_v] = "#0000FF40"
colors[bubble_v] = "#FF0000FF"
colors[enclosing_v] = "#FFFF0010"

voxelarray_2 = explode(voxel_array)
colors_2 = explode(colors)

# Shrink the gaps
x, y, z = np.indices(np.array(voxelarray_2.shape) + 1).astype(float) // 2
x[0::2, :, :] += 0.05
y[:, 0::2, :] += 0.05
z[:, :, 0::2] += 0.05
x[1::2, :, :] += 0.95
y[:, 1::2, :] += 0.95
z[:, :, 1::2] += 0.95

# and plot everything
ax = plt.figure().add_subplot(projection='3d')
ax.voxels(x,y,z, voxelarray_2, facecolors=colors_2, edgecolor='#FFFFFF10')
# ax.voxels(voxel_array, facecolors=colors, edgecolor='#FFFFFF10')

plt.show()
