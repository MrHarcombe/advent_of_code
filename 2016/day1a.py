def manhattan_distance(beacon, other):
    distance = sum(abs(val1-val2) for val1, val2 in zip(beacon, other))
    # print('from:', beacon, 'to:', other, 'distance:', distance)
    return distance

def parse_input(text):
    for command in text.split(", "):
        direction = command[0]
        length = command[1:]
        # print(direction, length, end=" ")
        yield 90 if direction == "R" else -90, int(length)

def get_new_coord(current, bearing, length):
    x, y = current
    if bearing == 0:
        y += length
    elif bearing == 90:
        x += length
    elif bearing == 180:
        y -= length
    elif bearing == 270:
        x -= length
    return (x,y)

test1 = "R2, L3"
test2 = "R2, R2, R2"
test3 = "R5, L5, R5, R3"
test4 = "R8, R4, R4, R8"
part1 = "R3, L5, R1, R2, L5, R2, R3, L2, L5, R5, L4, L3, R5, L1, R3, R4, R1, L3, R3, L2, L5, L2, R4, R5, R5, L4, L3, L3, R4, R4, R5, L5, L3, R2, R2, L3, L4, L5, R1, R3, L3, R2, L3, R5, L194, L2, L5, R2, R1, R1, L1, L5, L4, R4, R2, R2, L4, L1, R2, R53, R3, L5, R72, R2, L5, R3, L4, R187, L4, L5, L2, R1, R3, R5, L4, L4, R2, R5, L5, L4, L3, R5, L2, R1, R1, R4, L1, R2, L3, R5, L4, R2, L3, R1, L4, R4, L1, L2, R3, L1, L1, R4, R3, L4, R2, R5, L2, L3, L3, L1, R3, R5, R2, R3, R1, R2, L1, L4, L5, L2, R4, R5, L2, R4, R4, L3, R2, R1, L4, R3, L3, L4, L3, L1, R3, L2, R2, L4, L4, L5, R3, R5, R3, L2, R5, L2, L1, L5, L1, R2, R4, L5, R2, L4, L5, L4, L5, L2, L5, L4, R5, R3, R2, R2, L3, R3, L2, L5"
test = part1

coord = (0,0)
bearing = 0
for turn, length in parse_input(test):
    # print(coord, bearing, end=" -> ")
    bearing += turn
    bearing %= 360
    coord = get_new_coord(coord, bearing, length)
    # print(bearing, coord)
print(manhattan_distance(coord, (0,0)))
