from io import StringIO

test = "s1,x3/4,pe/b"

def spin(line, length):
    return line[-length:] + line[:-length]

def exchange(line, from_, to_):
    temp = list(line)
    temp[from_], temp[to_] = temp[to_], temp[from_]
    return "".join(temp)

def partner(line, a, b):
    temp = list(line)
    ai = temp.index(a)
    bi = temp.index(b)
    temp[ai], temp[bi] = temp[bi], temp[ai]
    return "".join(temp)

# with StringIO(test) as data:
with open("input16.txt") as data:
    for line in data:
        steps = line.strip().split(",")
        
# line = "abcde"
line = "".join([chr(n + ord("a")) for n in range(16)])
before = str(line)
print(line)

for step in steps:
    # print(step, end="->")
    if step[0] == "s":
        line = spin(line, int(step[1:]))
    elif step[0] == "x":
        line = exchange(line, *[int(n) for n in step[1:].split("/")])
    elif step[0] == "p":
        line = partner(line, *step[1:].split("/"))
    else:
        print("Huh?", step)
    # input(line)

print(before,"->",line)

mapping = {}
for i in range(len(before)):
    mapping[i] = line.index(before[i])

print(mapping)
before = list(line)
for i in range(1000000000):
    after = []
    for k in sorted(mapping.keys()):
        after.append(before[mapping[k]])
    before = after
    
print("".join(after))