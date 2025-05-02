from io import StringIO

test = """..X...
.SAMX.
.A..A.
XMAS.S
.X...."""

test = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

to_find = "XMAS"
grid = []


def check_from_here1(grid, y, x):
    found = 0
    for dy, dx in (
        (0, 1),
        (1, 1),
        (1, 0),
        (1, -1),
        (0, -1),
        (-1, -1),
        (-1, 0),
        (-1, 1),
    ):
        slice = [
            grid[y + n * dy][x + n * dx]
            for n in range(4)
            if y + n * dy in range(len(grid)) and x + n * dx in range(len(grid[y]))
        ]
        if slice == ["X", "M", "A", "S"]:
            found += 1
    return found


def check_from_here2(grid, y, x):
    found = 0
    slice = [
        grid[y + dy][x + dx]
        for dy, dx in (
            (-1, -1),
            (-1, 1),
            (1, 1),
            (1, -1),
        )
        if y + dy in range(len(grid)) and x + dx in range(len(grid[y]))
    ]
    if slice in (
        ["M", "M", "S", "S"],
        ["S", "S", "M", "M"],
        ["S", "M", "M", "S"],
        ["M", "S", "S", "M"],
    ):
        found = 1
    return found


# with StringIO(test) as input_data:
with open("input4.txt") as input_data:
    for line in input_data:
        grid.append(list(line.strip()))

count1 = 0
count2 = 0
for y in range(len(grid)):
    for x in range(len(grid[y])):
        if grid[y][x] == to_find[0]:
            count1 += check_from_here1(grid, y, x)
        if grid[y][x] == to_find[2]:
            count2 += check_from_here2(grid, y, x)

print("Part 1:", count1)
print("Part 2:", count2)
