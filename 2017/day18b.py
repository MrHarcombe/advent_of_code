from io import StringIO

test = """snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d"""

def isnumber(n):
    try:
        int(n)
        return True
    except ValueError:
        return False

def send(pid, x):
    q = f"q{1 if pid == 0 else 0}"
    if isnumber(x):
        value = int(x)
    elif x in registers[pid]:
        value = registers[pid][x]
    else:
        print("Unknown register:", x)
    registers[q].append(value)
    
def set_register(pid, x, y):
    if isnumber(y):
        registers[pid][x] = int(y)
    elif y in registers[pid]:
        registers[pid][x] = registers[pid][y]
    else:
        print("Unknown register:", y)
    
def increase_register(pid, x, y):
    if x in registers[pid]:
        if isnumber(y):
            registers[pid][x] += int(y)
        elif y in registers[pid]:
            registers[pid][x] += registers[pid][y]
        else:
            print("Unknown register:", y)
    else:
        print("Unknown register:", x)
        
def multiply_register(pid, x, y):
    if x in registers[pid]:
        if isnumber(y):
            registers[pid][x] *= int(y)
        elif y in registers[pid]:
            registers[pid][x] *= registers[pid][y]
        else:
            print("Unknown register:", y)
    else:
        print("Unknown register:", x)

def remainder_register(pid, x, y):
    if x in registers[pid]:
        if isnumber(y):
            registers[pid][x] %= int(y)
        elif y in registers[pid]:
            registers[pid][x] %= registers[pid][y]
        else:
            print("Unknown register:", y)
    else:
        print("Unknown register:", x)

def receive(pid, x):
    q = f"q{pid}"
    if len(registers[q]) > 0:
        value = registers[q].pop(0)
        # print("Dequeued:", value)
        registers[pid][x] = value
        return True
    else:
        return False

def jump_greater(pid, x, y):
    if isnumber(x) and int(x) > 0:
        if isnumber(y):
            return int(y)
        else:
            return registers[pid][y]
    elif x in registers[pid] and registers[pid][x] > 0:
        if isnumber(y):
            return int(y)
        else:
            return registers[pid][y]
    return 1

commands = []
registers = {0: {"p" : 0}, 1: {"p" : 1}, "q0" : [], "q1" : []}

# with StringIO(test) as data:
with open("input18.txt") as data:
    for line in data:
        command, *values = line.strip().split()
        commands.append((command, values))

pcs = [0, 0]
running = [True, True]
sent = 0
while (pcs[0] in range(len(commands)) and running[0]) or (pcs[1] in range(len(commands)) and running[1]):
    for pid, pc in enumerate(pcs):
        if pc not in range(len(commands)):
            continue

        assert(running or (not running and command == "rcv"))

        command, values = commands[pc]
        if command == "snd":
            send(pid, *values)
            if pid == 1:
                sent += 1
        elif command == "set":
            set_register(pid, *values)
        elif command == "add":
            increase_register(pid, *values)
        elif command == "mul":
            multiply_register(pid, *values)
        elif command == "mod":
            remainder_register(pid, *values)
        elif command == "rcv":
            running[pid] = receive(pid, *values)
        elif command == "jgz":
            pc += jump_greater(pid, *values)
        else:
            print("Eh?", command, *values)

        if command != "jgz" and running[pid]:
            pc += 1

        pcs[pid] = pc
        
        # if not all(running):
        #    print(pcs, running, sent)

print(sent)

# 129 too low