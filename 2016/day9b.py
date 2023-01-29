from io import StringIO

test1 = "ADVENT"
test2 = "A(1x5)BC"
test3 = "(3x3)XYZ"
test4 = "A(2x2)BCD(2x2)EFG"
test5 = "(6x1)(1x3)A"
test6 = "X(8x2)(3x3)ABCY"
test7 = "(27x12)(20x12)(13x14)(7x10)(1x12)A"
test8 = "(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN"
snippet = "(172x1)(3x7)XPJ(70x4)(40x7)WKQANMDILIQOOWQZDNGORPHFNHBKKKVQEJNUVNAQ(3x2)VFV(10x1)XUNNCAFYMV(9x13)OUIKISEPR(66x13)(10x6)JHDDURBDQC(3x11)SNT(2x11)EW(16x6)WMJFKTNQEACIZXLH(5x12)KPVAD"
test = snippet

# 2284750148-> too low

def decompress(incoming, current, count=1):
    # print("-->", incoming, current, count)
    segment_length = 0
    internal_count = 0
    while internal_count < count:
        if incoming[current] == "(":
            internal_count += 1
            current += 1
            span_start = current
            while incoming[current].isdigit():
                internal_count += 1
                current += 1
            span = int(incoming[span_start:current])
            internal_count += 1
            current += 1
            repeat_start = current
            while incoming[current].isdigit():
                internal_count += 1
                current += 1
            repeat = int(incoming[repeat_start:current])
            internal_count += 1
            current += 1
            # print(f"need to decompress {span} characters {count} times, from {test[current]}")
            
            _, inset_length = decompress(incoming[current:current+span], 0, span)
            
            internal_count += span
            current += span
            segment_length += inset_length * repeat
        else:
            internal_count += 1
            current += 1
            segment_length += 1

    # print("<--", current, segment_length)
    return current, segment_length

output = []
pos = 0
# with StringIO(test) as f:
with open("input9.txt") as f:
    for line in f:
        line = line.strip()
        while pos < len(line):
            # print(pos, len(line))
            pos, length = decompress(line, pos)
            output.append(length)
    
print(output, sum(output))
