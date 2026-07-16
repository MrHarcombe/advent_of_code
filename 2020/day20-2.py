from collections import defaultdict
from functools import cache
from io import StringIO
from itertools import permutations, product

import re

test = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###..."""

tiles = []

def print_tile(index, turns, flips):
    for row in rearrange_tile(index, turns, flips):
        print("".join(row))

@cache
def rearrange_tile(index, turns, flips):
    tile = tiles[index][1]
    for _ in range(turns):
        tile = tuple(zip(*tile[::-1]))
    if flips & 1:
        # flip vertically
        tile = tuple(row[::-1] for row in tile)
    elif flips & 2:
        # flip horizontally
        tile = tuple(tile[-n-1] for n in range(len(tile)))
    return tile

def match_vertical(tile_and_turn0, tile_and_turn1):
    # print("vertical:", tile_and_turn0, tile_and_turn1)
    tile0 = rearrange_tile(*tile_and_turn0)
    tile1 = rearrange_tile(*tile_and_turn1)
    return [row[-1] for row in tile0] == [row[0] for row in tile1]

def match_horizontal(tile_and_turn0, tile_and_turn1):
    # print("horizontal:", tile_and_turn0, tile_and_turn1)
    tile0 = rearrange_tile(*tile_and_turn0)
    tile1 = rearrange_tile(*tile_and_turn1)
    return tile0[-1] == tile1[0]

def build_tile_matches(tiles):
    side_matches = defaultdict(lambda: defaultdict(set))
    top_matches = defaultdict(lambda: defaultdict(set))

    for i in range(len(tiles)):
        for j in (n for n in range(len(tiles)) if n != i):
            for iturn in product(range(4), range(2)):
                for jturn in product(range(4), range(2)):
                    if match_vertical((i, *iturn), (j, *jturn)):
                        side_matches[i][(i, *iturn)].add((j, *jturn))
                    if match_horizontal((i, *iturn), (j, *jturn)):
                        top_matches[i][(i, *iturn)].add((j, *jturn))

    return side_matches, top_matches

def find_matching_tile(side, path, tile, turn):
    next_position = len(path)

    possible_sides = set()
    if next_position % side:
        possible_sides.update(side_matches[tile][(tile, *turn)])

    possible_tops = set()
    if next_position // side:
        above, *above_turn = path[next_position - side]
        possible_tops.update(top_matches[above][(above, *above_turn)])

    if len(possible_sides) == 0:
        return possible_tops
    elif len(possible_tops) == 0:
        return possible_sides
    else:
        return possible_sides & possible_tops

def dfs_use_all(start_tile, start_turn, tile_count, side):
    stack = [((start_tile, *start_turn), [(start_tile, *start_turn)], {start_tile})]

    while len(stack):
        (tile, *turn), path, visited = stack.pop()
        if len(path) == tile_count:
            return path

        neighbours = find_matching_tile(side, path, tile, (*turn,))
        for neighbour in neighbours:
            if neighbour[0] not in visited:
                stack.append((neighbour, path + [neighbour], visited | {neighbour[0]}))

    return None

# with StringIO(test) as inputs:
with open("input20.txt") as inputs:
    while True:
        tile = []
        line = inputs.readline().strip()
        if len(line) == 0:
            break
        tile_number = int(line.split()[1][:-1])
        for j in range(10):
            tile.append(tuple(inputs.readline().strip()))
        inputs.readline()
        tiles.append((tile_number, tuple(tile)))

tile_count = len(tiles)
side = int(tile_count ** 0.5)
array = []

side_matches, top_matches = build_tile_matches(tiles)

for tile_and_turn in product(range(tile_count), range(4), range(2)):
    order = dfs_use_all(tile_and_turn[0], tile_and_turn[1:], tile_count, side)
    if order:
        # print(f"{order}")
        # corners = 0, side, -side, -1
        total = tiles[order[0][0]][0] * tiles[order[side-1][0]][0] * tiles[order[-side][0]][0] * tiles[order[-1][0]][0]
        print("Part 1:", total)
        break

final_scan = []
for left_tile in range(0, len(order), side):
    scan_tile_size = len(tiles[left_tile][1])-2
    scan_row = [[] for n in range(scan_tile_size)]
    for tile in range(left_tile, left_tile + side):
        scan_tile = rearrange_tile(*order[tile])
        for row in range(1, len(scan_tile)-1):
            scan_row[row-1] += scan_tile[row][1:-1]

    final_scan.extend(scan_row)

tiles = [(0, final_scan)]
rearrange_tile.cache_clear()

# monster length:20, count of characters = 15

p0 = re.compile('..................#.')
p1 = re.compile('#....##....##....###')
p2 = re.compile('.#..#..#..#..#..#...')

for tile_and_turn in product(range(1), range(4), range(2)):
    found = False
    scan = rearrange_tile(*tile_and_turn)
    roughness = sum([1 for row in scan for ch in row if ch == "#"])
    for row in range(len(scan)-2):
        for col in range(len(scan[row])-20):
            r0 = "".join(scan[row])
            r1 = "".join(scan[row+1])
            r2 = "".join(scan[row+2])
            if p0.search(r0, col, col+20) and p1.search(r1, col, col+20) and p2.search(r2, col, col+20):
                # print("Found a monster!", (row, col))
                found = True
                roughness -= 15

    if found:
        #print_tile(*tile_and_turn)
        break

print("Part 2:", roughness)
