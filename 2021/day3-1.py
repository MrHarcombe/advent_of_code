inputs = ["" for i in range(12)]

with open("day3/input3.txt") as file:
    for line in file:
        for i, ch in enumerate(line.strip()):
            inputs[i] += ch

gamma = ""
epsilon = ""

for inp in inputs:
    ones = inp.count("1")
    zeroes = inp.count("0")
    if ones > zeroes:
        gamma += "1"
        epsilon += "0"
    else:
        gamma += "0"
        epsilon += "1"

print(gamma,epsilon)

gint = int(gamma, 2)
eint = int(epsilon, 2)
print(gint,eint)

print(gint * eint)