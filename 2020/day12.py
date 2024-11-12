from io import StringIO

test = """F10
N3
F7
R90
F11"""

FACINGS = ((0, 1), (1, 0), (0, -1), (-1, 0))

class Ship:
    def __init__(self):
        self.facing = 1
        self.pos = (0,0)
        self.waypoint = (10,1)

ship = Ship()
with open("input12.txt") as data:
# with StringIO(test) as data:
    for line in data:
        instruction = line[0]
        distance = int(line[1:])

        x, y = ship.pos
        match instruction:
            case "N":
                ship.pos = (x, y + distance)
            case "S":
                ship.pos = (x, y - distance)
            case "E":
                ship.pos = (x + distance, y)
            case "W":
                ship.pos = (x - distance, y)
            case "L":
                ship.facing -= distance // 90
                ship.facing %= 4
            case "R":
                ship.facing += distance // 90
                ship.facing %= 4
            case "F":
                dx, dy = FACINGS[ship.facing]
                dx *= distance
                dy *= distance
                ship.pos = (x + dx, y + dy)

        # print(line.strip(), ship.pos, ship.facing)

print("Part 1:", sum(map(abs, ship.pos)))

ship = Ship()
with open("input12.txt") as data:
# with StringIO(test) as data:
    for line in data:
        instruction = line[0]
        distance = int(line[1:])

        sx, sy = ship.pos
        wx, wy = ship.waypoint

        match instruction:
            case "N":
                ship.waypoint = (wx, wy + distance)
            case "S":
                ship.waypoint = (wx, wy - distance)
            case "E":
                ship.waypoint = (wx + distance, wy)
            case "W":
                ship.waypoint = (wx - distance, wy)
            case "F":
                ship.pos = (sx + wx * distance, sy + wy * distance)

            ###
            # 90° clockwise rotation: (x,y) becomes (y,−x)
            # 90° counterclockwise rotation: (x,y) becomes (−y,x)
            # 180° clockwise and counterclockwise rotation: (x,y) becomes (−x,−y)
            # 270° clockwise rotation: (x,y) becomes (−y,x)
            # 270° counterclockwise rotation: (x,y) becomes (y,−x)

            case "L":
                if distance == 90:
                    wx, wy = -wy, wx
                elif distance == 180:
                    wx, wy = -wx, -wy
                elif distance == 270:
                    wx, wy = wy, -wx
                else:
                    print("Huh?")

                ship.waypoint = (wx, wy)

            case "R":
                if distance == 90:
                    wx, wy = wy, -wx
                elif distance == 180:
                    wx, wy = -wx, -wy
                elif distance == 270:
                    wx, wy = -wy, wx
                else:
                    print("Huh?")

                ship.waypoint = (wx, wy)

        print(line.strip(), ship.pos, ship.waypoint)

print("Part 2:", sum(map(abs, ship.pos)))
