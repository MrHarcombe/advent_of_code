from io import StringIO
from itertools import product


def convert_schematic(schematic):
    columns = []
    for col in range(len(schematic[0])):
        columns.append(sum(1 for row in schematic if row[col] == "#"))
    return tuple(columns)


test = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""

locks = []
keys = []

# with StringIO(test) as input_data:
with open("input25.txt") as input_data:
    blank = " "
    while blank != "":
        schematic = []
        for _ in range(7):
            schematic.append(input_data.readline().strip())
        if schematic[0] == "#" * 5:
            locks.append(convert_schematic(schematic[1:]))
        else:
            keys.append(convert_schematic(schematic[:-1]))

        blank = input_data.readline()

# print("Locks:", locks)
# print("Keys:", keys)

possibles = set()
for lock, key in product(locks, keys):
    # print(lock, key)
    possible = True
    for l, k in zip(lock, key):
        if l + k >= 6:
            possible = False
    if possible:
        possibles.add((lock, key))

print("Day 25:", len(possibles))
