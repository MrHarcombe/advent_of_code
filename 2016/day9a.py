test1 = "ADVENT"
test2 = "A(1x5)BC"
test3 = "(3x3)XYZ"
test4 = "A(2x2)BCD(2x2)EFG"
test5 = "(6x1)(1x3)A"
test6 = "X(8x2)(3x3)ABCY"
line = test6

def decompress(incoming, current, outgoing):
    current += 1
    span_start = current
    while line[current].isdigit():
        current += 1
    span = int(line[span_start:current])
    current += 1
    count_start = current
    while line[current].isdigit():
        current += 1
    count = int(line[count_start:current])
    current += 1
    start = current
    # print(f"need to decompress {span} characters {count} times, from {test[start]}")
    
    output.append(line[start:start+span] * count)
    current += span
    return current

output = []
pos = 0
with open("input9.txt") as f:
    for line in f:
        line = line.strip()
        while pos < len(line):
            # print(pos, len(line))
            if line[pos] == "(":
                pos = decompress(line, pos, output)
                
            else:
                output.append(line[pos])
                pos += 1
            
print(len("".join(output)))
