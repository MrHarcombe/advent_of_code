from io import StringIO
from math import prod
import re

test = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""
test = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""
mul_pattern = re.compile(r"mul\(([0-9]+),([0-9]+)\)")
do_pattern = re.compile(r"do\(\)")
dont_pattern = re.compile(r"don\'t\(\)")

total1 = 0
total2 = 0
# with StringIO(test) as input_data:
with open("input3.txt") as input_data:
    enable = True
    for line in input_data:
        for m in mul_pattern.finditer(line.strip()):
            # print(m, m.group(0))
            total1 += prod(map(int, m.groups()))

            dos = [dm.start() for dm in do_pattern.finditer(line[:m.start()])]
            donts = [-dm.start() for dm in dont_pattern.finditer(line[:m.start()])]
            dos_and_donts = sorted(dos + donts, key=lambda item: abs(item))
            if len(dos_and_donts) > 0:
                enable = dos_and_donts[-1] > 0

            if enable:
                total2 += prod(map(int, m.groups()))

print("Part 1:", total1)
print("Part 2:", total2)

# 73425968 - too low
# 77877805 - too high
