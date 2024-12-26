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


def can_move(warehouse, robot, direction):
    check = complex(robot)

    # check for east/west movement...
    if direction.real != 0:
        while 0 <= check.real + direction.real <= warehouse["MAX_X"]:
            check += direction
            if warehouse[check] == "#":
                return False
            elif warehouse[check] == ".":
                return True

        return False

    # check for north/south movement
    else:
        if warehouse[check + direction] == "#":
            return False
        elif warehouse[check + direction] == ".":
            return True
        elif warehouse[check + direction] == "[":
            return can_move(warehouse, check + direction, direction) and can_move(
                warehouse, check + direction + 1, direction
            )
        elif warehouse[check + direction] == "]":
            return can_move(warehouse, check + direction - 1, direction) and can_move(
                warehouse, check + direction, direction
            )
        else:
            input("(CanMove) Uh-oh:" + warehouse[check + direction])


def build_affected(warehouse, robot, direction):
    if warehouse[robot + direction] == ".":
        return {robot + direction}
    elif warehouse[robot + direction] == "[":
        return (
            {robot + direction, robot + direction + 1}
            | build_affected(warehouse, robot + direction, direction)
            | build_affected(warehouse, robot + direction + 1, direction)
        )
    elif warehouse[robot + direction] == "]":
        return (
            {robot + direction - 1, robot + direction}
            | build_affected(warehouse, robot + direction - 1, direction)
            | build_affected(warehouse, robot + direction, direction)
        )
    else:
        input("(MakeMove) Uh-oh:" + warehouse[robot + direction])
        return set()


def make_move(warehouse, robot, direction):
    step = complex(robot)

    # check for east/west movement...
    if direction.real != 0:
        while 0 <= step.real + direction.real <= warehouse["MAX_X"]:
            step += direction
            if warehouse[step] == ".":
                break

        if direction.real > 0:
            rng = range(
                int(max(robot.real, step.real)), int(min(robot.real, step.real)), -1
            )
        else:
            rng = range(
                int(min(robot.real, step.real)), int(max(robot.real, step.real))
            )
        for crate in rng:
            new = complex(crate, step.imag)
            old = complex(crate, step.imag) + direction * -1
            warehouse[new] = warehouse[old]
            del warehouse[old]

    # check for north/south movement
    else:
        affected = sorted(
            build_affected(warehouse, robot, direction),
            key=lambda crate: (crate.imag, crate.real),
            reverse=direction.imag > 0,
        )
        for crate in affected:
            if warehouse[crate] in ("[", "]"):
                new = crate + direction
                old = crate
                warehouse[new] = warehouse[old]
                del warehouse[old]

    return robot + direction


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

# test = """#######
# #...#.#
# #.....#
# #..OO@#
# #..O..#
# #.....#
# #######

# <vv<<^^<<^^"""

# test = """###########
# #.........#
# #.O.O@O.O.#
# ###########

# ^>>>>v<^<<<v<<"""


warehouse = defaultdict(lambda: ".")
moves = ""

# with StringIO(test) as input_data:
with open("input15.txt") as input_data:
    for y, line in enumerate(input_data):
        if line.strip() == "":
            break

        x = 0
        for ch in line.strip():
            if ch != ".":
                if ch == "@":
                    robot = complex(x, y)
                elif ch == "#":
                    warehouse[complex(x, y)] = ch
                    warehouse[complex(x + 1, y)] = ch
                elif ch == "O":
                    warehouse[complex(x, y)] = "["
                    warehouse[complex(x + 1, y)] = "]"
            x += 2

    warehouse["MAX_Y"] = y
    warehouse["MAX_X"] = x

    for line in input_data:
        moves += line.strip()

# display_warehouse(warehouse, robot)
# input()

for move in moves:
    direction = directions[move]
    # display_warehouse(warehouse, robot)
    # print("Move:", move, "=", direction)
    # input()
    if warehouse[robot + direction] == ".":
        robot += direction
    elif can_move(warehouse, robot, direction):
        # print("can move")
        robot = make_move(warehouse, robot, direction)
    # else:
    #     print("up against it")

gps_sum = 0
crate_positions = [k for k, v in warehouse.items() if v == "["]
for pos in crate_positions:
    gps_sum += pos.real + 100 * pos.imag

print("Part 2:", gps_sum)
