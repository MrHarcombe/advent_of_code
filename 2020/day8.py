from io import StringIO

test = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""

def switch_nop_jmp(current):
    if current != -1:
        opcode, operand = code[current].strip().split()
        if opcode == "jmp":
            code[current] = f"nop {operand}"
        else:
            code[current] = f"jmp {operand}"

    for next in range(current+1, len(code)):
        opcode, operand = code[next].strip().split()
        if opcode == "jmp":
            code[next] = f"nop {operand}"
            return next
        elif opcode == "nop":
            code[next] = f"jmp {operand}"
            return next
        
    print("Uh-oh")
    return -1

# with StringIO(test) as data:
with open("input8.txt") as data:
    code = data.readlines()

pc = 0
acc = 0
executed = set()
while pc not in executed:
    executed.add(pc)
    opcode, operand = code[pc].strip().split()
    # print(pc, acc, opcode, operand)
    match opcode:
        case "nop":
            pass
        
        case "acc":
            acc += int(operand)

        case "jmp":
            pc += int(operand) - 1

    pc += 1

print("Part 1:", acc)

pc = 0
switched = -1
while pc < len(code):
    switched = switch_nop_jmp(switched)
    
    acc = 0
    executed = set()
    while pc not in executed and pc < len(code):
        executed.add(pc)
        opcode, operand = code[pc].strip().split()
        # print(pc, acc, opcode, operand)
        match opcode:
            case "nop":
                pass
            
            case "acc":
                acc += int(operand)

            case "jmp":
                pc += int(operand) - 1

        pc += 1

    if pc in executed:
        pc = 0

# print("Part 1:", acc)
print("Part 2:", acc)
