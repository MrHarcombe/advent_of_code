import sys, itertools

class intcode:
  def __init__(self, name, intfile, inputs):
    self.name = name
    self.index = 0
    self.inputs = inputs
    self.output = 0
    self.relative = 0

    with open(intfile) as f:
      line = f.readline()
      self.ops = list(map(int, line.split(',')))

    full_command = self.ops[self.index]
    self.command = full_command % 100
    self.parameters = list(map(int, str(full_command // 100)))

  def get_name(self):
    return self.name

  def has_inputs(self):
    return len(self.inputs) > 0

  def get_inputs(self):
    return self.inputs

  def add_input(self, new_input):
    self.inputs.append(new_input)

  def has_stalled(self):
    return len(self.inputs) == 0 and self.command == 3

  def has_finished(self):
    return self.command == 99

  def get_output(self):
    return self.output

  def get_input(self):
    return self.inputs.pop(0)

  def get_parameter(self):
    if len(self.parameters) == 0:
      return 0
    else:
      return self.parameters.pop()

  def get_value_by_mode(self, operand):
    value = 0
    mode = self.get_parameter()
    if mode == 0:
      value = self.get_value(operand)
    elif mode == 2:
      value = self.get_value(self.relative + operand)
    else:
      value = operand

    return value

  def get_value(self, index):
    if index >= len(self.ops):
      self.ops.extend([0 for n in range(index - len(self.ops) + 1)])
      print("{}: Extended -> len(ops) = {}".format(self.name, len(self.ops)), file=sys.stderr)

    return self.ops[index]

  def set_value_by_mode(self, index, value):
    mode = self.get_parameter()

    print("{}: Setting by mode ({}) {} to {}".format(self.name, mode, index, value), file=sys.stderr)
    
    if mode == 2:
      index += self.relative

    self.set_value(index, value)

  def set_value(self, index, value):
    if index >= len(self.ops):
      self.ops.extend([0 for n in range(index - len(self.ops) + 1)])

    print("{}: Setting {} to {}".format(self.name, index, value), file=sys.stderr)
    self.ops[index] = value

  def execute_next(self):
    if not self.has_finished():
      print("{}: cmd {}, params {}, inputs {}, output {}, relative {}".format(self.name, self.command, self.parameters, self.inputs, self.output, self.relative), file=sys.stderr)

      if self.command == 1:
        # addition
        operand1 = self.get_value(self.index+1)
        operand2 = self.get_value(self.index+2)
        dest = self.get_value(self.index+3)

        value1 = self.get_value_by_mode(operand1)
        value2 = self.get_value_by_mode(operand2)
        result = value1 + value2

        print("{}: {} + {} -> {} ({})".format(self.name, value1, value2, result, dest), file=sys.stderr)

        self.set_value_by_mode(dest, result)
        self.index += 4

      elif self.command == 2:
        # multiplication
        operand1 = self.get_value(self.index+1)
        operand2 = self.get_value(self.index+2)
        dest = self.get_value(self.index+3)

        value1 = self.get_value_by_mode(operand1)
        value2 = self.get_value_by_mode(operand2)
        result = value1 * value2

        print("{}: {} x {} -> {} ({})".format(self.name, value1, value2, result, dest), file=sys.stderr)

        self.set_value_by_mode(dest, result)
        self.index += 4

      elif self.command == 3:
        # input
        operand = self.get_value(self.index+1)

        print("{}: {} <- {}".format(self.name, operand, self.inputs), file=sys.stderr)

        result = self.inputs.pop(0)
        self.set_value_by_mode(operand, result)
        self.index += 2

      elif self.command == 4:
        # output
        operand = self.get_value(self.index+1)

        self.output = self.get_value_by_mode(operand)

        print("{}: {} -> output {}".format(self.name, operand, self.output))

        self.index += 2

      elif self.command == 5:
        # jump if true (non-zero)
        operand1 = self.get_value(self.index+1)
        operand2 = self.get_value(self.index+2)

        value1 = self.get_value_by_mode(operand1)
        value2 = self.get_value_by_mode(operand2)

        print("{}: {} if true ? {}".format(self.name, value1, value2), file=sys.stderr)

        if value1 != 0:
          self.index = value2
        else:
          self.index += 3

      elif self.command == 6:
        # jump if false (zero)
        operand1 = self.get_value(self.index+1)
        operand2 = self.get_value(self.index+2)

        value1 = self.get_value_by_mode(operand1)
        value2 = self.get_value_by_mode(operand2)

        print("{}: {} if false ? {}".format(self.name, value1, value2), file=sys.stderr)

        if value1 == 0:
          self.index = value2
        else:
          self.index += 3

      elif self.command == 7:
        # less than
        operand1 = self.get_value(self.index+1)
        operand2 = self.get_value(self.index+2)
        operand3 = self.get_value(self.index+3)

        value1 = self.get_value_by_mode(operand1)
        value2 = self.get_value_by_mode(operand2)

        print("{}: {} < {} -> {}".format(self.name, value1, value2, operand3), file=sys.stderr)

        if value1 < value2:
          self.set_value_by_mode(operand3, 1)
        else:
          self.set_value_by_mode(operand3, 0)

        self.index += 4

      elif self.command == 8:
        # equal to
        operand1 = self.get_value(self.index+1)
        operand2 = self.get_value(self.index+2)
        operand3 = self.get_value(self.index+3)

        value1 = self.get_value_by_mode(operand1)
        value2 = self.get_value_by_mode(operand2)

        print("{}: {} == {} -> {}".format(self.name, value1, value2, operand3), file=sys.stderr)

        if value1 == value2:
          self.set_value_by_mode(operand3, 1)
        else:
          self.set_value_by_mode(operand3, 0)

        self.index += 4

      elif self.command == 9:
        # relative base
        operand1 = self.get_value(self.index+1)

        value1 = self.get_value_by_mode(operand1)

        self.relative += value1
        self.index += 2

      else:
          print("Unexpected operation:", self.ops[self.index], file=sys.stderr)
          self.index += 1

      full_command = self.ops[self.index]
      self.command = full_command % 100
      self.parameters = list(map(int, str(full_command // 100)))

    else:
      print("{}: Running a halted machine".format(self.name), file=sys.stderr)

  def run_to_completion(self):
    while not self.has_finished():
      self.execute_next()
    return self.get_output()

test = intcode("p1", "input.txt", [2])
test.run_to_completion()
print(test.get_name(), "->", test.get_output())