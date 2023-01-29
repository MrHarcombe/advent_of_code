from io import StringIO

registers = { "a":0, "b":0, "c":1, "d":0 }
lines = []

test = """cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a"""

with open("input12.txt") as f:
#with StringIO(test) as f:
    for line in f:
        command, *parameters = line.strip().split()
        lines.append((command,parameters))

line = 0
while line < len(lines):
    command, parameters = lines[line]
    
    if command == "cpy":
        p1, p2 = parameters
        if p1.isdigit():
            registers[p2] = int(p1)
        else:
            registers[p2] = registers[p1]
    
    elif command == "inc":
        p1, = parameters
        registers[p1] += 1
        
    elif command == "dec":
        p1, = parameters
        registers[p1] -= 1
        
    elif command == "jnz":
        p1, p2 = parameters
        
        if p1.isalpha():
            condition = registers[p1]
        else:
            condition = int(p1)
        
        if condition != 0:
            if p2.isalpha():
                line += registers[p2]
            else:
                line += int(p2)
        else:
            line += 1

    if command != "jnz":
        line += 1

print(registers)