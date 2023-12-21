from collections import defaultdict
from io import StringIO

test = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
# test = "HASH"

def calculate_hash(value):
    hash = 0
    for ch in value:
        hash += ord(ch)
        hash *= 17
        hash %= 256
    return hash

def calculate_hashes(*args):
    for a in args:
        yield calculate_hash(a)

# with StringIO(test) as data:
with open("input15.txt") as data:
    for line in data:
        values = line.strip().split(",")

print("Part 1:", sum([h for h in calculate_hashes(*values)]))

def hash_add(table, value):
    box, lens = value.split("=")
    ibox = calculate_hash(box)
    ilens = int(lens)

    if box not in [b[0] for b in table[ibox]]:
        table[ibox].append((box, ilens))
    else:
        index = [i for i, b in enumerate(table[ibox]) if b[0] == box][0]
        table[ibox][index] = (box, ilens)

def hash_remove(table, value):
    box, _ = value.split("-")
    ibox = calculate_hash(box)
    
    if ibox in table and box in [b[0] for b in table[ibox]]:
        index = [i for i, b in enumerate(table[ibox]) if b[0] == box][0]
        table[ibox].pop(index)

def focusing_power(table):
    power = 0
    for box in table:
        for i, (slot, focal) in enumerate(table[box]):
            power += (box+1) * (i+1) * focal

    return power

hash_table = defaultdict(list)
for value in values:
    if "=" in value:
        hash_add(hash_table, value)
    else:
        hash_remove(hash_table, value)

print("Part 2:", focusing_power(hash_table))
