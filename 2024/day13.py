from io import StringIO
import numpy as np

test = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

presses1 = 0
presses2 = 0

# with StringIO(test) as input_data:
with open("input13.txt") as input_data:
    bax = 0
    bay = 0
    bbx = 0
    bby = 0
    px1 = 0
    py1 = 0
    for line in input_data:
        if line.strip().startswith("Button A:"):
            x, y = line[9:].split(", ")
            bax, bay = int(x[2:]), int(y[2:])
        elif line.strip().startswith("Button B:"):
            x, y = line[9:].split(", ")
            bbx, bby = int(x[2:]), int(y[2:])
        elif line.strip().startswith("Prize: "):
            x, y = line[7:].split(", ")
            px1, py1 = int(x[2:]), int(y[2:])
            px2, py2 = int(x[2:]) + 10000000000000, int(y[2:]) + 10000000000000

            a1, b1 = np.linalg.solve([[bax, bbx], [bay, bby]], [px1, py1])
            if 0 < a1 <= 100 and 0 < b1 <= 100:
                if round(a1, 2) == int(a1 + 0.01) and round(b1, 2) == int(b1 + 0.01):
                    presses1 += 3 * round(a1, 0) + round(b1, 0)

            a2, b2 = np.linalg.solve([[bax, bbx], [bay, bby]], [px2, py2])
            if round(a2, 2) == int(a2 + 0.01) and round(b2, 2) == int(b2 + 0.01):
                presses2 += 3 * round(a2, 0) + round(b2, 0)

print("Part 1:", presses1)
print("Part 2:", presses2)

# 21553 too low
# 31505 too high
