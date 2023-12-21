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

platform = {}

def display_platform(platform):
    for row in range(max_row):
        for col in range(max_col):
            ch = platform.get((row,col), ".")
            print(ch, end="")
        print()

sort_keys = {(-1,0): lambda k:(k[0],k[1]), (0,-1) : lambda k:(k[1],k[0]), (1,0): lambda k:(-k[0],-k[1]), (0,1) : lambda k:(-k[1],-k[0])}

def roll_boulders(platform, direction):
    for boulder in sorted([k for k in platform if platform[k] == "O"], key=sort_keys[direction]):
        roll = boulder
        new_roll = (boulder[0] + direction[0], boulder[1] + direction[1])
        while 0 <= new_roll[0] < max_row and 0 <= new_roll[1] < max_col and platform.get(new_roll, ".") == ".":
            roll = new_roll
            new_roll = (roll[0] + direction[0], roll[1] + direction[1])

        del platform[boulder]
        platform[roll] = "O"

# with StringIO(test) as data:
with open("input14.txt") as data:
    for row, line in enumerate(data):
        for col, ch in enumerate(line.strip()):
            if ch != ".":
                platform[(row,col)] = ch
                
    max_row = row+1
    max_col = col+1

# display_platform(platform)
# print()
# for boulder in sorted([k for k in platform if platform[k] == "O"], key=lambda k:(k[0],k[1])):
#     if boulder[0] == 0:
#         continue
#     
#     roll = boulder[0]
#     while roll > 0 and platform.get((roll-1, boulder[1]), ".") == ".":
#         roll -= 1
# 
#     # print(boulder, "->", (roll, boulder[1]))
# 
#     del platform[boulder]
#     platform[(roll, boulder[1])] = "O"

with open("output14.txt", "w") as trace:
    for count in range(250_000):
        for cycle in ((-1,0), (0,-1), (1,0), (0,1)):
            roll_boulders(platform, cycle)
            # display_platform(platform)
            # print()

        print(sum(max_row - boulder[0] for boulder in (k for k in platform if platform[k] == "O")), file=trace)
        if count % 500 == 0:
            print(count)
