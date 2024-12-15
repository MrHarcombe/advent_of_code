from collections import defaultdict
from io import StringIO

directions = {"^": (0, -1), ">": (1, 0), "v": (0, 1), "<": (-1, 0)}


def display_warehouse(warehouse, robot):
    for y in range(warehouse["MAX_Y"] + 1):
        row = []
        for x in range(warehouse["MAX_X"] + 1):
            if (x, y) == robot:
                row.append("@")
            elif (x, y) in warehouse:
                row.append(warehouse[(x, y)])
            else:
                row.append(" ")
        print("".join(row))


def is_space(warehouse, robot, direction):
    x, y = robot
    dx, dy = direction

    while 0 <= x + dx <= warehouse["MAX_X"] and 0 <= y + dy <= warehouse["MAX_Y"]:
        x += dx
        y += dy
        if warehouse[(x, y)] == "#":
            return False

    return True


test = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

warehouse = defaultdict(lambda: ".")
moves = ""

with StringIO(test) as input_data:
    for y, line in enumerate(input_data):
        if line.strip() == "":
            break

        for x, ch in enumerate(line.strip()):
            if ch != ".":
                if ch == "@":
                    robot = (x, y)
                else:
                    warehouse[(x, y)] = ch

    warehouse["MAX_Y"] = y
    warehouse["MAX_X"] = x

    for line in input_data:
        moves += line.strip()

print(warehouse)
print(robot)
print(moves)

for move in moves:
    direction = directions[move]
    display_warehouse(warehouse, robot)
    print("Move:", direction)
    if is_space(warehouse, robot, direction):
        print("there's space")
    else:
        print("up against it")
    input()
