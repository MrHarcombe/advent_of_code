import itertools

def get_parameter(params):
  if len(params) == 0:
    return 0
  else:
    return params.pop()

def run_intcode(inputs):
  with open("input.txt") as f:
      line = f.readline()
      ## part 1 tests
      # (4,3,2,1,0)
      #line = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"
      # (0,1,2,3,4)
      # line = "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0"
      line = "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"

      ops = list(map(int, line.split(',')))

      index = 0
      output = 0

      full_command = ops[index]
      command = full_command % 100
      parameters = list(map(int, str(full_command // 100)))

      while command != 99:
        print(command, parameters, inputs, output)
        if command == 1:
            # addition
            operand1 = ops[index+1]
            mode1 = get_parameter(parameters)
            operand2 = ops[index+2]
            mode2 = get_parameter(parameters)
            dest = ops[index+3]

            value1 = ops[operand1] if mode1 == 0 else operand1
            value2 = ops[operand2] if mode2 == 0 else operand2

            result = value1 + value2
            ops[dest] = result

            index += 4

        elif command == 2:
            # multiplication
            operand1 = ops[index+1]
            mode1 = get_parameter(parameters)
            operand2 = ops[index+2]
            mode2 = get_parameter(parameters)
            dest = ops[index+3]

            value1 = ops[operand1] if mode1 == 0 else operand1
            value2 = ops[operand2] if mode2 == 0 else operand2

            result = value1 * value2
            ops[dest] = result

            index += 4

        elif command == 3:
          # input
          operand = ops[index+1]

          #result = int(input("Enter input: "))
          result = inputs.pop(0)
          #print("Input:", result)
          ops[operand] = result
          index += 2

        elif command == 4:
          # output
          operand = ops[index+1]
          #print("Output:", ops[operand])
          output = ops[operand]
          index += 2

        elif command == 5:
          # jump if true (non-zero)
          operand1 = ops[index+1]
          operand2 = ops[index+2]

          mode1 = get_parameter(parameters)
          mode2 = get_parameter(parameters)

          value1 = ops[operand1] if mode1 == 0 else operand1
          value2 = ops[operand2] if mode2 == 0 else operand2

          if value1 != 0:
            index = value2
          else:
            index += 3

        elif command == 6:
          # jump if false (zero)
          operand1 = ops[index+1]
          operand2 = ops[index+2]

          mode1 = get_parameter(parameters)
          mode2 = get_parameter(parameters)

          value1 = ops[operand1] if mode1 == 0 else operand1
          value2 = ops[operand2] if mode2 == 0 else operand2

          if value1 == 0:
            index = value2
          else:
            index += 3

        elif command == 7:
          # less than
          operand1 = ops[index+1]
          operand2 = ops[index+2]
          operand3 = ops[index+3]

          mode1 = get_parameter(parameters)
          mode2 = get_parameter(parameters)

          value1 = ops[operand1] if mode1 == 0 else operand1
          value2 = ops[operand2] if mode2 == 0 else operand2

          #print("less than:", value1, value2, "setting:", operand3)

          if value1 < value2:
            ops[operand3] = 1
          else:
            ops[operand3] = 0

          index += 4

        elif command == 8:
          # equal to
          operand1 = ops[index+1]
          operand2 = ops[index+2]
          operand3 = ops[index+3]

          mode1 = get_parameter(parameters)
          mode2 = get_parameter(parameters)

          value1 = ops[operand1] if mode1 == 0 else operand1
          value2 = ops[operand2] if mode2 == 0 else operand2

          #print("equal to:", value1, value2, "setting:", operand3)

          if value1 == value2:
            ops[operand3] = 1
          else:
            ops[operand3] = 0

          index += 4

        else:
            print("Unexpected operation:", ops[index])
            index += 1

        full_command = ops[index]
        command = full_command % 100
        parameters = list(map(int, str(full_command // 100)))

  #print(ops)
  return output

outputs = []

def part1():
  for phases in itertools.permutations(range(5)):
    output = 0
    for phase in phases:
      output = run_intcode([phase, output])

    print(phases,"->", output)
    outputs.append(output)

  print(max(outputs))

output = 0
for phase in (9,):
  output = run_intcode([phase, output])
print(output)