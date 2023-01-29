from io import StringIO

test = """inc a
jio a, +2
tpl a
inc a"""

# with StringIO(test) as f:
with open("input23.txt") as f:
    commands = [line.strip() for line in f.readlines()]

# print(commands)
a = 1 # 0 for part 1, 1 for part 2
b = 0
pc = 0

while 0 <= pc < len(commands):
    operator, *operands = commands[pc].split()

    if operator == "inc":
        if operands[0] == "a":
            a += 1
        else:
            b += 1

    elif operator == "hlf":
        if operands[0] == "a":
            a //= 2
        else:
            b //= 2
        
    elif operator == "tpl":
        if operands[0] == "a":
            a *= 3
        else:
            b *= 3

    elif operator == "jmp":
        pc += int(operands[0])
        continue

    elif operator == "jie":
        register = operands[0][0]
        if register == "a" and a % 2 == 0 or register == "b" and b % 2 == 0:
            pc += int(operands[1])
            continue

    elif operator == "jio":
        register = operands[0][0]
        if register == "a" and a == 1 or register == "b" and b == 1:
            pc += int(operands[1])
            continue

    pc += 1

print(a,b)
