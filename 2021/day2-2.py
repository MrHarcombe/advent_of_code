hpos = 0
dpos = 0
aim = 0

with open('input2.txt') as file:
    for line in file:
        direction, amount = line.split()

        if direction == 'up':
            aim -= int(amount)
        elif direction == 'down':
            aim += int(amount)
        else:
            hpos += int(amount)
            dpos += aim * int(amount)

print(hpos*dpos)
