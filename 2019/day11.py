from day9 import intcode

turns = [(0,-1), (1,0), (0,1), (-1,0)]

def paint(start):
    pos = (0,0)
    direction = 0
    hull = {pos:start}

    robot = intcode("p1", "input11.txt", [])
    while not robot.has_finished():
        # print(f"{pos=}, {hull.get(pos, 0)}, {direction=}")
        current = hull.get(pos, 0)
        robot.add_input(current)
        paint = None
        turn = None
        while robot.count_output() < 2 and not robot.has_finished():
            robot.execute_next()
        if not robot.has_finished():
            paint, turn = robot.get_output()
            # print(f"{paint=}, {turn=}")
            if paint is not None:
                if turn is not None:
                    hull[pos] = paint
                    direction = (direction + (-1 if turn == 0 else 1)) % 4
                    pos = tuple(p1+p2 for p1, p2 in zip(pos, turns[direction]))
                else:
                    print("Uh-oh")

    return hull

hull_part1 = paint(0)
print("Part 1:", len(hull_part1))

hull_part2 = paint(1)
width = max(hull_part2.keys(), key=lambda item:item[0])[0]
height = max(hull_part2.keys(), key=lambda item:item[1])[1]
output = []

for row in range(height+1):
    line = []
    for col in range(width+1):
        line.append("#" if hull_part2.get((col,row), 0) else " ")
    output.append("".join(line))

print("Part 2:")
print("\n".join(output))
