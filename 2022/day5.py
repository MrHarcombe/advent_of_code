from io import StringIO
from collections import defaultdict

test = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

stacks = defaultdict(list)

def build_initial_stacks(stack_line, box_lines):
    stack_indexes = []
    for i, ch in enumerate(stack_line):
        if ch.isdigit():
            stack_indexes.append(i)

    for line in box_lines:
        for stack_index, line_index in enumerate(stack_indexes):
            if line_index < len(line):
                if line[line_index].strip():
                    stacks[stack_index+1].insert(0, line[line_index])

def process_stacks_a(line):
    _, count, _, from_stack, _, to_stack = line.split()
    #print(stacks, count, from_stack, to_stack)

    for n in range(int(count)):
        stacks[int(to_stack)].append(stacks[int(from_stack)].pop())

def process_stacks_b(line):
    _, count, _, from_stack, _, to_stack = line.split()
    #print(stacks, count, from_stack, to_stack)

    stacks[int(to_stack)] += stacks[int(from_stack)][-int(count):]
    stacks[int(from_stack)] = stacks[int(from_stack)][:-int(count)]

#with StringIO(test) as f:
with open("input5.txt") as f:
    stacks_input = []
    
    for line in f:
        if "[" in line:
            stacks_input.append(line)
        elif line.startswith(" 1"):
            build_initial_stacks(line, stacks_input)
        elif line.startswith("move"):
            process_stacks_b(line)

#print(stacks)
for k in sorted(stacks.keys()):
    print(stacks[k][-1], end="")
print()
