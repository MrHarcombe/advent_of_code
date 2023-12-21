from collections import defaultdict
from io import StringIO

test = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

platform = defaultdict(list)

def display_platform(platform):
    for row in range(max_row):
        for col in range(max_col):
            match = [i for i in platform.items() if (row,col) in i[1]]
            ch = "." if len(match) == 0 else match[0][0]
            print(ch, end="")
        print()

sort_keys = {(-1,0): lambda k:(k[0],k[1]), (0,-1) : lambda k:(k[1],k[0]), (1,0): lambda k:(-k[0],-k[1]), (0,1) : lambda k:(-k[1],-k[0])}

def roll_boulders(platform, direction):
    platform["O"].sort(key=sort_keys[direction])

    for i, boulder in enumerate(platform["O"]):
        roll = boulder
        new_roll = (boulder[0] + direction[0], boulder[1] + direction[1])
        
        while 0 <= new_roll[0] < max_row and 0 <= new_roll[1] < max_col and new_roll not in platform["O"] and new_roll not in platform["#"]:
            roll = new_roll
            new_roll = (roll[0] + direction[0], roll[1] + direction[1])

        platform["O"][i] = roll

# with StringIO(test) as data:
with open("input14.txt") as data:
    for row, line in enumerate(data):
        for col, ch in enumerate(line.strip()):
            if ch != ".":
                platform[ch].append((row,col))

    max_row = row+1
    max_col = col+1

with open("day14-trace.txt", "w") as trace:
    # for count in range(1_000_000_000):
    for count in range(250_000):
    # for count in range(3):
        for cycle in ((-1,0), (0,-1), (1,0), (0,1)):
            roll_boulders(platform, cycle)
            # display_platform(platform)
            # print()

        print(sum(max_row - boulder[0] for boulder in (b for b in platform["O"])), file=trace)
        if count % 500 == 0:
            print(count)
