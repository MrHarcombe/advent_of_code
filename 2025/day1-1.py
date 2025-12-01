from io import StringIO

test = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""

# with StringIO(test) as data:
with open("input1.txt") as data:
    position = 50
    password = 0
    
    for turn in data:
        direction = turn[0]
        amount = int(turn[1:])
        # print(direction, amount)

        if direction == "L":
            position -= amount
            
        else:
            position += amount
            
        position %= 100
        if position == 0:
            password += 1
            
print("Part 1:", password)

# 5689 too low
# 6477 wrong
# 6755 too high
