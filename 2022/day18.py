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

def get_neighbours(x,y,z, source):
    neighbours = []
    for possible in ((x-1,y,z), (x+1,y,z), (x,y-1,z), (x,y+1,z), (x,y,z-1), (x,y,z+1)):
        if possible in source:
            neighbours.append(possible)
    return neighbours

def get_bubbles(x,y,z, droplet_source):
    bubbles = set()
    for dx, dy, dz in ((-1,0,0), (1,0,0), (0,-1,0), (0,1,0), (0,0,-1), (0,0,1)):
        px, py, pz = x, y, z
        
        # get past lava in one direction
        while (px, py, pz) in droplet_source:
            px += dx
            py += dy
            pz += dz

        possibles = set()
        while minx <= px <= maxx and miny <= py <= maxy and minz <= pz <= maxz:
            if (px, py, pz) in droplet_source:
                bubbles |= possibles
                break
            else:
                possibles.add((px,py,pz))
            px += dx
            py += dy
            pz += dz

    # print(bubbles)

    not_enclosed = set()
    for bx, by, bz in bubbles:
        edges = 0
        for dx, dy, dz in ((-1,0,0), (1,0,0), (0,-1,0), (0,1,0), (0,0,-1), (0,0,1)):
            x,y,z = bx,by,bz
            while minx <= x <= maxx and miny <= y <= maxy and minz <= z <= maxz:
                x += dx
                y += dy
                z += dz
                if (x, y, z) in droplet_source:
                    # print((bx,by,bz), "found lava #", edges, (x,y,z), (dx,dy,dz))
                    edges += 1
                    break

        if edges < 6:
            # print((bx,by,bz),"not contained")
            not_enclosed.add((bx,by,bz))

    bubbles -= not_enclosed

    return bubbles

def explode(data):
    size = np.array(data.shape)*2
    data_e = np.zeros(size - 1, dtype=data.dtype)
    data_e[::2, ::2, ::2] = data
    return data_e

droplets = {}
minx,maxx=float("inf"),float("-inf")
miny,maxy=float("inf"),float("-inf")
minz,maxz=float("inf"),float("-inf")

# with StringIO(test) as f:
with open("input18.txt") as f:
    for line in f:
        x,y,z = [int(n) for n in line.strip().split(",")]
        minx,maxx=min(minx,x),max(maxx,x)
        miny,maxy=min(miny,y),max(maxy,y)
        minz,maxz=min(minz,z),max(maxz,z)
        droplets[(x,y,z)] = 6

for droplet in droplets:
    droplets[droplet] -= len(get_neighbours(*droplet, droplets))

bubbles = set()
for droplet in droplets:
    bubbles |= get_bubbles(*droplet, droplets)

# print(bubbles)

bubble_droplets = { bubble : 6 for bubble in bubbles }
for droplet in bubble_droplets:
    bubble_droplets[droplet] -= len(get_neighbours(*droplet, bubble_droplets))

# print(bubble_droplets)

lava_sa = sum(droplets.values())
bubble_sa = sum(bubble_droplets.values())
print(lava_sa, "+", bubble_sa, "=", lava_sa + bubble_sa)

# # prepare some coordinates
# voxelarray = np.zeros((maxx+1, maxy+1, maxz+1), dtype=np.short)
# for bx,by,bz in droplets:
#     voxelarray[bx,by,bz] = 1
# # print(voxelarray)
# 
# voxelarray_2 = explode(voxelarray)
# 
# # Shrink the gaps
# x, y, z = np.indices(np.array(voxelarray_2.shape) + 1).astype(float) // 2
# x[0::2, :, :] += 0.05
# y[:, 0::2, :] += 0.05
# z[:, :, 0::2] += 0.05
# x[1::2, :, :] += 0.95
# y[:, 1::2, :] += 0.95
# z[:, :, 1::2] += 0.95
# 
# # and plot everything
# ax = plt.figure().add_subplot(projection='3d')
# ax.voxels(x,y,z, voxelarray_2, facecolors=np.where(voxelarray_2,"#FFFFFF40","#FF0000"), edgecolor='#FFFFFF10')
# 
# plt.show()