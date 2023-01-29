from io import StringIO

test = """noop
addx 3
addx -5"""

test = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""

def update_display(time, strength, output):
    offset = (time-1)%40
    if strength-1 == offset:
        output[time-1] = '#'
    elif strength == offset:
        output[time-1] = '#'
    elif strength+1 == offset:
        output[time-1] = '#'

# with StringIO(test) as f:
with open("input10.txt") as f:
    time = 1
    strength = 1
    output = ["."] * 240

    for line in f:
        if line.startswith("noop"):
            update_display(time, strength, output)
            time += 1
                
        else:
            command, amount = line.split()
            amount = int(amount)
            
            for i in range(2):
                update_display(time, strength, output)
                time += 1

            strength += amount

for i in range(len(output) // 40):
    print(''.join(output[i*40:(i*40)+40]))
