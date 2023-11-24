from collections import defaultdict
from io import StringIO

test = """Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A."""

def parse_blueprint(data):
    start = data.readline().strip()[-2:-1]
    steps = int(data.readline().split()[-2])
    states = {}

    while data.readline() != "":
        details = []
        for n in range(9):
            details.append(data.readline().strip().split()[-1][:-1])
        states[details[0]] = details[1:]

    return start, steps, states

tape = defaultdict(int)
tape_index = 0

# with StringIO(test) as data:
with open("input25.txt") as data:
    start, steps, states = parse_blueprint(data)

# print(start, steps, states)

current_state = start
for step in range(steps):
    actions = states[current_state]
    if tape[tape_index] == 0:
        tape[tape_index] = int(actions[1])
        tape_index += 1 if actions[2] == "right" else -1
        current_state = actions[3]
    
    else:
        tape[tape_index] = int(actions[5])
        tape_index += 1 if actions[6] == "right" else -1
        current_state = actions[7]

print("Part 1:", sum([int(n) for n in tape.values()]))
