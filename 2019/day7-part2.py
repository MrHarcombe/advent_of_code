import itertools

class intcode:
  def __init__(self, name, intfile, inputs):
    self.name = name
    self.index = 0
    self.inputs = inputs
    self.output = 0

    with open(intfile) as f:
      line = f.readline()
      self.ops = list(map(int, line.split(',')))

    full_command = self.ops[self.index]
    self.command = full_command % 100
    self.parameters = list(map(int, str(full_command // 100)))

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

  def execute_next(self):
    if not self.has_finished():
      print("{}: cmd {}, params {}, inputs {}, output {}".format(self.name, self.command, self.parameters, self.inputs, self.output))

      if self.command == 1:
        # addition
        operand1 = self.ops[self.index+1]
        operand2 = self.ops[self.index+2]
        dest = self.ops[self.index+3]

        mode1 = self.get_parameter()
        mode2 = self.get_parameter()

        value1 = self.ops[operand1] if mode1 == 0 else operand1
        value2 = self.ops[operand2] if mode2 == 0 else operand2

        print("{}: {} + {} -> {}".format(self.name, value1, value2, dest))

        result = value1 + value2
        self.ops[dest] = result
        self.index += 4

      elif self.command == 2:
        # multiplication
        operand1 = self.ops[self.index+1]
        operand2 = self.ops[self.index+2]
        dest = self.ops[self.index+3]

        mode1 = self.get_parameter()
        mode2 = self.get_parameter()

        value1 = self.ops[operand1] if mode1 == 0 else operand1
        value2 = self.ops[operand2] if mode2 == 0 else operand2

        print("{}: {} x {} -> {}".format(self.name, value1, value2, dest))

        result = value1 * value2
        self.ops[dest] = result
        self.index += 4

      elif self.command == 3:
        # input
        operand = self.ops[self.index+1]

        print("{}: {} <- {}".format(self.name, operand, self.inputs))

        result = self.inputs.pop(0)
        self.ops[operand] = result
        self.index += 2

      elif self.command == 4:
        # output
        operand = self.ops[self.index+1]

        print("{}: {} -> output".format(self.name, operand))

        self.output = self.ops[operand]
        self.index += 2

      elif self.command == 5:
        # jump if true (non-zero)
        operand1 = self.ops[self.index+1]
        operand2 = self.ops[self.index+2]

        mode1 = self.get_parameter()
        mode2 = self.get_parameter()

        value1 = self.ops[operand1] if mode1 == 0 else operand1
        value2 = self.ops[operand2] if mode2 == 0 else operand2

        print("{}: {} if true ? {}".format(self.name, value1, value2))

        if value1 != 0:
          self.index = value2
        else:
          self.index += 3

      elif self.command == 6:
        # jump if false (zero)
        operand1 = self.ops[self.index+1]
        operand2 = self.ops[self.index+2]

        mode1 = self.get_parameter()
        mode2 = self.get_parameter()

        value1 = self.ops[operand1] if mode1 == 0 else operand1
        value2 = self.ops[operand2] if mode2 == 0 else operand2

        print("{}: {} if false ? {}".format(self.name, value1, value2))

        if value1 == 0:
          self.index = value2
        else:
          self.index += 3

      elif self.command == 7:
        # less than
        operand1 = self.ops[self.index+1]
        operand2 = self.ops[self.index+2]
        operand3 = self.ops[self.index+3]

        mode1 = self.get_parameter()
        mode2 = self.get_parameter()

        value1 = self.ops[operand1] if mode1 == 0 else operand1
        value2 = self.ops[operand2] if mode2 == 0 else operand2

        print("{}: {} < {} -> {}".format(self.name, value1, value2, operand3))

        if value1 < value2:
          self.ops[operand3] = 1
        else:
          self.ops[operand3] = 0

        self.index += 4

      elif self.command == 8:
        # equal to
        operand1 = self.ops[self.index+1]
        operand2 = self.ops[self.index+2]
        operand3 = self.ops[self.index+3]

        mode1 = self.get_parameter()
        mode2 = self.get_parameter()

        value1 = self.ops[operand1] if mode1 == 0 else operand1
        value2 = self.ops[operand2] if mode2 == 0 else operand2

        print("{}: {} == {} -> {}".format(self.name, value1, value2, operand3))

        if value1 == value2:
          self.ops[operand3] = 1
        else:
          self.ops[operand3] = 0

        self.index += 4

      else:
          print("Unexpected operation:", self.ops[self.index])
          self.index += 1

      full_command = self.ops[self.index]
      self.command = full_command % 100
      self.parameters = list(map(int, str(full_command // 100)))

    else:
      print("{}: Running a halted machine".format(self.name))

  def run_to_completion(self):
    while not self.has_finished():
      self.execute_next()
    return self.get_output()

def test_part1():
  intfile = "test1-3.txt"
  amp = intcode("A", intfile, [1,0])
  output = amp.run_to_completion()
  #print(output)
  amp = intcode("B", intfile, [0,output])
  output = amp.run_to_completion()
  #print(output)
  amp = intcode("C", intfile, [4,output])
  output = amp.run_to_completion()
  #print(output)
  amp = intcode("D", intfile, [3,output])
  output = amp.run_to_completion()
  #print(output)
  amp = intcode("E", intfile, [2,output])
  output = amp.run_to_completion()
  print(output)

def run_part2(intfile, phases):
  amp_a = intcode("A", intfile, [phases[0], 0])
  amp_b = intcode("B", intfile, [phases[1]])
  amp_c = intcode("C", intfile, [phases[2]])
  amp_d = intcode("D", intfile, [phases[3]])
  amp_e = intcode("E", intfile, [phases[4]])

  while not amp_e.has_finished():
    while not (amp_a.has_stalled() or amp_a.has_finished()):
      #print("A", amp_a.get_inputs(), amp_a.get_output())
      amp_a.execute_next()

    print("A {} with output: {}".format("ended" if amp_a.has_finished() else "stalled", amp_a.get_output()))
    amp_b.add_input(amp_a.get_output())
    while not (amp_b.has_stalled() or amp_b.has_finished()):
      #print("B", amp_b.get_inputs(), amp_b.get_output())
      amp_b.execute_next()

    print("B {} with output: {}".format("ended" if amp_b.has_finished() else "stalled", amp_b.get_output()))
    amp_c.add_input(amp_b.get_output())
    while not (amp_c.has_stalled() or amp_c.has_finished()):
      #print("C", amp_c.get_inputs(), amp_c.get_output())
      amp_c.execute_next()

    print("C {} with output: {}".format("ended" if amp_c.has_finished() else "stalled", amp_c.get_output()))
    amp_d.add_input(amp_c.get_output())
    while not (amp_d.has_stalled() or amp_d.has_finished()):
      #print("D", amp_d.get_inputs(), amp_d.get_output())
      amp_d.execute_next()

    print("D {} with output: {}".format("ended" if amp_d.has_finished() else "stalled", amp_d.get_output()))
    amp_e.add_input(amp_d.get_output())
    while not (amp_e.has_stalled() or amp_e.has_finished()):
      #print("E", amp_e.get_inputs(), amp_e.get_output())
      amp_e.execute_next()

    if not amp_e.has_finished():
      print("E stalled with output:", amp_e.get_output())
      amp_a.add_input(amp_e.get_output())

  print("E ended with output:", amp_e.get_output())
  return amp_e.get_output()

outputs = []
for phases in itertools.permutations(range(5,10)):
  outputs.append(run_part2("input.txt", phases))

print("Max output:", max(outputs))
