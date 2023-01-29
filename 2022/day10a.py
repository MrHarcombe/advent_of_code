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

intervals = (20,60,100,140,180,220)
strengths = []

#with StringIO(test) as f:
with open("input10.txt") as f:
    time = 0
    strength = 1
    for line in f:
        if line.startswith("noop"):
            time += 1
            if time in intervals:
                print(line.strip(), time, strength)
                strengths.append(strength)
                
        else:
            command, amount = line.split()
            amount = int(amount)
            if time + 1 in intervals:
                print(line.strip(), time, strength)
                strengths.append(strength)
            time += 2
            if time in intervals:
                print(line.strip(), time, strength)
                strengths.append(strength)
            strength += amount

    for interval in intervals:
        if time < interval:
            strengths.append(strength)

print(strengths)
print(sum([a*b for a,b in list(zip(strengths, intervals))]))

