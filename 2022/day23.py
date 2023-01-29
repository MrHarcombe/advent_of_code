from io import StringIO
from collections import defaultdict

test = """..............
..............
.......#......
.....###.#....
...#...#.#....
....#...##....
...#.###......
...##.#.##....
....#..#......
..............
..............
.............."""

# test = """.....
# ..##.
# ..#..
# .....
# ..##.
# ....."""

# test = """################################
# ################################
# ##............................##
# ##.#...#.####.####.####.#...#.##
# ##.##.##.#....#..#.#..#..#.#..##
# ##.#.#.#.###..####.####...#...##
# ##.#...#.#....#.#..#.#....#...##
# ##.#...#.####.#..#.#..#...#...##
# ##............................##
# ################################
# ##............................##
# ##...#...#.#...#..##...###....##
# ##....#.#..##.##.#..#.#.......##
# ##.....#...#.#.#.####..###....##
# ##....#.#..#...#.#..#.....#...##
# ##...#...#.#...#.#..#..###....##
# ##............................##
# ################################
# ################################"""

# test = """..#....####...#.....###.#.#.#..#
# .#.#.#..#...#..##..#..#...#....#
# ..###..##.###.#..##..#####..#..#
# #..#.#..#.##..####..#..###..####
# .#.###.#.##...#.....#...#.##.##.
# .#.##..#..##.##...#.##..##.###..
# .#####.#.....#...#.#.#........##
# ##.##...###..##.#.####..#..#.##.
# .....#.##..#.##.#....##.##.#.#.#
# #.###.#.###......#.#...#.##.#.##
# #.#....###.#..#.#..####..#.#..##
# ##.#..###.....#.#.#....##.....#.
# #...###..#.#..#####.....#......#
# .##.###.....###.#..#.#.#..#...#.
# .####.###.#..#.#.####......##.#.
# #......##.####.#..#.#.##.#...#..
# ...##..#....#.#..#.#.#.#.###.###
# #.....#.###.#.#..#...#.###..#...
# ...####.##..##.#......##..#...##
# ..##.##.##..###.#..#...#..#.#.#.
# #....#..##.......##.#.#.##.#...#
# #.#####....###.#.#..####.#.#.#.#
# ##.##.###.##.#.##.......####...#
# ###.#..#.###......###..#..###.#.
# ..##.##.##.#####.#####..###.#.#.
# .####.#....#.##..###.#.##.#.##.#
# #....##.###...###..#...#..#.##.#
# .#..##..####..###.##.#####.##...
# ....#.###.#####.#.#..###....#..#
# #..#....##..#.#..######.##...###
# ###.#.##........#.#.#.###.#.####
# ####.#..##.##..#.###.#.####....."""

# test = """.###.
# #...#
# #.#.#
# #...#
# .###."""

def display_elves():
    minx = min(elves, key=lambda i: i[1])[1]
    maxx = max(elves, key=lambda i: i[1])[1]
    miny = min(elves, key=lambda i: i[0])[0]
    maxy = max(elves, key=lambda i: i[0])[0]
    print(f"({minx},{miny}) -> ({maxx},{maxy})")
    for row in range(minx, maxx+1):
        for col in range(miny, maxy+1):
            if (col, row) in elves:
                print('#', end="")
            else:
                print('.', end="")
        print()
    print()

direction_list = [(((-1,-1), (0,-1), (1,-1)), (0,-1)),
                  (((-1,1), (0,1), (1,1)),    (0,1)),
                  (((-1,-1), (-1,0), (-1,1)), (-1,0)),
                  (((1,-1), (1,0), (1,1)),    (1,0))]
elves = {}

row = 0
# with StringIO(test) as f:
with open("input23.txt") as f:
    for line in f:
        for i, ch in enumerate(line.strip()):
            if ch == "#":
                elves[(i, row)] = False
        row += 1
        
print("initially:", len(elves))

# print("Before Round: 1", direction_list[0][1])
# display_elves()
# input()

# which elves have neighbours, so want to move
for elf in elves:
    # consider all 8 neighbours
    for delta in ((-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1)):
        if (elf[0] + delta[0], elf[1] + delta[1]) in elves:
            elves[elf] = True
            break

i = 0
while sum([1 for n in elves.values() if n]) > 0:
# for i in range(10):
    # generating proposed moves
    proposed_elves = defaultdict(list)
    for elf in (elf for elf, want in elves.items() if want):
        elf_move = None

        # initially, prioritize north, then south, then west then east
        # cycle those priorities each round
        for checks, move in direction_list:
            free = True
            for check in checks:
                if (elf[0] + check[0], elf[1] + check[1]) in elves:
                    free = False
                    break
            if free:
                elf_move = move
                break

        if elf_move != None:
            proposed_elves[(elf[0] + elf_move[0], elf[1] + elf_move[1])].append(elf)

    # move to those destinations that only have one elf waiting
    for to_elf, from_elf in proposed_elves.items():
        if len(from_elf) == 1:
            del elves[from_elf[0]]
            elves[to_elf] = False

    for elf in (elf for elf, wanted in elves.items() if wanted):
        elves[elf] = False

    # cycle the direction_list
    direction_list.append(direction_list.pop(0))

    # which elves have neighbours, so want to move
    for elf in elves:
        # consider all 8 neighbours
        for delta in ((-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1)):
            if (elf[0] + delta[0], elf[1] + delta[1]) in elves:
                elves[elf] = True
                break

    # print("After Round:", i+1)
    # display_elves()
    # input("Next priority: " + str(direction_list[0][1]) + "\n")
    i += 1

# print("Round:", i+1)
# display_elves()

rx_min = min(elves, key=lambda i: i[0])[0]
rx_max = max(elves, key=lambda i: i[0])[0]
ry_min = min(elves, key=lambda i: i[1])[1]
ry_max = max(elves, key=lambda i: i[1])[1]
print(rx_min, rx_max, ry_min, ry_max, len(elves))

area = (rx_max - rx_min + 1) * (ry_max - ry_min + 1) - len(elves)
print(area)
print("Rounds:", i+1)

# 6083 too high (wo subtracting elves)
# 3688 too low (subtracting elves)
# 3845 too high (subtracting elves)
# 3689... stoopid man!!