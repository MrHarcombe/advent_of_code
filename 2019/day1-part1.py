total = 0
with open("part1.txt") as f:
    mass = f.readline()
    while mass:
        mass = int(mass)
        fuel = (mass // 3) - 2
        #print(fuel)
        total += fuel
        mass = f.readline()

print(total)
