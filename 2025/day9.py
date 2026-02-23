from io import StringIO
from functools import cache
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
def is_inside(borders, point, min_x):

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

def build_rectangle_points(p1, p2):
    px1, py1 = p1
    px2, py2 = p2
    
    rectangle_points = set()
    for y in range(min(py1, py2), max(py1, py2)+1):
        for x in range(min(px1, px2), max(px1, px2)+1):
            rectangle_points.add((x,y))
            
    return rectangle_points

###
# Non-recursive flood fill from Wikipedia
# https://en.wikipedia.org/wiki/Flood_fill
#

def flood_fill(borders, start):
    filled_area = set(borders)

    queue = [start]
    while len(queue):
        fill = queue.pop(0)
        if fill not in filled_area:
            filled_area.add(fill)

            fill_x, fill_y = fill
            for ax, ay in ((-1,0),(1,0),(0,-1),(0,1)):
                next_fill = (fill_x + ax, fill_y + ay)
                if next_fill not in queue:
                    queue.append(next_fill)

    return filled_area

def part1(tiles):
    areas = {((x1,y1),(x2,y2)): (abs(x1-x2)+1) * (abs(y1-y2)+1) for ((x1,y1),(x2,y2)) in combinations(tiles,2)}
    return areas

def part2(tiles, all_areas, min_x):
    borders = build_borders(tiles)
    # print("built borders")
    # enclosed = flood_fill(borders, (tiles[0][0]+1, tiles[0][1]+1))
    # print("filled enclosed shape")

    ignore = False
    for (((x1,y1),(x2,y2)), area) in sorted(all_areas.items(), key=lambda item: -item[1]):
        ## take 1, failed
        # for x in range(min(x1, x2), max(x1, x2)+1):
        #     for y in range(min(y1, y2), max(y1, y2)+1):
        #         if (x,y) not in enclosed:
        #             ignore = True
        #             break
        #     if ignore:
        #         break
        # if not ignore:
        #     areas.append(abs(x1-x2+1) * abs(y1-y2+1))
        # ignore = False

        ## take 2, also failed
        # rect_borders = build_borders([(x1,y1),(x2,y1),(x2,y2),(x1,y2)])
        # if len(rect_borders.difference(enclosed)) == 0:
        #     areas.append(abs(x1-x2+1) * abs(y1-y2+1))

        ## take 3, using only "inside" ideas
        # [(x1,y1),(x2,y1),(x2,y2),(x1,y2)] - do need all four corners, as all four may bridge an "outside" area
        for tile in build_borders([(x1,y1),(x2,y1),(x2,y2),(x1,y2)]):
            if not is_inside(borders, tile, min_x):
                # print("Nope:", (x1,y1),(x2,y2))
                break
        else:
            # print((x1,y1),(x2,y2),(abs(x1-x2)+1) * (abs(y1-y2)+1))
            # biggest first, so return that
            return area

tiles = []
# with StringIO(test) as file:
with open("input9.txt") as file:
    for line in file:
        x,y = map(int, line.strip().split(","))
        tiles.append((x,y))

min_x = min(tiles, key=lambda item: item[0])[0]

begin = time()
all_areas = part1(tiles)
print("Part 1:", max(all_areas.values()))
print("Elapsed:", time() - begin)
print("Part 2:", part2(tiles, all_areas, min_x))
print("Total:", time() - begin)

# 4752742456 too high
# 4631560956 too high
