from io import StringIO

test = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""

# test = """..|..
# .....
# ..-.."""

# test = """...\\...
# ..............
# -......
# .......
# \\../..."""

# test = """|....-
# ......
# ......
# -....|"""

# test = """......|...\\..\\...
# ..../........|...
# ....\\.-.../......
# ......|....../...
# ................."""

mirrors = {
    "/": {
        (-1,0): (0,1),  # N -> E
        (0,1): (-1,0),  # E -> N
        (1,0): (0,-1),  # S -> W
        (0,-1): (1,0)  # W -> S
        },
    "\\": {
        (-1,0): (0,-1),  # N -> W
        (0,1): (1,0),  # E -> S
        (1,0): (0,1),  # S -> E
        (0,-1): (-1,0)  # W -> N
        }
    }

splitters = {
    "|": {
        (-1,0): [(-1,0)],
        (0,1): [(-1,0),(1,0)],
        (1,0): [(1,0)],
        (0,-1): [(-1,0),(1,0)]
        },
    "-": {
        (-1,0): [(0,-1),(0,1)],
        (0,1): [(0,1)],
        (1,0): [(0,-1),(0,1)],
        (0,-1): [(0,-1)]
        }
    }

cavern = {}

# with StringIO(test) as data:
with open("input16.txt") as data:
    for row, line in enumerate(data):
        for col, ch in enumerate(line.strip()):
            if ch != ".":
                cavern[(row,col)] = ch

min_row = 0
min_col = 0
max_row = row
max_col = col

def calculate_energised_cells(start, dx, cavern):
    energised = set()
    visited = set()

    # for row in range(max_row+1):
    #     for col in range(max_col+1):
    #         print(cavern.get((row,col), "."), end="")
    #     print()

    # print()
    # print("---")
    # print()

    beams = [(start, dx)]
    while len(beams) > 0:
        # print("-> beams:", beams)
        pos, dx = beams.pop(0)

        if 0 <= pos[0] + dx[0] <= max_row and 0 <= pos[1] + dx[1] <= max_col:
            new_pos = (pos[0] + dx[0], pos[1] + dx[1])
            if (new_pos, dx) not in visited:
                visited.add((new_pos, dx))
                energised.add(new_pos)
                underfoot = cavern.get(new_pos, ".")

                if underfoot in ("/", "\\"):
                    new_dx = mirrors[underfoot][dx]
                    beams.append((new_pos, new_dx))
                elif underfoot in ("|", "-"):
                    for new_dx in splitters[underfoot][dx]:
                        beams.append((new_pos, new_dx))
                else:
                    beams.append((new_pos, dx))

        # print("<- beams:", beams)

    # for row in range(max_row+1):
    #     for col in range(max_col+1):
    #         print("#" if (row,col) in energised else ".", end="")
    #     print()

    return energised

# initial beam is TL and moving E
part1_beam = ((0,-1), (0,1))
print("Part 1:", len(calculate_energised_cells(*part1_beam, cavern)))

cells = []
for row in range(max_row+1):
    for col, dx in ((-1, (0, 1)), (max_col+1, (0, -1))):
        cells.append(len(calculate_energised_cells((row, col), dx, cavern)))
for row, dx in ((-1, (1,0)), (max_row+1, (-1,0))):
    for col in range(max_col+1):
        cells.append(len(calculate_energised_cells((row, col), dx, cavern)))

print("Part 2:", max(cells))
