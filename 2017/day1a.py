from io import StringIO

## part 1

# test = "1122" # 3
# test = "1111" # 4
# test = "1234" # 0
test = "91212129" # 9

## part 2

# test = "1212" # 6
# test = "1221" # 0
# test = "123425" # 4
# test = "123123" # 12
# test = "12131415" # 4

with StringIO(test) as f:
    for line in f:
        value = line.strip()

sum = 0
for i, c in enumerate(value):
    if c == value[(i + 1) % len(value)]:
        sum += int(c)
        
print(sum)