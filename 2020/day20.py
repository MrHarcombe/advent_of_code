from functools import cache
from io import StringIO
from itertools import permutations, product

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
        print(row)

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

@cache
def match_vertical(tile_and_turn0, tile_and_turn1):
    # print("vertical:", tile_and_turn0, tile_and_turn1)
    tile0 = rearrange_tile(*tile_and_turn0)
    tile1 = rearrange_tile(*tile_and_turn1)
    return [row[-1] for row in tile0] == [row[0] for row in tile1]

@cache
def match_horizontal(tile_and_turn0, tile_and_turn1):
    # print("horizontal:", tile_and_turn0, tile_and_turn1)
    tile0 = rearrange_tile(*tile_and_turn0)
    tile1 = rearrange_tile(*tile_and_turn1)
    return tile0[-1] == tile1[0]

@cache
def match_pairs(size, side, pattern, current_matches, next_position):
    if next_position >= len(pattern):
        return True

    tile_a = current_matches[-1]
    tile_b = pattern[next_position]
    
    for turn in product(range(4), range(2)):
        # compare right edge to left edge
        if next_position % side and not match_vertical(tile_a, (tile_b, *turn)):
            continue

        # compare bottom row to top row
        if next_position // side and not match_horizontal(current_matches[next_position-side], (tile_b, *turn)):
            continue

        # if next_position > 1:
        #     print("Matched:", pattern, next_position, tile_a, (tile_b, turn))

        if match_pairs(size, side, pattern, (*current_matches, (tile_b, *turn)), next_position+1):
            return True

    return False

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
        if len(inputs.readline()) == 0:
            break
        tiles.append((tile_number, tuple(tile)))

num_tiles = len(tiles)
side_length = int(num_tiles ** 0.5)
array = []

for trial_order in permutations([n for n in range(num_tiles)], num_tiles):
# for trial_order in ((1,0,8,7,3,5,6,4,2),):
    complete = False

    for turn in product(range(4), range(2)):
        tile0 = (trial_order[0], *turn)

        complete = match_pairs(num_tiles, side_length, trial_order, (tile0,), 1)
        if complete:
            break

    if complete:
        break

print(f"{complete=}, {trial_order}")
# corners = 0, side, -side, -1
total = tiles[trial_order[0]][0] * tiles[trial_order[side_length-1]][0] * tiles[trial_order[-side_length]][0] * tiles[trial_order[-1]][0]
print("Part 1:", total)

