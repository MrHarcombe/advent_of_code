import io

inputs = """123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i""".split("\n")

circuit = {}

def evaluate(wire):
  command = circuit[wire]
  print("->", wire, command)
  ###
  # 1 operand commands
  # - previously evaluated answer
  # or a list containing
  # - either a numeric value
  # - or a reference to another identifier
  if isinstance(command, int):
    print("<-", command)
    return command
  elif len(command) == 1:
    if command[0].isdigit():
      answer = int(command[0])
    else:
      answer = evaluate(command[0])
    circuit[wire] = answer
    print("<-", answer)
    return answer

  ###
  # 2 operand commands
  # - should only be NOT here
  elif len(command) == 2:
    if command[0] != 'NOT':
      print("?!", wire, command)
      return 0

    else:
      if command[1].isdigit():
        answer = ~ int(command[1])
      else:
        answer = ~ evaluate(command[1])

      if answer < 0:
        answer &= 0xffff

      circuit[wire] = answer
      print("<-", answer)
      return answer

  ###
  # 3 operand commands
  # - AND
  # - OR
  # - LSHIFT
  # - RSHIFT
  elif len(command) == 3:
    if command[1] not in ("AND", "OR", "LSHIFT", "RSHIFT"):
      print("?!", wire, command)
      return 0

    left = 0
    if command[0].isdigit():
      left = int(command[0])
    else:
      left = evaluate(command[0])

    right = 0
    if command[2].isdigit():
      right = int(command[2])
    else:
      right = evaluate(command[2])

    if command[1] == "AND":
      answer = left & right
    elif command[1] == "OR":
      answer = left | right
    elif command[1] == "LSHIFT":
      answer = left << right
    elif command[1] == "RSHIFT":
      answer = left >> right

    if answer < 0:
      answer &= 0xffff

    circuit[wire] = answer
    print("<-", answer)
    return answer

  else:
    print("?!", wire, command)
    return 0

# with io.StringIO(inputs) as f:
with open("input.txt") as f:
  line = f.readline().strip()

  while line != "":
    parts = line.split("->")
    output = parts[1].strip()
    inputs = parts[0].split()

    #print(inputs, output)
    circuit[output] = inputs
    line = f.readline().strip()

print(circuit)
circuit["b"] = 16076
print(evaluate("a"))

#for wire in circuit:
#  signal = evaluate(wire)
#  print(wire,"->",signal)