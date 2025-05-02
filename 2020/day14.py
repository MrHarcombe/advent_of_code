from io import StringIO
import re

memory_match = re.compile(r"mem\[([0-9]+)\] = ([0-9]+)")

test = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""

memory = {}

def get_dict_from_mask(mask):
    word_size = len(mask)
    d = {}
    for pos, value in enumerate(mask):
        if value != "X":
            power = word_size - pos - 1
            d[power] = value

    return d

def get_dict_from_value(value):
    d = {}
    for pos, value in enumerate(f"{value:036b}"):
        power = 35 - pos
        d[power] = value

    return d

def get_value_from_dict(d):
    value = 0
    for k, v in d.items():
        value += 2 ** k if v == "1" else 0

    return value

# with StringIO(test) as inputs:
with open("input14.txt") as inputs:
    line = inputs.readline().strip()
    while line != "":
        current_mask = get_dict_from_mask(line.strip()[7:])
        line = inputs.readline().strip()
        while line.startswith("mem"):
            m = memory_match.match(line)
            address = int(m.group(1))
            proposed = get_dict_from_value(int(m.group(2)))

            proposed.update(current_mask)
            memory[address] = get_value_from_dict(proposed)

            line = inputs.readline().strip()

print(sum(memory.values()))

