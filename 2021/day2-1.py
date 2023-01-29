hpos = 0
dpos = 0

with open('input2.txt') as file:
    for line in file:
        direction, amount = line.split()

        if direction == 'up':
            dpos -= int(amount)
        elif direction == 'down':
            dpos += int(amount)
        else:
            hpos += int(amount)

print(hpos*dpos)
