from io import StringIO

test = """set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2"""

def isnumber(n):
    try:
        int(n)
        return True
    except ValueError:
        return False

def play_sound(x):
    global played, recovered
    if isnumber(x):
        played = x
    elif x in registers:
        played = registers[x]
    else:
        print("Unknown register:", x)
    # print("Played:", played)
    
def set_register(x, y):
    if isnumber(y):
        registers[x] = int(y)
    elif y in registers:
        registers[x] = registers[y]
    else:
        print("Unknown register:", y)
    
def increase_register(x, y):
    if x in registers:
        if isnumber(y):
            registers[x] += int(y)
        elif y in registers:
            registers[x] += registers[y]
        else:
            print("Unknown register:", y)
    else:
        print("Unknown register:", x)
        
def multiply_register(x, y):
    if x in registers:
        if isnumber(y):
            registers[x] *= int(y)
        elif y in registers:
            registers[x] *= registers[y]
        else:
            print("Unknown register:", y)
    else:
        print("Unknown register:", x)

def remainder_register(x, y):
    if x in registers:
        if isnumber(y):
            registers[x] %= int(y)
        elif y in registers:
            registers[x] %= registers[y]
        else:
            print("Unknown register:", y)
    else:
        print("Unknown register:", x)

def recover_last(x):
    global played, recovered
    if x in registers and registers[x] != 0:
        recovered = played
        print("Recovered:", recovered)

def jump_greater(x, y):
    if x in registers and registers[x] > 0:
        if isnumber(y):
            return int(y)
        else:
            return registers[y]
    return 1

commands = []
registers = {}
played = None
recovered = None

# with StringIO(test) as data:
with open("input18.txt") as data:
    for line in data:
        command, *values = line.strip().split()
        commands.append((command, values))
        
pc = 0
while 0 <= pc < len(commands):
    command, values = commands[pc]
    if command == "snd":
        play_sound(*values)
    elif command == "set":
        set_register(*values)
    elif command == "add":
        increase_register(*values)
    elif command == "mul":
        multiply_register(*values)
    elif command == "mod":
        remainder_register(*values)
    elif command == "rcv":
        recover_last(*values)
    elif command == "jgz":
        pc += jump_greater(*values)
    else:
        print("Eh?", command, *values)

    if command != "jgz":
        pc += 1

print(recovered)
