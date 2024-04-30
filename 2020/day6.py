from io import StringIO

test = """abc

a
b
c

ab
ac

a
a
a
a

b"""

count = 0
with open("input6.txt") as data:
# with StringIO(test) as data:
    current = set()
    for line in data:
        line = line.strip()
        if line == "":
            count += len(current)
            current = set()

        else:
            for ch in line:
                current.add(ch)

    count += len(current)
    
    print("Part 1:", count)

count = 0
with open("input6.txt") as data:
# with StringIO(test) as data:
    current = None
    
    for line in data:
        line = line.strip()
        if line == "":
            count += len(current)
            current = None

        else:
            if current == None:
                current = set(line)
            else:
                current &= set(line)

    count += len(current)
    
    print("Part 2:", count)

