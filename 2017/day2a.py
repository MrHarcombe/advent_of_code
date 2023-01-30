from io import StringIO

test = """5 1 9 5
7 5 3
2 4 6 8"""

sheet = []

# with StringIO(test) as f:
with open("input2.txt") as f:
    for line in f:
        sheet.append([int(n) for n in line.strip().split()])

checksum = 0
for row in sheet:
    sr = sorted(row)
    checksum += sr[-1] - sr[0]
    
print(checksum)