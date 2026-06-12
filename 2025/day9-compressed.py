from io import StringIO
from functools import cache
from bisect import bisect, insort
from itertools import combinations, pairwise
from time import time

test = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""

def build_borders(tiles):
    borders = []
    for t1, t2 in pairwise(tiles+[tiles[0]]):
        tx1, ty1 = t1
        tx2, ty2 = t2
        
        if tx1 == tx2:
            if ty1 < ty2:
                for by in range(ty1, ty2+1):
                    borders.append((tx1, by))
            else:
                for by in range(ty1, ty2-1, -1):
                    borders.append((tx1, by))
        
        elif ty1 == ty2:
            if tx1 < tx2:
                for bx in range(tx1, tx2+1):
                    borders.append((bx, ty1))
            else:
                for bx in range(tx1, tx2-1, -1):
                    borders.append((bx, ty1))
        
        else:
            print("Panic !!")
            print(t1, t2)

    return frozenset(borders)

@cache
def is_inside(borders, point, min_x=0):
    if point in borders:
        return True
    else:
        hits = 0
        x = point[0]
        on_border = False
        while x >= min_x - 1:
            if (x, point[1]) in borders:
                if not on_border:
                    hits += 1
                    on_border = True
            else:
                on_border = False
            x -= 1

        return hits == 1

def compress_coordinates(xy, tiles, compressed_tiles):
    return compressed_tiles[tiles.index(xy)]

def decompress_coordinates(xy, tiles, compressed_tiles):
    return tiles[compressed_tiles.index(xy)]

def part1(tiles):
    areas = {((x1,y1),(x2,y2)): (abs(x1-x2)+1) * (abs(y1-y2)+1) for ((x1,y1),(x2,y2)) in combinations(tiles,2)}
    return areas

def part2(tiles, compressed):
    borders = build_borders(compressed)
    possible_areas = []

    for pair in combinations(compressed, 2):
        (x1,y1), (x2,y2) = pair

        for tile in build_borders([(x1,y1),(x2,y1),(x2,y2),(x1,y2)]):
            if not is_inside(borders, tile):
                # print("Nope:", (x1,y1),(x2,y2))
                break
        else:
            tl = decompress_coordinates((x1,y1), tiles, compressed_tiles)
            br = decompress_coordinates((x2,y2), tiles, compressed_tiles)
            # print((x1,y1),(x2,y2), tl, br)
            possible_areas.append(((abs(tl[0]-br[0])+1) * (abs(tl[1]-br[1])+1), tl, br))
            
    return max(possible_areas)

tiles = []
# with StringIO(test) as file:
with open("input9.txt") as file:
    for line in file:
        x,y = map(int, line.strip().split(","))
        tiles.append((x,y))

unique_x = []
unique_y = []
compressed_tiles = []
for (x,y) in tiles:
    if x not in unique_x: insort(unique_x, x)
    if y not in unique_y: insort(unique_y, y)

for (x,y) in tiles:
    compressed_tiles.append((unique_x.index(x), unique_y.index(y)))

print("Part 1:", max(part1(tiles).values()))
print("Part 2:", part2(tiles, compressed_tiles)[0])
