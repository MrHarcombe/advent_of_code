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

# test = """R1050"""

with open("day1.log", "w") as output:
    # with StringIO(test) as data:
    with open("input1.txt") as data:
        position = 50
        password = 0
        
        for turn in data:
            direction = turn[0]
            amount = int(turn[1:])

            started_on_zero = position == 0
            scrolled_to_zero = False

            # move to new position
            if direction == "L":
                position -= amount
            else:
                position += amount

            # if turning left, may turn below 0
            while position < 0:
                position += 100

                # if didn't start at 0, count the first sub-zero as a lap
                if not started_on_zero:
                    password += 1
                else:
                    # once that's past, reset but also remember that we scrolled to/past zero
                    scrolled_to_zero = True
                    started_on_zero = False
                
                print("-<-", direction, amount, position, password, started_on_zero, scrolled_to_zero, file=output)

            # if turning right, may turn past 99 - wherever we started from, passing counts as it'll be a full turn
            while position > 99:
                password += 1
                position -= 100
                scrolled_to_zero = True

                print("->-", direction, amount, position, password, started_on_zero, scrolled_to_zero, file=output)

            # only award a final tick if we landed exactly on 0 and didn't scroll to there
            if position == 0 and not scrolled_to_zero:
                password += 1

            print("-->", direction, amount, position, password, started_on_zero, scrolled_to_zero, file=output)

print("Part 2:", password)

# 5689 too low
# 6131 6438 6477 6658 wrong
# 6755 too high