def get_parameter(params):
  if len(params) == 0:
    return 0
  else:
    return params.pop()

with open("input.txt") as f:
    line = f.readline()
    ## part 1 tests
    #line = "3,0,4,0,99"
    #line = "1002,4,3,4,33"

    ## part 2 tests
    #line = "3,9,8,9,10,9,4,9,99,-1,8"
    #line = "3,9,7,9,10,9,4,9,99,-1,8"
    #line = "3,3,1108,-1,8,3,4,3,99"
    #line = "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
    ops = list(map(int, line.split(',')))

    index = 0

    full_command = ops[index]
    command = full_command % 100
    parameters = list(map(int, str(full_command // 100)))

    while command != 99:
      #print(command, parameters)
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

        result = int(input("Enter input: "))
        ops[operand] = result
        index += 2

      elif command == 4:
        # output
        operand = ops[index+1]
        print("Output:", ops[operand])
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
