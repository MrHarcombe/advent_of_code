from collections import defaultdict
from io import StringIO

directions = {"^": 0 - 1j, ">": 1 + 0j, "v": 0 + 1j, "<": -1 + 0j}


def display_warehouse(warehouse, robot):
    for y in range(warehouse["MAX_Y"] + 1):
        row = []
        for x in range(warehouse["MAX_X"] + 1):
            if complex(x, y) == robot:
                row.append("@")
            elif complex(x, y) in warehouse:
                row.append(warehouse[complex(x, y)])
            else:
                row.append(" ")
        print("".join(row))


def is_space(warehouse, robot, direction):
    check = complex(robot)
    while (
        0 <= check.real + direction.real <= warehouse["MAX_X"]
        and 0 <= check.imag + direction.imag <= warehouse["MAX_Y"]
    ):
        check += direction
        if warehouse[check] == "#":
            return False
        elif warehouse[check] == ".":
            return True

    return False


def shift_contents(warehouse, robot, direction):
    gap = complex(robot) + direction

    while (
        0 <= gap.real + direction.real <= warehouse["MAX_X"]
        and 0 <= gap.imag + direction.imag <= warehouse["MAX_Y"]
    ):
        gap += direction
        if warehouse[gap] == ".":
            break

    del warehouse[robot + direction]
    warehouse[gap] = "O"


test = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

test = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

warehouse = defaultdict(lambda: ".")
moves = ""

# with StringIO(test) as input_data:
with open("input15.txt") as input_data:
    for y, line in enumerate(input_data):
        if line.strip() == "":
            break

        for x, ch in enumerate(line.strip()):
            if ch != ".":
                if ch == "@":
                    robot = complex(x, y)
                else:
                    warehouse[complex(x, y)] = ch

    warehouse["MAX_Y"] = y
    warehouse["MAX_X"] = x

    for line in input_data:
        moves += line.strip()

# print(warehouse)
# print(robot)
# print(moves)

for move in moves:
    direction = directions[move]
    # display_warehouse(warehouse, robot)
    # print("Move:", direction)
    if warehouse[robot + direction] == ".":
        robot += direction
    elif is_space(warehouse, robot, direction):
        shift_contents(warehouse, robot, direction)
        robot += direction
    # else:
    #     print("up against it")

gps_sum = 0
crate_positions = [k for k, v in warehouse.items() if v == "O"]
for pos in crate_positions:
    gps_sum += pos.real + 100 * pos.imag

print("Part 1:", gps_sum)
