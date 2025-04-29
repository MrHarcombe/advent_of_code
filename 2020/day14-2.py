from io import StringIO
import re

memory_match = re.compile(r"mem\[([0-9]+)\] = ([0-9]+)")

test = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""

memory = {}


def get_dict_from_mask(mask):
    word_size = len(mask)
    d = {}
    for pos, value in enumerate(mask):
        if value != "0":
            power = word_size - pos - 1
            d[power] = value

    return d


def get_dict_from_value(value):
    d = {}
    for pos, value in enumerate(f"{value:036b}"):
        power = 35 - pos
        d[power] = value

    return d


def enumerate_mask_addresses(original, mask):
    mask_address = dict(original)
    mask_address.update(mask)
    
    xs = [key for (key,value) in mask_address.items() if value == "X"]
    count = len(xs)
    for value in range(2**count):
        new_address = dict(mask_address)
        values = f"{value:0{count}b}"
        for pos, ch in enumerate(values):
            new_address[xs[pos]] = ch

        yield get_value_from_dict(new_address)


def get_value_from_dict(d):
    value = 0
    for k, v in d.items():
        value += 2 ** k if v == "1" else 0

    return value


with open("input14.txt") as inputs:
# with StringIO(test) as inputs:
    line = inputs.readline().strip()
    while line != "":
        current_mask = get_dict_from_mask(line.strip()[7:])
        line = inputs.readline().strip()
        while line.startswith("mem"):
            mm = memory_match.match(line)
            proposed_address = get_dict_from_value(int(mm.group(1)))
            value = int(mm.group(2))

            for address in enumerate_mask_addresses(proposed_address, current_mask):
                memory[address] = value

            line = inputs.readline().strip()

print(sum(memory.values()))
