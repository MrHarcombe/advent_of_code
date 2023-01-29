with open("part1.txt") as f:
    line = f.readline()
    ops = list(map(int, line.split(',')))

    # restore 1202 state
    ops[1] = 12
    ops[2] = 2

    index = 0
    while ops[index] != 99:
        if ops[index] == 1:
            # addition
            operand1 = ops[index+1]
            operand2 = ops[index+2]
            dest = ops[index+3]

            result = ops[operand1] + ops[operand2]
            ops[dest] = result

            index += 4

        elif ops[index] == 2:
            # multiplication
            operand1 = ops[index+1]
            operand2 = ops[index+2]
            dest = ops[index+3]

            result = ops[operand1] * ops[operand2]
            ops[dest] = result

            index += 4

        else:
            print("Unexpected operation:", ops[index])
            index += 1

print(ops)
