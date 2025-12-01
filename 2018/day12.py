from collections import defaultdict
from io import StringIO

def display_pots(pots, low, high):
    return "".join([pots[pot] for pot in range(low, high+1)])

def sum_pots(pots):
    total = 0
    for pot in pots:
        if pots[pot] == "#":
            total += pot
    return total

test = """initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #"""

pots = defaultdict(lambda:"")
notes = defaultdict(lambda:"")

# with StringIO(test) as data:
with open("input12.txt") as data:
    initial = data.readline()[15:].strip()
    pots |= {i:v for i,v in enumerate(list(initial))}
    
    data.readline()
    
    for line in data:
        llcrr, n = line.strip().split("=>")
        notes[llcrr.strip()] = n.strip()

part_a = 20
part_b = 50000000000

for gen in range(part_a):
    next_gen = defaultdict(lambda:"")
    low = min(k for k in pots if pots[k] == "#")
    high = max(k for k in pots if pots[k] == "#")
    # print(low,high,display_pots(pots,low,high))
    for pot in range(min(pots)-4,max(pots)+5):
        scan = "".join([pots[n] for n in range(pot,pot+5)])
        # print(pot, scan, "=>", notes[scan])
        next_gen[pot+2] = notes[scan]
    pots = next_gen
    
low = min(k for k in pots if pots[k] == "#")
high = max(k for k in pots if pots[k] == "#")
print(low,high,display_pots(pots,low,high))
    
count = sum_pots(pots)
print("Part 1:", count)

pots = defaultdict(lambda:"")
pots |= {i:v for i,v in enumerate(list(initial))}
previous = sum_pots(pots)
for gen in range(1,150):
    next_gen = defaultdict(lambda:"")
    low = min(k for k in pots if pots[k] == "#")
    high = max(k for k in pots if pots[k] == "#")
    # print(low,high,display_pots(pots,low,high))
    for pot in range(min(pots)-4,max(pots)+5):
        scan = "".join([pots[n] for n in range(pot,pot+5)])
        # print(pot, scan, "=>", notes[scan])
        next_gen[pot+2] = notes[scan]
    pots = next_gen
    count = sum_pots(pots)
    print(gen,"->",count,count-previous)
    previous = count

# 5450000111057 too high
# 5450000111166
# 5450000001166 -> (part_b - 125) * 109 + 14791
