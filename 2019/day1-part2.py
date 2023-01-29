def reduce(fuel):
    return (fuel // 3) - 2

total = 0
with open("part1.txt") as f:
    mass = f.readline()
    while mass:
        mass = int(mass)
        fuel = reduce(mass)
        #print(fuel)
        total += fuel

        fuel = reduce(fuel)
        while fuel > 0:
            total += fuel
            fuel = reduce(fuel)

        mass = f.readline()

print(total)
