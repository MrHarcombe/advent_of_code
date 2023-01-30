from io import StringIO
from collections import defaultdict
from operator import lt, le, eq, ne, ge, gt

test = """b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10"""

op_map = { "<" : lt, "<=" : le, "==" : eq, "!=" : ne, ">=" : ge, ">" : gt }

commands = []
registers = defaultdict(int)

# with StringIO(test) as f:
with open("input8.txt") as f:
    commands = [l.strip().split() for l in f.readlines()]

max_value = 0
for command in commands:
    register = command[0]
    op = command[1]
    value = int(command[2])
    cond_register = command[4]
    cond_op = op_map[command[5]]
    cond_value = int(command[6])
    
    if cond_op(registers[cond_register], cond_value):
        if op == "inc":
            registers[register] += value
        else:
            registers[register] -= value

    max_value = max(max_value, max(registers.values()))

print("Part 1:", max(registers.values()))
print("Part 2:", max_value)

