from io import StringIO

def isnumber(value):
    try:
        int(value)
    except ValueError:
        return False
    return True

registers = { "a":2, "b":0, "c":0, "d":0 }
lines = []

test = """out 1
out a"""

with StringIO(test) as f:
# with open("input25.txt") as f:
    for line in f:
        command, *parameters = line.strip().split()
        lines.append((command,parameters))

line = 0
while line < len(lines):
    command, parameters = lines[line]

    if command == "cpy":
        p1, p2 = parameters
        if p2 in registers:
            if isnumber(p1):
                registers[p2] = int(p1)
            elif p1 in registers:
                registers[p2] = registers[p1]
            else:
                print("cpy ignoring dodgy p1", p1)
        else:
            print("cpy ignoring dodgy p2", p2)
    
    elif command == "inc":
        p1, = parameters
        if p1 in registers:
            registers[p1] += 1
        else:
            print("inc ignoring dodgy p1", p1)
        
    elif command == "dec":
        p1, = parameters
        if p1 in registers:
            registers[p1] -= 1
        else:
            print("dec ignoring dodgy p1", p1)
        
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

    elif command == "tgl":
        p1, = parameters
        if p1.isdigit():
            toggle = int(p1)
        else:
            toggle = registers[p1]

        if 0 <= line + toggle < len(lines):
            tgl_command = lines[line + toggle] 
            # print(tgl_command)
            if tgl_command[0] == "inc":
                new_command = ("dec", tgl_command[1])
            elif tgl_command[0] in ("dec", "tgl"):
                new_command = ("inc", tgl_command[1])
            elif tgl_command[0] == "jnz":
                new_command = ("cpy", tgl_command[1])
            elif tgl_command[0] in ("cpy"):
                new_command = ("jnz", tgl_command[1])

            # print(new_command)
            lines[line + toggle] = new_command
        else:
            print("ignoring tgl line", line + toggle)

    elif command == "out":
        p1, = parameters
        if p1.isdigit():
            value = int(p1)
        else:
            value = registers[p1]
        print(value, end=" ")

    # print(command, parameters, "->", registers)

    if command != "jnz":
        line += 1

# print(registers)
