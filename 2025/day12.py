from functools import cache
from io import StringIO
from itertools import repeat, product
from math import prod
from time import time

import numpy as np
import re

test = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2"""


def build_packages(counts, gifts):
    parcels = []
    for gift, count in enumerate(counts):
        parcels += repeat(gifts[gift], count)

    return product(*parcels)

@cache
def check_fits(size, region, x, y, parcel):
    npparcel = np.reshape(parcel, (3,3))
    npregion = np.reshape(region, size)

    padded_parcel = np.pad(npparcel, ((y,npregion.shape[0]-3-y),(x,npregion.shape[1]-3-x)), constant_values=0)
    new_region = npregion + padded_parcel
    if np.max(new_region) < 2:
        return new_region
    
    return None


# @cache
def place_packages(size, region, parcels):
    if len(parcels) == 0:
        return True

    parcel = parcels[0]
    parcels = tuple(parcels[1:])

    for y in range(size[0]-3+1):
        for x in range(size[1]-3+1):
            new_region = check_fits(size, region, x, y, parcel)
            if new_region is not None:
                return place_packages(size, tuple(np.reshape(new_region, -1)), parcels)

    return False


gifts = {}
trees = []

# with StringIO(test) as data:
with open("input12.txt") as data:
    # prepare the gifts, rotated and flipped
    for _ in range(6):
        gift = re.match("([0-9]):", data.readline()).group(1)
        shape = ""
        for _ in range(3):
            shape += data.readline().strip()
        shape = shape.replace(".", "0").replace("#", "1")
        shape = np.asarray(list(map(int, shape)), np.int8)
        shape = np.reshape(shape, (3,3))

        shapes = [tuple(np.reshape(shape, -1))]
        for turn in range(4):
            rot_shape = tuple(np.reshape(np.rot90(shape, turn), -1))
            if not any((s == rot_shape) for s in shapes):
                shapes.append(rot_shape)
            flip_shape = tuple(np.reshape(np.flipud(shape), -1))
            if not any((s == flip_shape) for s in shapes):
                shapes.append(flip_shape)
            flip_shape = tuple(np.reshape(np.fliplr(shape), -1))
            if not any((s == flip_shape) for s in shapes):
                shapes.append(flip_shape)
        
        gifts[int(gift)] = shapes

        data.readline()

    # now work through the trees
    for line in data:
        tree, counts = line.strip().split(": ")
        tree_y, tree_x = list(map(int, tree.split("x")))
        counts = list(map(int, counts.split()))
        
        trees.append(((tree_x, tree_y), tuple([0]*tree_x*tree_y), tuple(counts)))

# now the work begins!
begin = time()
region_count = 0
for size, region, counts in trees:
    for possible_packages in build_packages(counts, gifts):
        # possible_packages
        if place_packages(size, region, possible_packages):
            region_count += 1
            break

print("Part 1:", region_count)
print("Elapsed:", time() - begin)
