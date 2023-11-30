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


def set_register(x, y):
  if isnumber(y):
    registers[x] = int(y)
  elif y in registers:
    registers[x] = registers[y]
  else:
    print("Unknown register:", y)


def decrease_register(x, y):
  if x in registers:
    if isnumber(y):
      registers[x] -= int(y)
    elif y in registers:
      registers[x] -= registers[y]
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


def jump_non_zero(x, y):
  if x in registers and registers[x] != 0 or isnumber(x) and int(x) != 0:
    if isnumber(y):
      return int(y)
    else:
      return registers[y]
  return 1


commands = []
registers = {r: 0 for r in ("a", "b", "c", "d", "e", "f", "g", "h")}
registers["a"] = 1

# with StringIO(test) as data:
with open("input23.txt") as data:
  for line in data:
    command, *values = line.strip().split()
    commands.append((command, values))

trace = open("day23_trace.txt", "w")
total_pc = 0
pc = 0
mul_count = 0
while pc in range(len(commands)):
  command, values = commands[pc]
  # if pc in (3, 8, 29, 31):
  #     print("Before", total_pc, pc, command, registers)

  if command == "set":
    set_register(*values)
  elif command == "sub":
    decrease_register(*values)
  elif command == "mul":
    multiply_register(*values)
    mul_count += 1
  elif command == "jnz":
    pc += jump_non_zero(*values)
  else:
    print("Eh?", command, *values)

  # if pc in (8, 31):
  #     print("After", total_pc, pc, command, registers)

  if command != "jnz":
    pc += 1

  total_pc += 1

  if registers["g"] == registers["b"]:
    print(total_pc, pc, registers, file=trace)

print(mul_count)
